import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
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
    
    # 수치형 데이터 정리
    numeric_cols = ['순위', '일관객', '누적관객', '스크린수', '상영횟수']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    return df

try:
    df = load_data()
    
    # Sidebar: 기본 필터 및 정보
    st.sidebar.header("🔍 데이터 탐색 설정")
    min_date = df['날짜'].min().date()
    max_date = df['날짜'].max().date()
    st.sidebar.write(f"**데이터 기간:** {min_date} ~ {max_date}")
    st.sidebar.write(f"**총 등록 영화 수:** {df['영화명'].nunique()}개")
    
    # ==========================================
    # 구역 1: 개별 영화 추이 분석
    # ==========================================
    st.header("📌 Section 1. 개별 영화의 날짜별 관객 수 추이")
    
    # 영화 선택 드롭다운 (가나다 순 정렬)
    movie_list = sorted(df['영화명'].dropna().unique())
    selected_movie = st.selectbox("분석할 영화를 선택하세요:", movie_list)
    
    if selected_movie:
        # 선택한 영화 데이터 필터링
        movie_df = df[df['영화명'] == selected_movie].sort_values('날짜')
        
        # Plotly 선 그래프 생성
        fig1 = px.line(
            movie_df,
            x='날짜',
            y='일관객',
            title=f"'{selected_movie}' 날짜별 일관객 수 변화",
            labels={'날짜': '날짜', '일관객': '일일 관객 수(명)'},
            markers=True,
            hover_data={'날짜': '|%Y-%m-%d', '일관객': ':,d', '순위': True}
        )
        
        # 그래프 스타일링
        fig1.update_traces(
            hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객:</b> %{y:,}명<br><b>순위:</b> %{customdata[0]}위",
            line_color="#E50914"
        )
        fig1.update_layout(
            xaxis_title="날짜",
            yaxis_title="일관객 수 (명)",
            hovermode="x unified",
            template="plotly_white"
        )
        
        st.plotly_chart(fig1, use_container_width=True)
        
        # 사용자가 직접 입력하는 인사이트 공간
        user_insight_1 = st.text_input(
            "이 그래프로 알 수 있는 것 (한 문장 입력):",
            value="선그래프로 내가 알아낸것",
            key="insight_1"
        )
        
        # 입력한 내용 출력
        if user_insight_1:
            st.info(f"💡 **이 그래프로 알 수 있는 것:** {user_insight_1}")

    st.markdown("---")

    # ==========================================
    # 구역 2: 일관객 합계 Top 5 영화 비교
    # ==========================================
    st.header("📌 Section 2. 일관객 합계 Top 5 영화의 날짜별 추이 비교")
    
    # 데이터 기간 내 일관객 합계 기준 Top 5 영화 추출
    top5_movies = (
        df.groupby('영화명')['일관객']
        .sum()
        .nlargest(5)
        .index.tolist()
    )
    
    # Top 5 영화 데이터 필터링
    top5_df = df[df['영화명'].isin(top5_movies)].sort_values('날짜')
    
    # Top 5 선 그래프 생성 (색상으로 영화 구분)
    fig2 = px.line(
        top5_df,
        x='날짜',
        y='일관객',
        color='영화명',
        title="기간 내 일관객 합계 상위 5개 영화의 날짜별 일관객 수 변화",
        labels={'날짜': '날짜', '일관객': '일일 관객 수(명)', '영화명': '영화 제목'},
        markers=True,
        hover_data={'순위': True}
    )
    
    fig2.update_traces(
        hovertemplate="<b>영화명:</b> %{fullData.name}<br><b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객:</b> %{y:,}명<br><b>순위:</b> %{customdata[0]}위"
    )
    
    fig2.update_layout(
        xaxis_title="날짜",
        yaxis_title="일관객 수 (명)",
        hovermode="x unified",
        template="plotly_white",
        legend_title_text="영화 선택 (클릭하여 토글)",
        legend=dict(
            orient="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Section 2 사용자 인사이트 입력 공간
    user_insight_2 = st.text_input(
        "이 그래프로 알 수 있는 것 (한 문장 입력):",
        value="",
        key="insight_2"
    )
    
    if user_insight_2:
        st.info(f"💡 **이 그래프로 알 수 있는 것:** {user_insight_2}")

    st.markdown("---")

    # ==========================================
    # 구역 3: 추후 그래프 추가용 구역
    # ==========================================
    st.header("📌 Section 3. 추후 그래프 추가 구역")
    st.write("👉 *다음 버전에서 추가 분석 그래프가 업로드될 예정입니다.*")

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
