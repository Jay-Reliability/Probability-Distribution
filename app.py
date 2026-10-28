import io
import os
import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
import scipy.stats as stats
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

# 페이지 기본 설정
st.set_page_config(
    page_title="Probability Distribution Function Graph V1.0",
    page_icon="📈",
    layout="wide",
)

# 한글 폰트 설정 (Matplotlib 그래프 이미지 저장용)
plt.rcParams["axes.unicode_minus"] = False
for font_name in ["Malgun Gothic", "NanumGothic", "AppleGothic", "DejaVu Sans"]:
    plt.rcParams["font.family"] = font_name
    break


def get_dist_prefix(dist_name: str) -> str:
    """CSV 컬럼명 생성을 위한 분포 접두사를 반환합니다 ('확률분포_' + PDF or CDF)."""
    if dist_name == "Weibull 분포":
        return "Weibull"
    return dist_name


def calculate_distribution(dist: str, params: dict, x_min: float, x_max: float, x_step: float):
    """선택된 확률분포와 모수, X축 범위를 바탕으로 PDF와 CDF 데이터를 계산합니다."""
    if x_min >= x_max or x_step <= 0:
        raise ValueError("X축 범위(최소값 < 최대값) 또는 Step(0보다 큰 값)이 올바르지 않습니다.")

    x = np.arange(x_min, x_max + x_step * 0.5, x_step)
    x = np.round(x, 10)

    if dist == "정규분포":
        mean = float(params["평균"])
        std = float(params["표준편차"])
        if std <= 0:
            raise ValueError("표준편차는 0보다 커야 합니다.")
        y_pdf = stats.norm.pdf(x, loc=mean, scale=std)
        y_cdf = stats.norm.cdf(x, loc=mean, scale=std)

    elif dist == "Weibull 분포":
        shape = float(params["형상모수(Shape)"])
        scale = float(params["척도모수(Scale)"])
        if shape <= 0 or scale <= 0:
            raise ValueError("형상모수(Shape)와 척도모수(Scale)는 0보다 커야 합니다.")
        y_pdf = stats.weibull_min.pdf(x, c=shape, scale=scale)
        y_cdf = stats.weibull_min.cdf(x, c=shape, scale=scale)

    elif dist == "대수정규분포":
        mu = float(params["위치모수(μ)"])
        sigma = float(params["척도모수(σ)"])
        if sigma <= 0:
            raise ValueError("척도모수(σ)는 0보다 커야 합니다.")
        y_pdf = stats.lognorm.pdf(x, s=sigma, scale=np.exp(mu))
        y_cdf = stats.lognorm.cdf(x, s=sigma, scale=np.exp(mu))

    elif dist == "지수분포":
        lam = float(params["고장률(λ)"])
        if lam <= 0:
            raise ValueError("고장률(λ)은 0보다 커야 합니다.")
        y_pdf = stats.expon.pdf(x, scale=1.0 / lam)
        y_cdf = stats.expon.cdf(x, scale=1.0 / lam)
    else:
        raise ValueError("확률분포를 선택해주세요.")

    # 무한대 값 보정
    y_pdf = np.where(np.isfinite(y_pdf), y_pdf, 0.0)
    y_cdf = np.where(np.isfinite(y_cdf), y_cdf, 0.0)

    return x, y_pdf, y_cdf


def create_matplotlib_image_bytes(dist: str, x: np.ndarray, y_pdf: np.ndarray, y_cdf: np.ndarray) -> bytes:
    """현재 그려진 그래프를 고화질 JPG 바이트 데이터로 생성합니다."""
    fig = Figure(figsize=(12, 5), dpi=300)
    ax_pdf = fig.add_subplot(121)
    ax_cdf = fig.add_subplot(122)

    ax_pdf.plot(x, y_pdf, color="blue", label="PDF")
    ax_pdf.set_title(f"{dist} - PDF")
    ax_pdf.set_xlabel("x")
    ax_pdf.set_ylabel("Probability Density")
    ax_pdf.grid(True)

    ax_cdf.plot(x, y_cdf, color="red", label="CDF")
    ax_cdf.set_title(f"{dist} - CDF")
    ax_cdf.set_xlabel("x")
    ax_cdf.set_ylabel("Cumulative Probability")
    ax_cdf.grid(True)

    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="jpg", dpi=300, bbox_inches="tight")
    buf.seek(0)
    return buf.getvalue()


def main():
    # 커스텀 스타일 적용
    st.markdown(
        """
        <style>
        .main-title-bar {
            background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 14px 22px;
            border-radius: 8px;
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        </style>
        <div class="main-title-bar">
            <span>Probability Distribution Function Graph V1.0</span>
            <span style="font-size:13px; font-weight:normal; opacity:0.85;">Reliability Distribution Analyzer</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_html, tab_native = st.tabs([
        "🌐 웹 브라우저 전용 UI (Reliability_Distribution_Analyzer.html)",
        "📊 Streamlit 네이티브 대시보드",
    ])

    # 탭 1: 생성된 Reliability_Distribution_Analyzer.html을 그대로 임베드하여 100% 동일한 GUI/UX 제공
    with tab_html:
        html_path = os.path.join(os.path.dirname(__file__), "Reliability_Distribution_Analyzer.html")
        if os.path.exists(html_path):
            with open(html_path, "r", encoding="utf-8") as f:
                html_content = f.read()
            components.html(html_content, height=760, scrolling=True)
        else:
            st.warning("Reliability_Distribution_Analyzer.html 파일을 찾을 수 없습니다.")

    # 탭 2: Streamlit 네이티브 위젯 기반 대시보드
    with tab_native:
        if "app_terminated" not in st.session_state:
            st.session_state.app_terminated = False

        if st.session_state.app_terminated:
            st.info("프로그램이 종료되었습니다. 다시 시작하려면 아래 버튼을 클릭하세요.")
            if st.button("다시 시작하기"):
                st.session_state.app_terminated = False
                st.rerun()
            return

        # 상단 컨트롤 레이아웃: 확률분포 선택 | 모수 입력 | X축 범위 및 간격 | 액션 버튼
        col_dist, col_param, col_range, col_btn = st.columns([1.3, 2.2, 2.5, 1.5])

        with col_dist:
            st.markdown("##### 확률분포 선택")
            dist = st.selectbox(
                "확률분포 선택",
                options=["정규분포", "Weibull 분포", "대수정규분포", "지수분포"],
                index=0,
                label_visibility="collapsed",
            )

        params = {}
        with col_param:
            st.markdown("##### 모수 입력")
            if dist == "정규분포":
                p_col1, p_col2 = st.columns(2)
                params["평균"] = p_col1.number_input("평균", value=0.0, step=0.1, format="%.4g")
                params["표준편차"] = p_col2.number_input("표준편차", value=1.0, min_value=0.0001, step=0.1, format="%.4g")
            elif dist == "Weibull 분포":
                p_col1, p_col2 = st.columns(2)
                params["형상모수(Shape)"] = p_col1.number_input("형상모수(Shape)", value=2.0, min_value=0.0001, step=0.1, format="%.4g")
                params["척도모수(Scale)"] = p_col2.number_input("척도모수(Scale)", value=10.0, min_value=0.0001, step=0.5, format="%.4g")
            elif dist == "대수정규분포":
                p_col1, p_col2 = st.columns(2)
                params["위치모수(μ)"] = p_col1.number_input("위치모수(μ)", value=0.0, step=0.1, format="%.4g")
                params["척도모수(σ)"] = p_col2.number_input("척도모수(σ)", value=1.0, min_value=0.0001, step=0.1, format="%.4g")
            elif dist == "지수분포":
                params["고장률(λ)"] = st.number_input("고장률(λ)", value=0.1, min_value=0.0001, step=0.01, format="%.4g")

        with col_range:
            st.markdown("##### X축 범위 및 간격")
            r_col1, r_col2, r_col3 = st.columns(3)
            x_min = r_col1.number_input("최소값", value=0.0, step=1.0, format="%.4g")
            x_max = r_col2.number_input("최대값", value=100.0, step=1.0, format="%.4g")
            x_step = r_col3.number_input("Step", value=0.1, min_value=0.0001, step=0.1, format="%.4g")

        # 데이터 계산
        try:
            x, y_pdf, y_cdf = calculate_distribution(dist, params, x_min, x_max, x_step)
            prefix = get_dist_prefix(dist)
            pdf_col_name = f"{prefix}_PDF"
            cdf_col_name = f"{prefix}_CDF"

            df_export = pd.DataFrame({
                "x": [f"{val:.1f}" for val in x],
                pdf_col_name: [f"{val:.2f}" for val in y_pdf],
                cdf_col_name: [f"{val:.2f}" for val in y_cdf],
            })
            csv_bytes = df_export.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
            img_bytes = create_matplotlib_image_bytes(dist, x, y_pdf, y_cdf)
            calc_error = None
        except Exception as e:
            calc_error = str(e)
            csv_bytes = b""
            img_bytes = b""

        with col_btn:
            st.markdown("##### 실행 및 저장")
            b_col1, b_col2 = st.columns([2, 1])
            with b_col1:
                st.button("그래프 그리기", use_container_width=True, type="primary")
                st.download_button(
                    label="데이터(CSV) 저장",
                    data=csv_bytes,
                    file_name=f"{get_dist_prefix(dist)}_data.csv",
                    mime="text/csv",
                    disabled=(calc_error is not None),
                    use_container_width=True,
                )
                st.download_button(
                    label="그래프 저장",
                    data=img_bytes,
                    file_name="distribution_graph.jpg",
                    mime="image/jpeg",
                    disabled=(calc_error is not None),
                    use_container_width=True,
                )
            with b_col2:
                if st.button("종료", use_container_width=True):
                    st.session_state.app_terminated = True
                    st.rerun()

        st.divider()

        if calc_error:
            st.error(f"입력 오류: {calc_error}")
            return

        # 좌/우 패널에 PDF, CDF 인터랙티브 그래프 출력 (마우스 오버 시 X, Y 표시)
        g_col1, g_col2 = st.columns(2)

        with g_col1:
            fig_pdf = go.Figure()
            fig_pdf.add_trace(
                go.Scatter(
                    x=x,
                    y=y_pdf,
                    mode="lines",
                    name="PDF",
                    line=dict(color="blue", width=2),
                    hovertemplate="X: %{x:.2f}<br>Y: %{y:.4f}<extra></extra>",
                )
            )
            fig_pdf.update_layout(
                title=f"{dist} - 확률밀도함수(PDF)",
                xaxis_title="x",
                yaxis_title="Probability Density",
                template="plotly_white",
                hovermode="closest",
                height=480,
            )
            st.plotly_chart(fig_pdf, use_container_width=True)

        with g_col2:
            fig_cdf = go.Figure()
            fig_cdf.add_trace(
                go.Scatter(
                    x=x,
                    y=y_cdf,
                    mode="lines",
                    name="CDF",
                    line=dict(color="red", width=2),
                    hovertemplate="X: %{x:.2f}<br>Y: %{y:.4f}<extra></extra>",
                )
            )
            fig_cdf.update_layout(
                title=f"{dist} - 누적확률밀도함수(CDF)",
                xaxis_title="x",
                yaxis_title="Cumulative Probability",
                template="plotly_white",
                hovermode="closest",
                height=480,
            )
            st.plotly_chart(fig_cdf, use_container_width=True)

        with st.expander("📋 CSV 저장 데이터 미리보기"):
            st.dataframe(df_export, use_container_width=True, height=220)


if __name__ == "__main__":
    main()
