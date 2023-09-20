from fastapi.templating import Jinja2Templates
from pathlib import Path

parent_directory = Path(__file__).parent.parent
templates_path = parent_directory / "templates"
templates = Jinja2Templates(directory=templates_path)