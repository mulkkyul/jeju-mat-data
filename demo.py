import streamlit as st
from PIL import Image
import hydralit_components as hc
import pandas as pd

# =====================================================================================
# Page setup
# =====================================================================================
st.set_page_config(layout='wide',initial_sidebar_state='expanded',page_title="제주.맛.데 - 제주 맛집 데이터")
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown("""
<style>
.shopInfo {
    font-size:25px !important;
     color :#C7BACC !important;
               font-family: 'Roboto', sans-serif;
}
.sidebarHeader {
    font-size:25px !important;
     color :#000000 !important;
               font-family: 'Roboto', sans-serif;
}
.columnHeader {
    font-size:50px !important;
    color: black !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown('<p class="columnHeader">제주.맛.데 </br>'
                    '<span style=\"font-size: 40% ; color: gray\">제주 맛집 from 데이터</span></p>', unsafe_allow_html=True)

# =====================================================================================
# Load data
# =====================================================================================
@st.cache
def load_data(filename):
    df = pd.read_csv(filename, header=0, delimiter=',')
    return df

df_data_raw = load_data('./rawData/JT_SHP_SALES_VARTION_LIST_202112.csv').sort_values(by=["RANK_CO"], ascending=False)



# =====================================================================================
# Sidebar
# =====================================================================================
list_foodType = ['모두','한식','음료','간식','양식','아시아음식','패스트푸드','주점및주류판매','부페']
foodType = st.sidebar.radio("음식 종류", options=list_foodType)
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
franchise = st.sidebar.checkbox("프랜차이즈 포함")
airport = st.sidebar.checkbox("제주공항 내 상점 포함")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("제주.맛.데에 대해서 알고 싶다면 [여기로](https://brunch.co.kr/@mulkkyul)")

# =====================================================================================
# Nav. bar
# =====================================================================================
menu_data = [
    {'icon': "fas fa-map-marker-alt", 'label': "구좌읍", 'id': '구좌읍'},
    {'icon': "fas fa-map-marker-alt", 'label': "남원읍", 'id': '남원읍'},
    {'icon': "fas fa-map-marker-alt", 'label': "대정읍", 'id': '대정읍'},
    {'icon': "fas fa-map-marker-alt", 'label': "서귀포시내", 'id': '서귀포시 동지역'},
    {'icon': "fas fa-map-marker-alt", 'label': "성산읍", 'id': '성산읍'},
    {'icon': "fas fa-map-marker-alt", 'label': "안덕면", 'id': '안덕면'},
    {'icon': "fas fa-map-marker-alt", 'label': "애월읍", 'id': '애월읍'},
    {'icon': "fas fa-map-marker-alt", 'label': "우도면", 'id': '우도면'},
    {'icon': "fas fa-map-marker-alt", 'label':"제주시내",'id':'제주시 동지역'},
    {'icon': "fas fa-map-marker-alt", 'label':"조천읍",'id':'조천읍'},
    {'icon': "fas fa-map-marker-alt", 'label': "표선면", 'id': '표선면'},
    {'icon': "fas fa-map-marker-alt", 'label': "한경면", 'id': '한경면'},
    {'icon': "fas fa-map-marker-alt", 'label':"한림읍",'id':'한림읍'},
]
st.info("(모바일사용자) 아래 빨간 메뉴바의 왼쪽 버튼을 터치하여 지역 선택 가능")
over_theme = {'txc_inactive': '#FFFFFF'}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    home_name='전지역',
    hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
    sticky_nav=True, #at the top or not
    sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
)


# =====================================================================================
# find the restaurants
# =====================================================================================
list_franchise = ["한국맥도날드","버거킹","빽다방","던킨","탐앤탐스","파리바게뜨","풀바셋","에이바우트","메가엠지씨","컴포즈",
                  "투썸플레이스","커피빈","할리스","파스쿠찌","뚜레쥬르","써브웨이","파리바게트","김밥천국",
                  "(유)아웃백스테이크","롯데리아","KFC","맘스터치","도미노피자","교촌치킨"]

df_target = df_data_raw
if(not franchise):
    df_target = df_target[df_target["CMPNM_NM"].str.contains('|'.join(list_franchise)) == False]
if(not airport):
    df_target = df_target[df_target["CMPNM_NM"].str.contains("공항") == False]
if(not foodType == "모두"):
    df_target = df_target[df_target["MLSFC_NM"] == foodType]
if(not menu_id == "전지역"):
    df_target = df_target[df_target["AREA_NM"] == menu_id]

# =====================================================================================
# Row 1: Top 30
# =====================================================================================
st.markdown('<p class="columnHeader">'
            '<span style=\"font-size: 40% ; color: black\">색상:</span></br>'
            '<span style=\"font-size: 40% ; color: blue\">파랑: 제주도민이 더 많이 찾은 곳</span></br>'
            '<span style=\"font-size: 40% ; color: red\">빨강: 방문객이 더 많이 찾은 곳</span></br>'
            '<span style=\"font-size: 40% ; color: green\">초록: 제주도민, 방문객 모두 골고루 찾은 곳</span>'
            '</p>', unsafe_allow_html=True)


st.markdown('<p class="columnHeader">Top 1 - 30</p>', unsafe_allow_html=True)

numCols = 3
cols = st.columns(numCols)
for idxCol in range(numCols):
    idxStart = idxCol*10
    idxEnd =  idxStart + 9
    colTitle = "랭킹 %d - %d" % (idxStart+1,idxEnd+1)
    with cols[idxCol]:
        for idxRank in range(idxStart,idxEnd+1):
            if(idxRank >= len(df_target)):
                break
            shopTitle = df_target["CMPNM_NM"].iloc[idxRank]
            shopAddress = df_target["SIGNGU_NM"].iloc[idxRank] + ' ' + df_target["ADSTRD_NM"].iloc[idxRank]
            shopMenu = df_target["MLSFC_NM"].iloc[idxRank] + ' ' + df_target["SCLAS_NM"].iloc[idxRank]

            popularityRatio = 2.0
            if(df_target["JJINHBT_SALES_PRICE_RATE"].iloc[idxRank] > popularityRatio * df_target["OTSD_SALES_PRICE_RATE"].iloc[idxRank]):
                shopPopularity = "blue"
            elif(popularityRatio * df_target["JJINHBT_SALES_PRICE_RATE"].iloc[idxRank] < df_target["OTSD_SALES_PRICE_RATE"].iloc[idxRank]):
                shopPopularity = "red"
            else:
                shopPopularity = "green"

            markdown_shopTitle = f"<p class=\"shopInfo\"><span style=\"color: {shopPopularity}\"> #{idxRank+1}. {shopTitle} </span>  " \
                                 f"<span style=\"font-size: 60% ; color: gray\">{shopMenu}</span> <br>" \
                                 f"<span style=\"font-size: 60% ; color: gray\">{shopAddress}</span></p>"
            st.markdown(markdown_shopTitle, unsafe_allow_html=True)

st.markdown('___')


# =====================================================================================
# Row 2: Top 10 for each category
# =====================================================================================
numCols = 3
cols = st.columns(numCols)
with cols[0]:
    st.markdown('<p class="columnHeader">제주도민이 더 많이 찾은 Top 10</p>', unsafe_allow_html=True)

    countShop = 0
    idxTemp = 0
    while(countShop < 10):
        if(idxTemp >= len(df_target)):
            break
        if (df_target["JJINHBT_SALES_PRICE_RATE"].iloc[idxTemp] > popularityRatio * df_target["OTSD_SALES_PRICE_RATE"].iloc[idxTemp]):
            shopPopularity = "blue"
            countShop = countShop + 1

            shopTitle = df_target["CMPNM_NM"].iloc[idxTemp]
            shopAddress = df_target["SIGNGU_NM"].iloc[idxTemp] + ' ' + df_target["ADSTRD_NM"].iloc[idxTemp]
            shopMenu = df_target["MLSFC_NM"].iloc[idxTemp] + ' ' + df_target["SCLAS_NM"].iloc[idxTemp]

            markdown_shopTitle = f"<p class=\"shopInfo\"><span style=\"color: {shopPopularity}\"> #{countShop}. {shopTitle} </span>  " \
                                 f"<span style=\"font-size: 60% ; color: gray\">{shopMenu}</span> <br>" \
                                 f"<span style=\"font-size: 60% ; color: gray\">{shopAddress}</span></p>"
            st.markdown(markdown_shopTitle, unsafe_allow_html=True)

        idxTemp = idxTemp + 1

with cols[1]:
    st.markdown('<p class="columnHeader">방문객이 더 많이 찾은 Top 10</p>', unsafe_allow_html=True)
    countShop = 0
    idxTemp = 0
    while(countShop < 10):
        if(idxTemp >= len(df_target)):
            break
        if (popularityRatio * df_target["JJINHBT_SALES_PRICE_RATE"].iloc[idxTemp] < df_target["OTSD_SALES_PRICE_RATE"].iloc[idxTemp]):
            shopPopularity = "red"
            countShop = countShop + 1

            shopTitle = df_target["CMPNM_NM"].iloc[idxTemp]
            shopAddress = df_target["SIGNGU_NM"].iloc[idxTemp] + ' ' + df_target["ADSTRD_NM"].iloc[idxTemp]
            shopMenu = df_target["MLSFC_NM"].iloc[idxTemp] + ' ' + df_target["SCLAS_NM"].iloc[idxTemp]

            markdown_shopTitle = f"<p class=\"shopInfo\"><span style=\"color: {shopPopularity}\"> #{countShop}. {shopTitle} </span>  " \
                                 f"<span style=\"font-size: 60% ; color: gray\">{shopMenu}</span> <br>" \
                                 f"<span style=\"font-size: 60% ; color: gray\">{shopAddress}</span></p>"
            st.markdown(markdown_shopTitle, unsafe_allow_html=True)

        idxTemp = idxTemp + 1


with cols[2]:
    #colTitle = "제주도민, 방문객이 골고루 찾은 Top 10"
    #cols[2].title(colTitle)
    st.markdown('<p class="columnHeader">제주도민, 방문객이 골고루 찾은 Top 10</p>', unsafe_allow_html=True)

    countShop = 0
    idxTemp = 0
    while(countShop < 10):
        if(idxTemp >= len(df_target)):
            break
        if (df_target["JJINHBT_SALES_PRICE_RATE"].iloc[idxTemp] > popularityRatio *
                df_target["OTSD_SALES_PRICE_RATE"].iloc[idxTemp]):
            shopPopularity = "blue"
        elif (popularityRatio * df_target["JJINHBT_SALES_PRICE_RATE"].iloc[idxTemp] <
              df_target["OTSD_SALES_PRICE_RATE"].iloc[idxTemp]):
            shopPopularity = "red"
        else:
            shopPopularity = "green"
            countShop = countShop + 1

            shopTitle = df_target["CMPNM_NM"].iloc[idxTemp]
            shopAddress = df_target["SIGNGU_NM"].iloc[idxTemp] + ' ' + df_target["ADSTRD_NM"].iloc[idxTemp]
            shopMenu = df_target["MLSFC_NM"].iloc[idxTemp] + ' ' + df_target["SCLAS_NM"].iloc[idxTemp]

            markdown_shopTitle = f"<p class=\"shopInfo\"><span style=\"color: {shopPopularity}\"> #{countShop}. {shopTitle} </span>  " \
                                 f"<span style=\"font-size: 60% ; color: gray\">{shopMenu}</span> <br>" \
                                 f"<span style=\"font-size: 60% ; color: gray\">{shopAddress}</span></p>"
            st.markdown(markdown_shopTitle, unsafe_allow_html=True)

        idxTemp = idxTemp + 1

# =====================================================================================
# Row 3: Map
# =====================================================================================

st.markdown('___')
st.markdown('<p class="columnHeader">제주 행정 구역 지도</p>', unsafe_allow_html=True)
header_pic = Image.open('jeju.jpg')
st.image(header_pic, use_column_width=True)
st.write("This map was retrieved from [INVEST KOREA](https://www.investkorea.org/jj-kr/cntnts/i-1163/web.do)")


# =====================================================================================
# Row 4: About
# =====================================================================================
about = st.expander('제주.맛.데에 관하여.')
with about:
    st.write("제주.맛.데. = 제주 맛집 데이터")
    st.write("제주.맛.데는 아래 공공 데이터를 활용하여 제작되었습니다.")
    st.write("- 관광 소비행태 데이터_카드사 음식 급상승 데이터 (2022).제주관광공사. [문화 빅데이터 플랫폼](https://www.bigdata-culture.kr/bigdata/user/data_market/detail.do?id=f0306b70-597a-11ec-8ee4-95f65f846b27)")
    st.write("위 데이터셋에서 2021년 12월의 자료로 작성")
    st.write("")
    st.write("제주.맛.데에 대해서 조금 더 알고 싶다면 여기로 -> [브런치](https://brunch.co.kr/@mulkkyul)")


