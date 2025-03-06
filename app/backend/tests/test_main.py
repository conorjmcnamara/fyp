import pytest
import os
import uvicorn
from unittest.mock import patch
from typing import Generator
from src.main import main
from src.app import app


@pytest.fixture()
def mock_backend_port() -> Generator[None, None, None]:
    os.environ["BACKEND_PORT"] = "8000"
    yield
    del os.environ["BACKEND_PORT"]


def test_main(mock_backend_port: None):
    with patch.object(uvicorn, "run") as mock_uvicorn_run:
        main()
        mock_uvicorn_run.assert_called_once_with(app, host="0.0.0.0", port=8000)
