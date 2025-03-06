import faiss
import pickle
from unittest.mock import patch, mock_open
from src.utils.file_utils import read_embeddings, read_obj


def test_read_embeddings():
    mock_index = faiss.IndexFlatIP(128)

    with patch.object(faiss, "read_index", return_value=mock_index) as mock_read_index:
        result = read_embeddings("fake_path")
        mock_read_index.assert_called_once_with("fake_path")
        assert result == mock_index


def test_read_obj():
    dummy_data = {"key": "value"}

    with patch("builtins.open", mock_open(read_data=pickle.dumps(dummy_data))):
        with patch.object(pickle, "load", return_value=dummy_data) as mock_pickle_load:
            result = read_obj("fake_path")
            mock_pickle_load.assert_called_once()
            assert result == dummy_data
