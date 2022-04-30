from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    JWT_SECRET: str
    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str
    AWS_S3_BUCKET_NAME: str
    WISE_BASE_URL: str
    WISE_ACCESS_TOKEN: str

    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = "utf-8"


settings = Settings()
