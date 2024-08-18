from pydantic_settings import BaseSettings, SettingsConfigDict


class StackParameters(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    prefix: str
    ip_address: str
    ami: str
    account_id: str
    aws_region: str
    instance_type: str
