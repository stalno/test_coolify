import os
from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional, Union, TypeAlias
from pathlib import Path


load_dotenv(find_dotenv())
_StrPath: TypeAlias = Union[os.PathLike[str], str, Path]

RETAILCRM_API_KEY = os.getenv("RETAILCRM_API_KEY", "")
PROJECT_NAME = os.getenv("PROJECT_NAME", "")
PROJECT_VERSION = os.getenv("PROJECT_VERSION", "")


class ServerSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="SERVER_",
        extra="ignore",
    )
    methods: List[str] = ["*"]
    headers: List[str] = ["*"]
    origins: List[str] = ["*"]
    host: str = "0.0.0.0"
    port: int = 80


class Settings(BaseSettings):
    server: ServerSettings

    @staticmethod
    def root_dir() -> Path:
        return Path(__file__).resolve().parent.parent.parent

    @classmethod
    def path(cls, *paths: _StrPath, root_dir: Optional[Path] = None) -> Path:
        if root_dir is None:
            root_dir = cls.root_dir()
        return Path(root_dir, *paths)


def load_settings(server: Optional[ServerSettings] = None) -> Settings:
    return Settings(server=server or ServerSettings())
