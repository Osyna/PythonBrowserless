from dotenv import load_dotenv
import os
load_dotenv()


def get_env_var(name: str) -> str:
    """Get environment variable or raise error if not found."""
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Environment variable {name} not set")
    return value