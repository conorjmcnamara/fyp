import pytest
from unittest.mock import patch, MagicMock
from typing import Generator
from transformers import AutoModel, AutoTokenizer
from src.utils.download_hf_model import download_hf_model


@pytest.fixture
def mock_auto_model() -> Generator[MagicMock, None, None]:
    with patch.object(AutoModel, "from_pretrained", return_value=MagicMock()) as mock_auto_model:
        yield mock_auto_model


@pytest.fixture
def mock_auto_tokenizer() -> Generator[MagicMock, None, None]:
    with patch.object(
        AutoTokenizer,
        "from_pretrained",
        return_value=MagicMock()
    ) as mock_auto_tokenizer:
        yield mock_auto_tokenizer


def test_download_hf_model(mock_auto_model: MagicMock, mock_auto_tokenizer: MagicMock):
    save_dir = "test_dir"
    model_name = "test_model"
    mock_auto_model_instance = mock_auto_model.return_value
    mock_auto_tokenizer_instance = mock_auto_tokenizer.return_value

    download_hf_model(save_dir, model_name)

    mock_auto_model.assert_called_once_with(model_name)
    mock_auto_tokenizer.assert_called_once_with(model_name)

    mock_auto_model_instance.save_pretrained.assert_called_once_with(save_dir)
    mock_auto_tokenizer_instance.save_pretrained.assert_called_once_with(save_dir)
