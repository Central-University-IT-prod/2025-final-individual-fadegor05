from dishka import Provider, Scope, from_context
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class GunicornSettings(BaseModel):
    workers: int = 4


class ModerationSettings(BaseModel):
    ai: bool = False
    banwords: bool = False


class MinioSettings(BaseModel):
    user: str
    password: str


class OpenrouterSettings(BaseModel):
    token: str


class ServerSettings(BaseModel):
    port: int


class BotSettings(BaseModel):
    token: str


class PostgresSettings(BaseModel):
    user: str
    password: str
    host: str
    port: str
    db: str

    provider: str = "postgresql+asyncpg"

    @property
    def url(self) -> str:
        return f"{self.provider}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

    @property
    def localhost_url(self) -> str:
        return f"{self.provider}://{self.user}:{self.password}@localhost:{self.port}/{self.db}"


class RedisSettings(BaseModel):
    host: str
    port: str

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}/"


class Settings(BaseSettings):
    gunicorn: GunicornSettings
    moderation: ModerationSettings
    minio: MinioSettings
    openrouter: OpenrouterSettings
    server: ServerSettings
    bot: BotSettings
    postgres: PostgresSettings
    redis: RedisSettings

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="_",
        case_sensitive=False,
        extra="ignore",
    )


def get_settings() -> Settings:
    return Settings()  # type: ignore


class SettingsProvider(Provider):
    config = from_context(provides=Settings, scope=Scope.APP)
