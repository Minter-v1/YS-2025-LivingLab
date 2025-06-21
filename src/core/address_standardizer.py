from src.utils.config import Config
import requests
import time
from urllib.parse import quote
from typing import Dict, Any, List
import logging


class AddressStandardizer:
    """
    주소 표준화 클래스
    """

    def __init__(self, config):
        self.config = config
        self.api_key = self.config.get_api_key()
        self.api_url = self.config.get_api_url()
        self.api_delay = self.config.get_api_delay()

        # api 키 검증
        if not self.api_key:
            raise ValueError("API Key is not exist")

    def call_address_api(self, address: str) -> Dict[str, any]:
        """도로명주소 API 호출

        Args:
            address (str): 지번 주소 및 주소

        Returns:
            Dict[str, any]: API 응답
        """
        try:
            # NOTE : API 메타 정보에서 필수키 확인
            params = {
                "confmKey": self.api_key,  # 필수키
                "currentPage": 1,  # 필수키
                "countPerPage": 10,  # 필수키
                "keyword": address,  # 필수키
                "resultType": "json",  # 선택키, 리턴타입 json
            }

            # API 호출
            response = requests.get(self.api_url, params=params, timeout=10)

            # HTTP 200
            if response.status_code == 200:
                result = response.json()

                if "results" in result:
                    common = result["results"].get("common", {})
                    error_code = common.get("errorCode", -1)

                    # 정상
                    if error_code == "0":
                        address_list = result["results"].get("juso", [])
                        return {"status": True, "data": address_list}

                    # API 에러
                    else:
                        # TODO : 에러 메세지 처리
                        return {"status": False, "error_code": error_code}

                # 응답 없음
                else:
                    # TODO : 에러 메세지 처리
                    return {"status": False, "message": "Response is not valid"}

            # HTTP 에러
            else:
                return {
                    "status": False,
                    "message": f"HTTP Error : {response.status_code}",
                }
        finally:
            time.sleep(float(self.api_delay))

    def convert_to_road_address(self, address: str) -> Dict[str, Any]:
        """도로명 주소 변환 함수

        Args:
            address (str): 지번 주소 및 주소

        Returns:
            Dict[str, Any]: 도로명 주소 변환
        """
        if not address:
            return {"status": False, "message": "Address is Empty"}

        # 주소 정제
        cleaned_address = self._cleaned_address(address)

        if not cleaned_address:
            return {"status": False, "message": "Address is Empty"}

        # api 호출
        api_result = self.call_address_api(cleaned_address)

        if not api_result.get("status", False):
            return {"status": False, "message": api_result.get("message", "API Error")}

        address_list = api_result.get("data", [])

        # 주소 검색 결과가 없음
        if not address_list:
            return {"status": False, "message": "Not Found Address"}

        best_result = address_list[0]
        return {
            "status": True,
            "standard_address": best_result.get("roadAddr", ""),  # 도로명 주소
            "jibun_address": best_result.get("jibunAddr", ""),  # 지번 주소
            "original_address": address,
        }

    def convert_to_road_address_batch(
        self, address_list: List[str]
    ) -> List[Dict[str, Any]]:
        if not address_list:
            return []

        result = []
        for address in address_list:
            result.append(self.convert_to_road_address(address))

        return result

    # FIXME: remove keyword 등록 필요
    def _cleaned_address(self, address: str) -> str:
        """주소 정제(API 호출 전)

        Args:
            address (str): 원본 주소

        Returns:
            str: 정제 후 주소
        """

        address = address.strip()

        # 단어만 추출 후 연결
        cleaned = " ".join(address.split())

        # TODO: 상세 주소 삭제 (by re)

        # TODO: 제거 키워드 등록
        remove_keywords = []

        for keyword in remove_keywords:
            if keyword in cleaned:
                cleaned = cleaned.replace(keyword, " ")

        # 단어만 추출 후 연결
        cleaned = " ".join(cleaned.split())

        return cleaned


if __name__ == "__main__":
    standardizer = AddressStandardizer(Config())

    test_addresses = [
        "한밭대학교",
        "대전광역시 유성구 대학로 291",
        "대전광역시 서구 글래드스톤 101동 101호",
        "국립한밭대학교",
        "국립한밭대학교 자동화관",  # NOTE: 이 주소형태 에러
    ]

    print(f"\n===== 여러 주소 테스트: {len(test_addresses)}개 =====")
    results = standardizer.convert_to_road_address_batch(test_addresses)
    for addr, res in zip(test_addresses, results):
        print(f"주소: {addr}")
        print(f"결과: {res}")
        print("---")
