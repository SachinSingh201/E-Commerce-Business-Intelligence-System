import os

class Settings:
    PROJECT_NAME: str = "E-Commerce BI System"
    
    # Database settings
    DB_USER: str = os.getenv("DB_USER", "your_username")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "your_password")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_NAME: str = os.getenv("DB_NAME", "your_db_name")
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
