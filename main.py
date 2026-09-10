import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

# 메인 제목 및 설명
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.markdown("KOBIS 일별 박스오피스 데이터를 바탕으로 시간의 흐름에 따른 영화 관객 수 및 각종 지표 변화를 탐색하는 도감입니다.")
st.markdown("---")

# 데이터 로드 함수 (캐싱 적용)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    
    # 날짜 열을 datetime 타입으로 변환 (YYYYMMDD 형식)
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d')
    
    # 수치형 데이터 정형화
    numeric_cols = ['순위', '일관객', '누적관객', '스크린수', '상영횟수']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    return df

try:
    df = load_data()
    
    # 사이드바 설정
    st.sidebar.header("🔍 데이터 탐색 설정")
    min_date = df['날짜'].min().date()
    max_date = df['날짜'].max().date()
    st.sidebar.write(f"**데이터 기간:** {min_date} ~ {max_date}")
    st.sidebar.write(f"**총 등록 영화 수:** {df['영화명'].nunique()}개")
    
    # ==========================================
    # 구역 1: 개별 영화 날짜별 일관객 추이
    # ==========================================
    st.header("📌 Section 1. 개별 영화의 날짜별 관객 수 추이")
    
    # 영화 선택 드롭다운
    movie_list = sorted(df['영화명'].dropna().unique())
    selected_movie = st.selectbox("분석할 영화를 선택하세요:", movie_list)
    
    if selected_movie:
        movie_df = df[df['영화명'] == selected_movie].sort_values('날짜')
        
        # Plotly 선 그래프 생성
        fig1 = px.line(
            movie_df,
            x='날짜',
            y='일관객',
            title=f"'{selected_movie}' 날짜별 일관객 수 변화",
            labels={'날짜': '날짜', '일관객': '일일 관객 수(명)'},
            markers=True
        )
        
        # 마우스 호버 스타일 지정
        fig1.update_traces(
            hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객:</b> %{y:,}명<br><b>순위:</b> %{customdata[0]}위",
            customdata=movie_df[['순위']],
            line_color="#E50914"
        )
        fig1.update_layout(
            xaxis_title="날짜",
            yaxis_title="일관객 수 (명)",
            hovermode="x unified",
            template="plotly_white"
        )
        
        st.plotly_chart(fig1, use_container_width=True)
        
        # 인사이트 문구 위치
        st.info(f"💡 **이 그래프로 알 수 있는 것:** '{selected_movie}'의 개봉 초기 관객 집중도와 주말/평일 간의 관객 수 변동 추이를 확인할 수 있습니다.")

    st.markdown("---")

    # ==========================================
    # 구역 2: 추후 그래프 추가 구역
    # ==========================================
    st.header("📌 Section 2. 박스오피스 상위권 누적 관객 흐름 (추가 예정)")
    st.write("👉 *다음 버전에서 시간 흐름에 따른 상위권 영화들의 누적 관객 수 비교 그래프가 추가될 예정입니다.*")

    with st.expander("💡 다음 추가 예정 그래프 구역 미리보기"):
        st.caption("이곳에 다음 시계열 분석 그래프가 들어갈 자리입니다.")
        st.info("💡 **이 그래프로 알 수 있는 것:** (추후 입력 예정)")

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
