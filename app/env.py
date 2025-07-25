
class Env:
    """
    Environment variables for the FastAPI application.
    """

    DATABASE_URL: str = "postgresql://leo:secret12345@localhost/local_db"

    def __init__(self):
        import os
        from dotenv import load_dotenv

        # Load environment variables from .env file
        load_dotenv()

        self.DATABASE_URL = os.getenv("DATABASE_URL", self.DATABASE_URL)

env = Env()