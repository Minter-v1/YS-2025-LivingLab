from pathlib import Path
import pandas as pd


class FileHandler:
    def __init__(self, config, file_path):
        self.config = config
        self.file_path = Path(file_path)
        self.supported_extensions = config.get_supported_extensions()
        self.default_save_path = Path(config.get_save_path())
        self.original_file_name = self.file_path.stem  # 파일명(확장자 제외)

    # 파일 읽기
    def read_file(self):
        # 확장자 검증
        if self.file_path.suffix.lower() not in [".xlsx", ".xls"]:
            raise ValueError(f"Unsupported file format: {self.file_path.suffix}")

        # 데이터 프레임 변환
        df = pd.read_excel(self.file_path)

        return df

    # 파일 검증
    def validate_file(self, df):
        if df is None or df.empty:
            return False, "File is empty"
        return True, "File is valid"

    # 결과 저장
    def save_result(self, df) -> bool:
        # 파일명 생성 (date는 config에서 자동으로 넣음)
        file_name = self.config.format_filename(original_name=self.original_file_name)

        if not file_name.endswith(".xlsx"):
            file_name += ".xlsx"

        # 저장 경로 지정
        output_path = self.default_save_path / file_name

        # 디렉토리가 없으면 생성
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            df.to_excel(output_path, index=False, engine="openpyxl")
            print(f"File saved successfully: {output_path}")
            return True

        except Exception as e:
            print(f"Failed to save file : {e}")
            return False


if __name__ == "__main__":
    from src.utils.config import Config

    # 테스트용 더미 파일 경로
    test_file_path = "test_file.xlsx"

    # 테스트
    try:
        config = Config()
        file_handler = FileHandler(config, test_file_path)
        print("FileHandler created successfully")

    except Exception as e:
        print(f"FileHandler creation failed: {e}")

    test_df = pd.DataFrame(
        {
            "주소": ["대전광역시 유성구 동서대로 125", "대전광역시 유성구 대학로 211"],
            "세대 수": ["1", "2"],
        }
    )
    test_output = "test_output.xlsx"

    # 읽기

    # 검증
    try:
        is_valid, message = file_handler.validate_file(test_df)
        print("File validation successful")

    except Exception as e:
        print(f"File validation failed: {e}")

    # 저장
    try:
        success = file_handler.save_result(test_df)
    except Exception as e:
        print(f"File save failed: {e}")
