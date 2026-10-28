# Probability Distribution Function Graph V1.0

신뢰성 공학 및 데이터 분석에서 자주 사용되는 **4대 확률분포(정규분포, Weibull 분포, 대수정규분포, 지수분포)**에 대해 모수(Parameter)와 X축 범위/간격을 설정하고 **확률밀도함수(PDF)** 및 **누적확률밀도함수(CDF)** 그래프를 분석·저장할 수 있는 웹 애플리케이션입니다.

---

## 주요 기능

1. **4대 확률분포 분석 지원**
   - **정규분포 (Normal Distribution)**: 평균($\mu$), 표준편차($\sigma$)
   - **Weibull 분포 (Weibull Distribution)**: 형상모수(Shape, $k$), 척도모수(Scale, $\lambda$)
   - **대수정규분포 (Lognormal Distribution)**: 위치모수($\mu$), 척도모수($\sigma$)
   - **지수분포 (Exponential Distribution)**: 고장률($\lambda$)
2. **반응형 상단 컨트롤 레이아웃**
   - 어떤 확률분포를 선택하더라도 `그래프 그리기`, `데이터(CSV) 저장`, `그래프 저장`, `종료` 버튼이 화면 밖으로 밀려나지 않고 항상 한눈에 보이도록 설계되었습니다.
3. **데이터(CSV) 저장 기능**
   - 화면에 출력된 그래프의 $(x, y)$ 데이터를 원하는 폴더와 파일명으로 즉시 CSV 저장할 수 있습니다.
   - 컬럼 포맷: `x`, `<확률분포>_PDF`, `<확률분포>_CDF` (예: `x,Weibull_PDF,Weibull_CDF`)
4. **마우스 오버(Hover) 좌표 툴팁 표시**
   - PDF 및 CDF 그래프 선 위에 마우스를 올리면 해당 지점의 `(X, Y)` 좌표값이 그래프 위에 실시간으로 출력됩니다.
5. **고화질 그래프 이미지 저장**
   - 좌측 PDF 그래프와 우측 CDF 그래프를 병합하여 고해상도 이미지(`.jpg` / `.png`)로 저장합니다.

---

## 파일 구성

| 파일명 | 설명 |
| :--- | :--- |
| `Reliability_Distribution_Analyzer.html` | 별도 서버 없이 웹 브라우저에서 즉시 실행되는 독립형 HTML 애플리케이션 |
| `app.py` | Streamlit Cloud 배포용 메인 애플리케이션 파일 |
| `requirements.txt` | Streamlit 배포에 필요한 Python 패키지 목록 |
| `01_Reliability_Distribution_Analyzer.py` | 원본 Windows Tkinter 데스크톱 애플리케이션 코드 |
| `Web_Reliability_Distribution_Graph_Analyzer.md` | 프로젝트 작업지도서 |

---

## 실행 방법

### 1. 웹 브라우저에서 바로 실행 (`Reliability_Distribution_Analyzer.html`)
별도의 설치 없이 `Reliability_Distribution_Analyzer.html` 파일을 더블클릭하여 Chrome, Edge 등 웹 브라우저에서 바로 실행할 수 있습니다.

### 2. 로컬 환경에서 Streamlit 실행 (`app.py`)
```bash
pip install -r requirements.txt
streamlit run app.py
```

### 3. GitHub & Streamlit Community Cloud 배포 방법
1. 본 디렉터리의 파일(`app.py`, `requirements.txt`, `README.md`, `Reliability_Distribution_Analyzer.html`)을 GitHub Repository에 업로드(Push)합니다.
2. [Streamlit Community Cloud](https://share.streamlit.io/)에 접속하여 로그인합니다.
3. **New app** 버튼을 클릭하고 업로드한 GitHub Repository와 Branch를 선택합니다.
4. **Main file path**에 `app.py`를 입력한 뒤 **Deploy!** 버튼을 클릭하면 웹 게시가 완료됩니다.
