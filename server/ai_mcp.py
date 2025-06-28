# server.py
from datetime import datetime
from bs4 import BeautifulSoup
from fastmcp import FastMCP
import requests
import pandas as pd
from io import BytesIO

mcp = FastMCP("Forest Fire")


@mcp.tool
def fire_1_data():
    """
    대형산불위험예보목록
    """
    response = requests.post(
        "http://forestfire.nifos.go.kr/mBfireExcel.action",
        data={
            "sido": "47",
            "sggu": "47730",
            "emd": "0",
        },
    )
    #     행정구역	예보구분	풍속	실효습도	예보일자
    # 경북 의성 비안면	주의보	7.5	43.5	2025년04월26일 18시
    # 경북 의성 단밀면	주의보	7.2	43.5	2025년04월26일 18시
    # 경북 의성 안계면	주의보	7.8	43.5	2025년04월26일 18시
    # 경북 의성 다인면	주의보	7.4	43.5	2025년04월26일 18시
    # 2번째 행의 최신 예보일자를 통하여 금일 예보일자가 맞는지 확인
    # 맞는 모든 행의 행정구역, 예보구본 풍속 실효습도 반환

    # Excel 파일 응답을 파싱하여 데이터 추출

    # Excel 파일을 pandas DataFrame으로 읽기
    try:
        df = pd.read_excel(BytesIO(response.content), header=0)
    except Exception as e:
        return {"error": f"Excel 파일 파싱 오류: {str(e)}"}

    # 컬럼명 확인 및 데이터 검증
    if len(df.columns) < 5:
        return {"error": "필요한 컬럼이 부족합니다."}

    # 2번째 행(인덱스 1)에서 예보일자 추출
    if len(df) < 2:
        return {"error": "데이터가 충분하지 않습니다."}

    now = datetime.now()
    forecast_date = now.strftime("%Y년%m월%d일 %H시")

    # 금일 예보 데이터만 필터링
    today_forecasts = []

    for index, row in df.iterrows():
        if index == 0:  # 헤더 행 건너뛰기
            continue

        row_date = row.iloc[4]  # 5번째 컬럼(예보일자)
        if str(row_date) == str(forecast_date):  # 같은 예보일자인 경우만
            forecast_data = {
                "행정구역": str(row.iloc[0]),
                "예보구분": str(row.iloc[1]),
                "풍속": str(row.iloc[2]),
                "실효습도": str(row.iloc[3]),
                "예보일자": str(row.iloc[4]),
            }
            today_forecasts.append(forecast_data)

    return {"예보일자": str(forecast_date), "예보_데이터": today_forecasts}


@mcp.tool
def fire_2_data():
    """
    소각산불징후예보목록
    """
    response = requests.post(
        "http://forestfire.nifos.go.kr/mIncinerateList.action",
        data={
            "search": "sgg",
            "iffsfAdm": "47",
            "iffsfAdmSgg": "47730",
            "danger": "3",
            "date": datetime.now().strftime("%Y-%m-%d"),
        },
    )

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table")
    if not table:
        return {"error": "테이블을 찾을 수 없습니다."}
    rows = table.find_all("tr")
    if len(rows) < 2:
        return {"error": "데이터가 충분하지 않습니다."}
    cells = rows[1].find_all("td")
    return {
        "high_temp": str(cells[3].get_text(strip=True)),
        "relative_humidity": str(cells[4].get_text(strip=True)),
        "today_high_temp": str(cells[5].get_text(strip=True)),
        "classification": str(cells[6].get_text(strip=True)),
    }


@mcp.tool
def fire_3_data():
    """
        소각산불징후예보목록
        fetch("http://forestfire.nifos.go.kr/mFfdfIdxList.action", {
      "headers": {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7,ja-JP;q=0.6,ja;q=0.5",
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
        "upgrade-insecure-requests": "1"
      },
      "referrer": "http://forestfire.nifos.go.kr/mFfdfIdxList.action",
      "body": "sido=47&date=2025-06-28",
      "method": "POST",
      "mode": "cors",
      "credentials": "include"
    });
    """
    response = requests.post(
        "http://forestfire.nifos.go.kr/mFfdfIdxList.action",
        data={
            "sido": "47",
            "date": datetime.now().strftime("%Y-%m-%d"),
        },
    )
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table")
    if not table:
        return {"error": "테이블을 찾을 수 없습니다."}
    rows = table.find_all("tr")
    if len(rows) < 2:
        return {"error": "데이터가 충분하지 않습니다."}

    ret = {}
    for row in rows[1:]:
        cells = row.find_all("td")
        # 습도(%)	풍속(m/s)	산불확산지수(ha/h)	위험등급
        ret[cells[1].get_text(strip=True)] = {
            "relative_humidity": cells[2].get_text(strip=True),
            "wind_speed": cells[3].get_text(strip=True),
            "fire_spread_index": cells[4].get_text(strip=True),
            "danger_grade": cells[5].get_text(strip=True),
        }
    return ret


@mcp.tool
def fire_4_data():
    """
     산림연료습도
    시도	시군구	읍면동	최소	최대	평균	표준편차

    """
    response = requests.post(
        "http://forestfire.nifos.go.kr/mFmcList.action",
        data={
            "schtype": "emd",
            "sido": "47",
            "sggu": "47730",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "hour": datetime.now().strftime("%H"),
        },
    )
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table")
    if not table:
        return {"error": "테이블을 찾을 수 없습니다."}
    rows = table.find_all("tr")
    if len(rows) < 2:
        return {"error": "데이터가 충분하지 않습니다."}
    ret = {}
    for row in rows[1:]:
        cells = row.find_all("td")
        ret[cells[2].get_text(strip=True)] = {
            "min": cells[3].get_text(strip=True),
            "max": cells[4].get_text(strip=True),
            "avg": cells[5].get_text(strip=True),
            "std": cells[6].get_text(strip=True),
        }
    return ret


if __name__ == "__main__":
    mcp.run()
