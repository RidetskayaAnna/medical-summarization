from fastapi import FastAPI
from models.extractive_baseline import get_extractive_summary
from models.zero_shot import get_zero_shot_summary
from models.few_shot import get_few_shot_summary
from api.schemas import SummarizationRequest, SummarizationResponse


app = FastAPI(
    title="Medical Summarization API",
    description="API для суммаризации историй болезни",
    version="1.0.0"
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/summarize", response_model=SummarizationResponse)
def summarize(request: SummarizationRequest):
    methods = {
        "baseline": get_extractive_summary,
        "zero_shot": get_zero_shot_summary,
        "few_shot": get_few_shot_summary
    }

    selected_methods = (
        methods if request.method == "all"
        else {request.method: methods[request.method]}
    )

    results = {}
    errors = {}

    for method_name, method_function in selected_methods.items():
        try:
            result = method_function(request.text)

            if result == "ОШИБКА":
                errors[method_name] = "Не удалось выполнить суммаризацию"
            else:
                results[method_name] = result

        except Exception as e:
            errors[method_name] = str(e)

    return SummarizationResponse(
        results=results,
        errors=errors
    )