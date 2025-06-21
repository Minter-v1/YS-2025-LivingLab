import configparser
import os
from pathlib import Path
from shutil import copyfile


class Config:
    def __init__(self, config_path="config/config.ini"):
        self.config = configparser.ConfigParser()
        self.config_path = config_path
        self.load_config()

    # config.ini 로드
    def load_config(self):
        if not os.path.exists(self.config_path):
            self.create_config()

        try:
            self.config.read(self.config_path, encoding="utf-8")

            # 로그
            print(f"Success to load config file: {self.config_path}")

        except Exception as e:
            print(f"Failed to load config file: {e} ")

    # config.ini 생성
    def create_config(self):
        template_path = Path("config/config.ini.template")
        destination = Path("config/config.ini")
        copyfile(template_path, destination)

    # config 파일 저장
    def save_config(self):

        try:
            if not os.path.exists(self.config_path):
                Path(self.config_path).mkdir(exist_ok=True, parents=True)

            with open(self.config_path, "w", encoding="utf-8") as f:
                self.config.write(f)

        except Exception as e:
            print(f"Failed to save config : {e}")

    # getter 메서드
    # api키
    def get_api_key(self):
        return self.config.get("API", "address_api", fallback="")

    # 지원 확장자
    def get_supported_extensions(self):
        return self.config.get("FILE", "supported_extensions", fallback=".xlsx, .xls")

    # 저장 경로
    def get_save_path(self):
        return self.config.get("FILE", "default_save_path", fallback="./results/")

    # 파일명 형식
    def get_filename(self):
        return self.config.get(
            "FILE", "result_filename_format", fallback="{original_name}_처리결과_{date}"
        )

    # 실제 파일명 생성
    def format_filename(self, original_name):
        template = self.get_filename()
        from datetime import datetime

        date = datetime.now().strftime("%Y%m%d")

        return template.format(original_name=original_name, date=date)


if __name__ == "__main__":
    config = Config()
    print(config.get_api_key)
    print(config.get_supported_extensions())
    print(config.get_save_path())
    print(config.get_filename())
    print(config.format_filename("test"))
