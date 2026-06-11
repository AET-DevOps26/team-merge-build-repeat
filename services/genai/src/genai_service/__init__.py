"""GenAI service package."""

import os

__all__ = ["__version__"]

__version__ = os.getenv("APP_VERSION", "0.1.0")
