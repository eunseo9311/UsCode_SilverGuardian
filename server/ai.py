import requests
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import getpass
from pydantic import BaseModel, Field
from typing import Dict, List
import re
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent

server_params = StdioServerParameters(
    command="python",
    # Make sure to update to the full absolute path to your math_server.py file
    args=[os.path.join(os.path.dirname(__file__), "ai_mcp.py")],
)


if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")


# Pydantic 모델 정의
class RegionRisk(BaseModel):
    region_name: str = Field(..., description="지역명")
    risk_level: int = Field(..., ge=1, le=5, description="산불 위험도 (1-5 등급)")


class RegionRiskResponse(BaseModel):
    regions: List[RegionRisk] = Field(..., description="지역별 산불 위험도 목록")

    def to_dict(self) -> Dict[str, int]:
        """지역명: 위험도 형태의 딕셔너리로 변환"""
        return {region.region_name: region.risk_level for region in self.regions}


llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)


# service=data&request=GetFeature&data=LT_C_KFDRSSIGUGRADE&key=인증키&domain=인증키 URL&[요청파라미터]


def vworld_api_request():
    response = requests.get(
        "https://api.vworld.kr/req/data",
        params={
            "service": "data",
            "request": "GetFeature",
            "data": "LT_C_KFDRSSIGUGRADE",
            "key": "B5D53737-89F9-30D3-B59B-187D560C4194",
            "format": "json",
            "page": "1",
            "emdCd": "47730250",
            "attrFilter": "ymd:between:20140112,20150114",
            "geomFilter": "POINT(129.12683628711966 35.09120479827111)",
        },
    )
    return response.content


def get_forest_fire_data():
    """
    산림청 국립산림과학원_산불위험예보정보
    """
    response = requests.get(
        "http://apis.data.go.kr/1400377/forestPoint/forestPointListEmdSearch",
        params={
            "ServiceKey": "xd95vu/SW8XGCB1RxMafxGI49nuQCdNQ62iVIJIAnAov2fLWSIjU3J/OiEUQnuZDVwV2bmhX+xOBdes35AJvzQ==",
            "pageNo": "1",
            "numOfRows": "10",
            "_type": "json",
            "localAreas": "4773047026",
            "excludeForecast": "0",
        },
    )
    return response.content


async def region_state():
    """
    지역 상태 - AI 응답을 구조화된 형태로 반환
    """
    messages = [
        (
            "system",
            """당신은 의성군의 산불 추측 시스템입니다. 의성군의 각 지역의 산불 위험도를 추측합니다. 
        산불 위험도는 0~100 점으로 표시합니다. 100점은 산불 위험도가 가장 높은 것이고, 0점은 산불 위험도가 가장 낮은 것입니다.
        
        응답은 다음 JSON 형식으로만 제공해주세요:
        {
            "regions": [
                {"region_name": "지역명", "risk_level": 숫자},
                {"region_name": "지역명", "risk_level": 숫자}
            ]
        }
        
        의성군의 주요 지역들: 의성읍, 단촌면, 점곡면, 옥산면, 사곡면, 춘산면, 가음면, 금성면, 봉양면, 비안면, 구천면, 단밀면, 단북면, 안계면, 다인면, 신평면, 안평면, 안사면
        """,
        ),
        (
            "human",
            "의성군의 각 지역의 산불 위험도를 추측해주세요. JSON 형식으로만 응답해주세요.",
        ),
    ]

    try:
        print("flag1", os.path.join(os.path.dirname(__file__), "ai_mcp.py"))
        async with stdio_client(server_params) as (read, write):
            print("flag2")
            async with ClientSession(read, write) as session:
                print("flag3")
                # Initialize the connection
                await session.initialize()
                print("flag4")
                # Get tools
                tools = await load_mcp_tools(session)
                print("flag5")
                # Create and run the agent
                agent = create_react_agent("gemini-2.0-flash", tools)
                agent_response = await agent.ainvoke(messages)

        content = str(agent_response.content).strip()

        # JSON 응답 파싱 시도
        # JSON 블록 추출 (```json ... ``` 형태인 경우)
        json_match = re.search(r"```json\s*(.*?)\s*```", content, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # 직접 JSON 파싱 시도
            json_str = content

        data = json.loads(json_str)
        response = RegionRiskResponse(**data)
        return response.to_dict()

    except (json.JSONDecodeError, ValueError) as e:
        # JSON 파싱 실패 시 텍스트에서 지역명과 위험도 추출
        print(f"JSON 파싱 실패, 텍스트 파싱 시도: {e}")
        return parse_text_response(content)


def parse_text_response(text: str) -> Dict[str, int]:
    """
    AI 텍스트 응답에서 지역명과 위험도를 추출
    """
    result = {}

    # 다양한 패턴으로 지역명과 위험도 매칭
    patterns = [
        r"([가-힣]+(?:읍|면|동))[:\s]*(\d+)",  # 지역명: 숫자
        r"([가-힣]+(?:읍|면|동)).*?(\d+)등급",  # 지역명 ... 숫자등급
        r"([가-힣]+(?:읍|면|동)).*?위험도[:\s]*(\d+)",  # 지역명 ... 위험도: 숫자
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text)
        for region, risk in matches:
            try:
                risk_level = int(risk)
                if 1 <= risk_level <= 5:
                    result[region] = risk_level
            except ValueError:
                continue

    return result
