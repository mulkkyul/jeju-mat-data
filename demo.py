import streamlit as st
from PIL import Image
import pandas as pd

# =====================================================================================
# Page setup
# =====================================================================================
st.set_page_config(layout='wide',initial_sidebar_state='expanded',page_title="맛있는 데이터. 제주")
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

st.markdown('<p class="columnHeader"><span style=\"color: #ea4335\">맛있는</span> 데이터 <span style=\"font-size: 60% ; color: #4285f4\">Jeju</span></br></p>', unsafe_allow_html=True)

# =====================================================================================
# Load data
# =====================================================================================
@st.cache
def load_data(filename):
    df = pd.read_csv(filename, header=0, delimiter=',')
    return df

df_data_raw = load_data('./data_julyToDec2021.csv').sort_values(by=["ALL_SALES_PRICE_RATE"], ascending=False)


# =====================================================================================
# Options
# =====================================================================================
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

list_foodType = ['모두','한식','음료','간식','양식','아시아음식','패스트푸드','주점및주류판매','부페']
foodType = st.radio("음식 종류", options=list_foodType)

list_region = ['전지역','구좌읍','남원읍','대정읍','서귀포시내','성산읍','안덕면','애월읍','우도면','제주시내','조천읍','표선면','한경면','한림읍']
region = st.radio("지역", options=list_region)

st.write("")
st.write("")
franchise = st.checkbox("프랜차이즈 포함")
airport = st.checkbox("제주공항 내 상점 포함")
hotel = st.checkbox("호텔/리조트 내 식당 포함")

st.markdown('___')


# =====================================================================================
# find the restaurants
# =====================================================================================
list_franchise = ["한국맥도날드","버거킹","빽다방","던킨","탐앤탐스","파리바게뜨","풀바셋","에이바우트","메가엠지씨","컴포즈",
                  "투썸플레이스","커피빈","할리스","파스쿠찌","뚜레쥬르","써브웨이","파리바게트","김밥천국",
                  "(유)아웃백스테이크","롯데리아","KFC","맘스터치","도미노피자","교촌치킨","배스킨라빈스","아웃백스테이크하우스"]
list_hotel = ["토스카나","한화호텔앤드리조트","제주신화월드"]

df_target = df_data_raw
if(not franchise):
    df_target = df_target[df_target["CMPNM_NM"].str.contains('|'.join(list_franchise)) == False]
if(not airport):
    df_target = df_target[df_target["CMPNM_NM"].str.contains("공항") == False]
if(not hotel):
    df_target = df_target[df_target["CMPNM_NM"].str.contains('|'.join(list_hotel)) == False]

if(not foodType == "모두"):
    df_target = df_target[df_target["MLSFC_NM"] == foodType]
if(not region == "전지역"):
    if (region == "제주시내"):
        df_target = df_target[df_target["AREA_NM"] == "제주시 동지역"]
    elif (region == "서귀포시내"):
        df_target = df_target[df_target["AREA_NM"] == "서귀포시 동지역"]
    else:
        df_target = df_target[df_target["AREA_NM"] == region]

# =====================================================================================
# Row 1: Top 30
# =====================================================================================
st.markdown('<p class="columnHeader">🎉  &nbsp;&nbsp;Top 30</p><i class="fas fa-plane-departure"></i>', unsafe_allow_html=True)

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
                shopPopularity = "#4285f4"
                icon = "🌴"
            elif(popularityRatio * df_target["JJINHBT_SALES_PRICE_RATE"].iloc[idxRank] < df_target["OTSD_SALES_PRICE_RATE"].iloc[idxRank]):
                shopPopularity = "#fbbc05"
                icon = "🧳"
            else:
                shopPopularity = "#34a853"
                icon = "🌴🧳"

            markdown_shopTitle = f"<p class=\"shopInfo\"><span style=\"color: {shopPopularity}\"> #{idxRank+1}. {shopTitle} {icon} </span>  " \
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
    st.markdown('<p class="columnHeader">🌴 &nbsp;제주도민이 더 많이 찾은 Top 10</p>', unsafe_allow_html=True)

    countShop = 0
    idxTemp = 0
    while(countShop < 10):
        if(idxTemp >= len(df_target)):
            break
        if (df_target["JJINHBT_SALES_PRICE_RATE"].iloc[idxTemp] > popularityRatio * df_target["OTSD_SALES_PRICE_RATE"].iloc[idxTemp]):
            shopPopularity = "#4285f4"
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
    st.markdown('<p class="columnHeader">🧳 &nbsp;외지인이 더 많이 찾은 Top 10</p>', unsafe_allow_html=True)
    countShop = 0
    idxTemp = 0
    while(countShop < 10):
        if(idxTemp >= len(df_target)):
            break
        if (popularityRatio * df_target["JJINHBT_SALES_PRICE_RATE"].iloc[idxTemp] < df_target["OTSD_SALES_PRICE_RATE"].iloc[idxTemp]):
            shopPopularity = "#fbbc05"
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
    st.markdown('<p class="columnHeader">🌴🧳 &nbsp;제주도민, 외지인이 골고루 찾은 Top 10</p>', unsafe_allow_html=True)

    countShop = 0
    idxTemp = 0
    while(countShop < 10):
        if(idxTemp >= len(df_target)):
            break
        if (df_target["JJINHBT_SALES_PRICE_RATE"].iloc[idxTemp] > popularityRatio *
                df_target["OTSD_SALES_PRICE_RATE"].iloc[idxTemp]):
            shopPopularity = "#4285f4"
        elif (popularityRatio * df_target["JJINHBT_SALES_PRICE_RATE"].iloc[idxTemp] <
              df_target["OTSD_SALES_PRICE_RATE"].iloc[idxTemp]):
            shopPopularity = "#fbbc05"
        else:
            shopPopularity = "#34a853"
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
st.markdown('___')
st.markdown('<p class="columnHeader"><span style=\"font-size: 90% ; color: gray\">About</span> <span style=\"color: #ea4335\">맛있는</span> 데이터 <span style=\"font-size: 60% ; color: #4285f4\">Jeju</span></br></p>', unsafe_allow_html=True)
st.write("맛있는 데이터, 제주는 제주관광공사에서 제공하는 제주도 내 음식점별 전월 대비 매출 변화량 데이터를 이용하여 제작되었습니다. "         
         "2021년 하반기 (7-12월) 데이터를 취합하여, 전체 매출 금액 비율 (ALL_SALES_PRICE_RATE)로 순위를 매기고, "
         "제주도민 매출금액 비율(JJINHBT_SALES_PRICE_RATE)과 외지인 매출금액 비율(OTSD_SALES_PRICE_RATE)을 이용하여, 제주도민과 외지인이 선호하는 음식점을 구분합니다.")
st.write("")
st.write("- 데이터셋: 관광 소비행태 데이터_카드사 음식 급상승 데이터 (2022).*제주관광공사*. Retrieved from [문화 빅데이터 플랫폼](https://www.bigdata-culture.kr/bigdata/user/data_market/detail.do?id=f0306b70-597a-11ec-8ee4-95f65f846b27)")
st.write("- 소스코드: https://github.com/mulkkyul/jeju-mat-data")
st.write("- 맛있는 데이터, 제주를 만든 이야기가 궁금하다면 여기로 -> [브런치](https://brunch.co.kr/@mulkkyul)")
st.write("")
st.write("")
st.write("by mulkkyul")



