from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

root_directory = Path(__file__).resolve().parent
# print(root_directory)


class Env_Vars(BaseSettings):
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        # Points specifically to root/.env
        env_file=root_directory / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# Pydantic ensures this is instantiated correctly at runtime
env_vars = Env_Vars()  # type: ignore
