import requests
import streamlit as st
import pandas as pd
import html
import streamlit.components.v1 as components
import altair as alt
import textwrap
from pathlib import Path

API_URL = "http://127.0.0.1:8000/summarize"
PROJECT_ROOT = Path(__file__).resolve().parents[2]

EXAMPLE_HISTORY = """Пациент, 65 лет. Жалобы на кашель, повышение температуры до 38°C и общую слабость в течение трёх дней. При осмотре выявлены хрипы в лёгких. Диагноз: внебольничная пневмония. Назначено лечение антибиотиками."""


def insert_example():
    st.session_state.history_text = EXAMPLE_HISTORY


def clear_history():
    st.session_state.history_text = ""


def load_file():
    uploaded_file = st.session_state.get("history_file")
    if uploaded_file is not None:
        try:
            st.session_state.history_text = uploaded_file.getvalue().decode("utf-8-sig")
        except UnicodeDecodeError:
            st.session_state.file_error = "Не удалось прочитать файл. Используйте UTF-8."


st.set_page_config(
    page_title="Medical Summarization",
    layout="wide"
)

st.markdown("""
<style>

div[data-testid="stVerticalBlockBorderWrapper"],
div[data-testid="stVerticalBlockBorderWrapper"] > div,
div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"] {
    background-color: #FFFFFF !important;
    border-radius: 12px;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid #D5E4ED !important;
    padding: 1rem;
}

div[data-testid="stVegaLiteChart"] {
    background-color: #FFFFFF !important;
    border: 1px solid #D5E4ED !important;
    border-radius: 12px;
    padding: 12px;
}

div[data-testid="stVegaLiteChart"] svg,
div[data-testid="stVegaLiteChart"] .vega-embed,
div[data-testid="stVegaLiteChart"] rect.background {
    background-color: #FFFFFF !important;
    fill: #FFFFFF !important;
}

div[data-testid="stMetric"] {
    background-color: #FFFFFF !important;
    border: 1px solid #D5E4ED;
    border-radius: 12px;
    padding: 12px;
}

[data-testid="stMetricLabel"] p {
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    color: #31536B !important;
}

[data-testid="stMetricValue"] {
    font-size: 1.8rem !important;
    font-weight: 650 !important;
    color: #239B72 !important;
}

.summary-text-card {
    background-color: #FFFFFF;
    border: 1px solid #D5E4ED;
    border-radius: 10px;
    padding: 16px 20px;
    color: #31536B;
    line-height: 1.7;
    margin: 8px 0 16px 0;
}



section[data-testid="stSidebar"] button {
    border-radius: 9px !important;
    text-align: left !important;
    justify-content: flex-start !important;
    padding: 10px 14px !important;
    transition: all 0.2s ease;
}

section[data-testid="stSidebar"] button[kind="secondary"] {
    background-color: transparent !important;
    color: #31536B !important;
    border: 1px solid transparent !important;
}

section[data-testid="stSidebar"] button[kind="secondary"]:hover {
    background-color: #E1F0F8 !important;
    border-color: #D5E4ED !important;
}

section[data-testid="stSidebar"] button[kind="primary"] {
    background-color: #D5EAF7 !important;
    color: #31536B !important;
    border: none !important;
    border-left: 4px solid #239B72 !important;
}


section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 0.5rem;
}


section[data-testid="stSidebar"] button {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;

    width: 100% !important;
    min-height: 46px !important;

    padding: 8px 12px !important;
    border-radius: 10px !important;

    text-align: left !important;
    transition: all 0.2s ease;
}

section[data-testid="stSidebar"] button > div {
    display: grid !important;
    grid-template-columns: 24px 130px !important;
    align-items: center !important;
    column-gap: 10px !important;

    width: 164px !important;
    flex-shrink: 0 !important;
}

section[data-testid="stSidebar"] button [data-testid="stIconMaterial"] {
    justify-self: center !important;
    margin: 0 !important;
}

section[data-testid="stSidebar"] button p {
    text-align: left !important;
    margin: 0 !important;
    white-space: nowrap !important;
}

section[data-testid="stSidebar"] button[kind="secondary"] {
    background-color: transparent !important;
    color: #31536B !important;
    border: 1px solid transparent !important;
}

section[data-testid="stSidebar"] button[kind="secondary"]:hover {
    background-color: #E1F0F8 !important;
    border-color: #D5E4ED !important;
}

section[data-testid="stSidebar"] button[kind="primary"] {
    background-color: #D5EAF7 !important;
    color: #31536B !important;
    border: none !important;
    border-left: 4px solid #239B72 !important;
}



section[data-testid="stSidebar"] > div:first-child {
    scrollbar-width: none;
}

section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar {
    display: none;
}


section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    margin-bottom: 0 !important;
}

section[data-testid="stSidebar"] hr {
    margin-top: 0.8rem !important;
    margin-bottom: 0.8rem !important;
}

section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 0.5rem;
}


section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
    padding-top: 2.2rem !important;
}


section[data-testid="stSidebar"] [data-testid="stSidebarHeader"] {
    height: 0 !important;
    min-height: 0 !important;
    padding: 0 !important;
}


section[data-testid="stMain"] .block-container,
section[data-testid="stMain"] [data-testid="stMainBlockContainer"],
div[data-testid="stMainBlockContainer"] {
    padding-top: 2rem !important;
    margin-top: 0rem !important;
}


</style>
""", unsafe_allow_html=True)


def show_summary(text):
    safe_text = html.escape(str(text))
    st.markdown(
        f'<div class="summary-text-card">{safe_text}</div>',
        unsafe_allow_html=True
    )



# Боковая панель

st.sidebar.markdown("""
<div style="display: flex; align-items: center; gap: 11px; margin-bottom: 8px;">
    <div style="
        width: 42px;
        height: 42px;
        background: #E1F4EC;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    ">
        <svg width="25" height="25" viewBox="0 0 24 24" fill="#239B72">
            <path d="M9 2h6v7h7v6h-7v7H9v-7H2V9h7z"/>
        </svg>
    </div>
    <span style="
        color: #31536B;
        font-size: 19px;
        font-weight: 700;
    ">Medical Summarization</span>
</div>
""", unsafe_allow_html=True)

st.sidebar.caption("Система суммаризации медицинских историй")
st.sidebar.divider()

pages = [
    "Суммаризация",
    "Аналитика",
    "Датасет",
    "О проекте"
]

if "current_page" not in st.session_state:
    st.session_state.current_page = "Суммаризация"


def set_page(page_name):
    if st.session_state.current_page != page_name:
        st.session_state.current_page = page_name
        st.session_state.scroll_to_top = True


page_icons = {
    "Суммаризация": ":material/article:",
    "Аналитика": ":material/monitoring:",
    "Датасет": ":material/database:",
    "О проекте": ":material/info:"
}

for page_name in pages:
    st.sidebar.button(
        page_name,
        key=f"nav_{page_name}",
        icon=page_icons[page_name],
        use_container_width=True,
        type="primary" if st.session_state.current_page == page_name else "secondary",
        on_click=set_page,
        args=(page_name,)
    )

page = st.session_state.current_page
should_scroll_to_top = st.session_state.pop("scroll_to_top", False)

st.sidebar.divider()
st.sidebar.caption("Учебный проект • 2026")


# Раздел 1. Суммаризация
if page == "Суммаризация":

    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 4px;">
        <span style="color: #239B72; font-size: 28px;">✚</span>
        <span style="color: #31536B; font-size: 26px; font-weight: 700;">
            Суммаризация истории болезни
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.caption("Введите историю болезни или загрузите текстовый файл.")

    if "history_text" not in st.session_state:
        st.session_state.history_text = ""

    if "file_error" in st.session_state:
        st.error(st.session_state.pop("file_error"))

    st.markdown("**Загрузить файл с историей болезни**")

    st.file_uploader(
        "Выберите TXT-файл",
        type=["txt"],
        key="history_file",
        on_change=load_file,
        label_visibility="collapsed"
    )

    col1, col2 = st.columns(2, gap="small")

    with col1:
        st.button(
            "Вставить пример",
            on_click=insert_example,
            use_container_width=True,
            type="secondary"
        )

    with col2:
        st.button(
            "Очистить поле",
            on_click=clear_history,
            use_container_width=True,
            type="secondary"
        )

    st.markdown("**Текст истории болезни**")

    history = st.text_area(
        "Текст истории болезни",
        height=250,
        placeholder="Вставьте сюда текст истории болезни...",
        key="history_text",
        label_visibility="collapsed"
    )

    st.caption(f"Количество символов: {len(history)}")

    method_options = {
        "Все методы": "all",
        "Baseline": "baseline",
        "Zero-shot": "zero_shot",
        "Few-shot": "few_shot"
    }

    st.markdown("**Метод суммаризации**")

    selected_method = st.selectbox(
        "Метод суммаризации",
        options=list(method_options.keys()),
        label_visibility="collapsed"
    )

    st.write("")

    if st.button(
        "Суммаризировать",
        type="primary",
        use_container_width=True
    ):
        if not history.strip():
            st.warning("Сначала введите историю болезни.")

        else:
            payload = {
                "text": history,
                "method": method_options[selected_method]
            }

            with st.spinner("Выполняется суммаризация..."):
                try:
                    response = requests.post(
                        API_URL,
                        json=payload,
                        timeout=180
                    )

                    response.raise_for_status()
                    data = response.json()

                    st.markdown("""
                    <div style="
                        display: flex;
                        align-items: center;
                        gap: 10px;
                        margin: 24px 0 14px 0;
                    ">
                        <span style="color: #239B72; font-size: 23px;">✚</span>
                        <span style="color: #31536B; font-size: 22px; font-weight: 700;">
                            Результаты суммаризации
                        </span>
                    </div>
                    """, unsafe_allow_html=True)

                    if data.get("results"):
                        all_summaries = []

                        for method_name, summary in data["results"].items():
                            st.markdown(f"**{method_name}**")
                            show_summary(summary)

                            st.download_button(
                                label=f"Скачать {method_name}",
                                data=summary,
                                file_name=f"{method_name}_summary.txt",
                                mime="text/plain",
                                key=f"download_{method_name}"
                            )

                            all_summaries.append(
                                f"Метод: {method_name}\n\n{summary}"
                            )

                        st.download_button(
                            label="Скачать все результаты",
                            data="\n\n".join(all_summaries),
                            file_name="all_summaries.txt",
                            mime="text/plain",
                            key="download_all"
                        )

                    if data.get("errors"):
                        st.warning("Некоторые методы не удалось выполнить.")

                        for method_name, error in data["errors"].items():
                            st.error(f"{method_name}: {error}")

                    if not data.get("results") and not data.get("errors"):
                        st.info("API не вернуло результатов.")

                except requests.exceptions.ConnectionError:
                    st.error("Не удалось подключиться к API. Проверьте FastAPI.")

                except requests.exceptions.Timeout:
                    st.error("Превышено время ожидания ответа от API.")

                except requests.exceptions.HTTPError as error:
                    st.error(f"Ошибка API: {error}")

                except requests.exceptions.RequestException as error:
                    st.error(f"Ошибка запроса: {error}")




# Раздел 2. Аналитика
elif page == "Аналитика":

    results_path = PROJECT_ROOT / "data" / "processed" / "results_test.csv"

    header_col, button_col = st.columns([5, 1])

    with header_col:
        st.markdown("""
        <h2 style="
            color: #31536B;
            font-size: 26px;
            font-weight: 700;
            margin: 10px 0 0 0;
            padding: 0;
        ">
            Аналитика моделей
        </h2>
        """, unsafe_allow_html=True)

    with button_col:
        if st.button(
            "Обновить",
            icon=":material/refresh:",
            use_container_width=True
        ):
            st.rerun()

    if not results_path.exists():
        st.warning("Файл с результатами экспериментов пока не найден.")

    else:
        try:
            results_df = pd.read_csv(
                results_path,
                encoding="utf-8-sig"
            )

            required_columns = [
                "id",
                "reference_summary",
                "baseline_summary",
                "zero_shot_summary",
                "few_shot_summary"
            ]

            missing_columns = [
                col for col in required_columns
                if col not in results_df.columns
            ]

            if missing_columns:
                st.error(
                    f"Отсутствуют столбцы: {', '.join(missing_columns)}"
                )

            elif results_df.empty:
                st.warning("Файл результатов пуст.")

            else:
                modified_time = results_path.stat().st_mtime
                modified_date = pd.to_datetime(
                    modified_time,
                    unit="s"
                ).strftime("%d.%m.%Y %H:%M")

                info_col1, info_col2 = st.columns(2)

                info_col1.caption(f"Записей: {len(results_df)}")

                with info_col2:
                    st.markdown(
                        f'<div style="text-align: right; color: #7D9AAF; font-size: 14px;">'
                        f'Обновлено: {modified_date}</div>',
                        unsafe_allow_html=True
                    )

                st.subheader("Средняя длина резюме")

                methods = {
                    "Baseline": "baseline_summary",
                    "Zero-shot": "zero_shot_summary",
                    "Few-shot": "few_shot_summary"
                }

                cols = st.columns(3, gap="medium")

                for col, (name, column) in zip(cols, methods.items()):
                    avg_length = (
                        results_df[column]
                        .fillna("")
                        .astype(str)
                        .str.len()
                        .mean()
                    )

                    col.metric(
                        name,
                        f"{avg_length:.0f}",
                        help="Среднее количество символов в резюме"
                    )

                st.caption("Среднее количество символов в резюме.")

                st.subheader("Метрики качества")

                st.caption(
                    "Оценка качества суммаризации относительно эталонных резюме."
                )

                st.html("""
                <div style="
                    display: grid;
                    grid-template-columns: repeat(3, minmax(0, 1fr));
                    gap: 20px;
                    align-items: stretch;
                    margin-bottom: 8px;
                ">
                    <div style="
                        background: #FFFFFF;
                        border: 1px solid #D5E4ED;
                        border-radius: 12px;
                        padding: 20px;
                        min-height: 175px;
                        box-sizing: border-box;
                    ">
                        <div style="color: #31536B; font-size: 17px; font-weight: 650; margin-bottom: 14px;">
                            ROUGE-L
                        </div>
                        <div style="color: #6F8DA3; font-size: 14px; line-height: 1.6; min-height: 65px;">
                            Оценивает сходство последовательностей слов между результатом и эталоном.
                        </div>
                        <div style="border-top: 1px solid #E6EEF3; padding-top: 12px; color: #7D9AAF; font-size: 13px;">
                            Ожидает расчёта
                        </div>
                    </div>

                    <div style="
                        background: #FFFFFF;
                        border: 1px solid #D5E4ED;
                        border-radius: 12px;
                        padding: 20px;
                        min-height: 175px;
                        box-sizing: border-box;
                    ">
                        <div style="color: #31536B; font-size: 17px; font-weight: 650; margin-bottom: 14px;">
                            BERTScore
                        </div>
                        <div style="color: #6F8DA3; font-size: 14px; line-height: 1.6; min-height: 65px;">
                            Оценивает семантическое сходство между результатом и эталоном.
                        </div>
                        <div style="border-top: 1px solid #E6EEF3; padding-top: 12px; color: #7D9AAF; font-size: 13px;">
                            Ожидает расчёта
                        </div>
                    </div>

                    <div style="
                        background: #FFFFFF;
                        border: 1px solid #D5E4ED;
                        border-radius: 12px;
                        padding: 20px;
                        min-height: 175px;
                        box-sizing: border-box;
                    ">
                        <div style="color: #31536B; font-size: 17px; font-weight: 650; margin-bottom: 14px;">
                            Critical Fact Recall
                        </div>
                        <div style="color: #6F8DA3; font-size: 14px; line-height: 1.6; min-height: 65px;">
                            Показывает, насколько полно сохранены важные медицинские факты.
                        </div>
                        <div style="border-top: 1px solid #E6EEF3; padding-top: 12px; color: #7D9AAF; font-size: 13px;">
                            Ожидает расчёта
                        </div>
                    </div>
                </div>
                """)

                st.subheader("Сравнение результатов")

                selected_index = st.selectbox(
                    "Медицинская история",
                    options=range(len(results_df)),
                    format_func=lambda i: (
                        f"Запись {i + 1} — ID {results_df.iloc[i]['id']}"
                    )
                )

                row = results_df.iloc[selected_index]

                st.caption(
                    f"Запись {selected_index + 1} из {len(results_df)}"
                )

                st.markdown("**Эталонное резюме**")

                show_summary(row["reference_summary"])

                st.markdown("**Результаты моделей**")

                baseline_tab, zero_tab, few_tab = st.tabs(
                    ["Baseline", "Zero-shot", "Few-shot"]
                )

                with baseline_tab:
                    st.markdown("**Результат Baseline**")
                    show_summary(row["baseline_summary"])

                with zero_tab:
                    st.markdown("**Результат Zero-shot**")
                    show_summary(row["zero_shot_summary"])

                with few_tab:
                    st.markdown("**Результат Few-shot**")
                    show_summary(row["few_shot_summary"])

        except Exception as e:
            st.error(f"Ошибка загрузки результатов: {e}")


# Раздел 3. Датасет
elif page == "Датасет":

    st.markdown("""
    <h2 style="
        color: #31536B;
        font-size: 26px;
        font-weight: 700;
        margin: 10px 0 0 0;
        padding: 0;
    ">
        Датасет
    </h2>
    """, unsafe_allow_html=True)

    st.caption("Статистика и характеристики медицинских историй.")

    try:
        raw_path = PROJECT_ROOT / "data" / "raw" / "medical-summarization.csv"

        train_path = PROJECT_ROOT / "data" / "processed" / "train.csv"
        validation_path = PROJECT_ROOT / "data" / "processed" / "validation.csv"
        test_path = PROJECT_ROOT / "data" / "processed" / "test.csv"

        df = pd.read_csv(raw_path)
        train_df = pd.read_csv(train_path)
        validation_df = pd.read_csv(validation_path)
        test_df = pd.read_csv(test_path)

        st.subheader("Общая информация")

        col1, col2, col3, col4 = st.columns(4, gap="medium")

        col1.metric("Всего записей", len(df))
        col2.metric("Train", len(train_df))
        col3.metric("Validation", len(validation_df))
        col4.metric("Test", len(test_df))


        def style_chart(chart):
            return (
                chart
                .properties(height=280)
                .configure(
                    background="#FFFFFF",
                    view=alt.ViewConfig(stroke=None)
                )
                .configure_axis(
                    labelColor="#52748B",
                    titleColor="#31536B",
                    gridColor="#E6EEF3",
                    domainColor="#D5E4ED",
                    tickColor="#D5E4ED",
                    labelFontSize=11,
                    titleFontSize=12
                )
            )

        st.subheader("Распределение данных")

        split_data = pd.DataFrame({
            "Выборка": ["Train", "Validation", "Test"],
            "Количество записей": [
                len(train_df),
                len(validation_df),
                len(test_df)
            ]
        })

        split_chart = alt.Chart(split_data).mark_bar(
            color="#239B72",
            cornerRadiusTopLeft=5,
            cornerRadiusTopRight=5
        ).encode(
            x=alt.X(
                "Выборка:N",
                sort=["Train", "Validation", "Test"],
                axis=alt.Axis(labelAngle=0, title=None)
            ),
            y=alt.Y(
                "Количество записей:Q",
                axis=alt.Axis(title=None),
                scale=alt.Scale(
                    domainMin=0,
                    nice=True
                )
            ),
            tooltip=[
                alt.Tooltip("Выборка:N"),
                alt.Tooltip("Количество записей:Q")
            ]
        )

        st.altair_chart(
            style_chart(split_chart),
            use_container_width=True
        )

        st.subheader("Длина медицинских историй")

        history_lengths = df["full_history"].fillna("").str.len()

        col1, col2, col3 = st.columns(3, gap="medium")

        col1.metric(
            "Средняя длина",
            f"{history_lengths.mean():.0f}",
            help="Среднее количество символов"
        )

        col2.metric(
            "Медианная длина",
            f"{history_lengths.median():.0f}",
            help="Медианное количество символов"
        )

        col3.metric(
            "Максимальная длина",
            f"{history_lengths.max():.0f}",
            help="Максимальное количество символов"
        )

        st.caption("Все значения указаны в символах.")

        history_bins = pd.cut(history_lengths, bins=10)
        history_counts = history_bins.value_counts(sort=False)

        history_distribution = pd.DataFrame({
            "Интервал": [
                f"{int(interval.left)}–{int(interval.right)}"
                for interval in history_counts.index
            ],
            "Количество": history_counts.values
        })

        history_chart = alt.Chart(history_distribution).mark_bar(
            color="#239B72",
            cornerRadiusTopLeft=5,
            cornerRadiusTopRight=5
        ).encode(
            x=alt.X(
                "Интервал:N",
                sort=history_distribution["Интервал"].tolist(),
                axis=alt.Axis(
                    labelAngle=0,
                    labelLimit=90,
                    title=None
                )
            ),
            y=alt.Y(
                "Количество:Q",
                axis=alt.Axis(title=None),
                scale=alt.Scale(domainMin=0, nice=True)
            ),
            tooltip=[
                alt.Tooltip("Интервал:N"),
                alt.Tooltip("Количество:Q")
            ]
        )

        st.altair_chart(
            style_chart(history_chart),
            use_container_width=True
        )

        st.subheader("Длина эталонных резюме")

        summary_lengths = df["reference_summary"].fillna("").str.len()

        col1, col2, col3 = st.columns(3, gap="medium")

        col1.metric(
            "Средняя длина",
            f"{summary_lengths.mean():.0f}",
            help="Среднее количество символов"
        )

        col2.metric(
            "Медианная длина",
            f"{summary_lengths.median():.0f}",
            help="Медианное количество символов"
        )

        col3.metric(
            "Максимальная длина",
            f"{summary_lengths.max():.0f}",
            help="Максимальное количество символов"
        )

        st.caption("Все значения указаны в символах.")

        summary_bins = pd.cut(summary_lengths, bins=10)
        summary_counts = summary_bins.value_counts(sort=False)

        summary_distribution = pd.DataFrame({
            "Интервал": [
                f"{int(interval.left)}–{int(interval.right)}"
                for interval in summary_counts.index
            ],
            "Количество": summary_counts.values
        })

        summary_chart = alt.Chart(summary_distribution).mark_bar(
            color="#239B72",
            cornerRadiusTopLeft=5,
            cornerRadiusTopRight=5
        ).encode(
            x=alt.X(
                "Интервал:N",
                sort=summary_distribution["Интервал"].tolist(),
                axis=alt.Axis(
                    labelAngle=0,
                    labelLimit=90,
                    title=None
                )
            ),
            y=alt.Y(
                "Количество:Q",
                axis=alt.Axis(title=None),
                scale=alt.Scale(domainMin=0, nice=True)
            ),
            tooltip=[
                alt.Tooltip("Интервал:N"),
                alt.Tooltip("Количество:Q")
            ]
        )

        st.altair_chart(
            style_chart(summary_chart),
            use_container_width=True
        )

        st.subheader("Структура датасета")

        st.caption("Столбцы и их назначение в исходном датасете.")

        columns_df = pd.DataFrame({
            "Название столбца": df.columns,
            "Описание": [
                "Идентификатор записи",
                "Полная история болезни",
                "Эталонное краткое содержание"
            ]
        })

        styled_columns_df = (
            columns_df.style
            .set_properties(**{
                "background-color": "#FFFFFF",
                "color": "#31536B",
                "border-color": "#D5E4ED",
                "padding": "10px"
            })
            .set_table_styles([
                {
                    "selector": "th",
                    "props": [
                        ("background-color", "#F5FAFE"),
                        ("color", "#31536B"),
                        ("font-weight", "600"),
                        ("border-color", "#D5E4ED")
                    ]
                }
            ])
        )

        st.dataframe(
            styled_columns_df,
            use_container_width=True,
            hide_index=True
        )

    except FileNotFoundError as error:
        st.error(f"Не найден файл датасета: {error.filename}")

    except Exception as error:
        st.error(f"Ошибка при загрузке датасета: {error}")



# Раздел 4. О проекте
elif page == "О проекте":

    st.markdown("""
    <h2 style="
        color: #31536B;
        font-size: 26px;
        font-weight: 700;
        margin: 10px 0 0 0;
        padding: 0;
    ">
        О проекте
    </h2>
    """, unsafe_allow_html=True)

    st.caption("Информация о системе и используемых технологиях.")

    st.subheader("Medical Summarization")

    st.write("""
    Проект посвящён автоматической суммаризации медицинских историй
    для упрощения передачи информации между медицинскими специалистами.
    """)

    st.subheader("Реализуемые методы")


    st.html("""
    <div style="
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 20px;
        align-items: stretch;
        margin-bottom: 8px;
    ">
        <div style="
            background-color: #FFFFFF;
            border: 1px solid #D5E4ED;
            border-radius: 12px;
            padding: 20px;
            min-height: 130px;
            box-sizing: border-box;
        ">
            <div style="color: #31536B; font-size: 17px; font-weight: 650; margin-bottom: 18px;">
                Baseline
            </div>
            <div style="color: #6F8DA3; font-size: 14px; line-height: 1.6;">
                Базовый метод суммаризации.
            </div>
        </div>
        <div style="
            background-color: #FFFFFF;
            border: 1px solid #D5E4ED;
            border-radius: 12px;
            padding: 20px;
            min-height: 130px;
            box-sizing: border-box;
        ">
            <div style="color: #31536B; font-size: 17px; font-weight: 650; margin-bottom: 18px;">
                Zero-shot
            </div>
            <div style="color: #6F8DA3; font-size: 14px; line-height: 1.6;">
                Суммаризация языковой моделью без примеров.
            </div>
        </div>
        <div style="
            background-color: #FFFFFF;
            border: 1px solid #D5E4ED;
            border-radius: 12px;
            padding: 20px;
            min-height: 130px;
            box-sizing: border-box;
        ">
            <div style="color: #31536B; font-size: 17px; font-weight: 650; margin-bottom: 18px;">
                Few-shot
            </div>
            <div style="color: #6F8DA3; font-size: 14px; line-height: 1.6;">
                Суммаризация языковой моделью с примерами.
            </div>
        </div>
    </div>
    """)

    st.subheader("Технологии")

    technologies = [
        "Python",
        "FastAPI",
        "Streamlit",
        "LLM API",
        "Pandas"
    ]

    tech_cols = st.columns(len(technologies))

    for col, technology in zip(tech_cols, technologies):
        with col:
            st.markdown(
                f"""
                <div style="
                    background-color: #FFFFFF;
                    border: 1px solid #D5E4ED;
                    border-radius: 9px;
                    padding: 10px 4px;
                    margin: 30px;
                    text-align: center;
                    color: #31536B;
                    font-size: 13px;
                    font-weight: 600;
                ">
                    {technology}
                </div>
                """,
                unsafe_allow_html=True
            )


    st.warning(
        "Приложение является учебным проектом. "
        "Результаты суммаризации не предназначены для самостоятельной "
        "диагностики или принятия медицинских решений."
    )

if should_scroll_to_top:
    components.html(
        """
        <script>
            function scrollMainToTop() {
                const doc = window.parent.document;

                const main = doc.querySelector(
                    '[data-testid="stMain"]'
                );

                if (main) {
                    main.scrollTo({
                        top: 0,
                        behavior: "instant"
                    });
                }

                const container = doc.querySelector(
                    '[data-testid="stMainBlockContainer"]'
                );

                if (container && main) {
                    main.scrollTop = Math.max(
                        0,
                        container.offsetTop - 12
                    );
                }
            }

            requestAnimationFrame(() => {
                scrollMainToTop();
                requestAnimationFrame(scrollMainToTop);
            });
        </script>
        """,
        height=0
    )