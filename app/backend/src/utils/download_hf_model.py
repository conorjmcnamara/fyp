from transformers import AutoModel, AutoTokenizer


def download_hf_model(save_dir: str, model_name: str) -> None:
    model = AutoModel.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    model.save_pretrained(save_dir)
    tokenizer.save_pretrained(save_dir)
    print(f"Model and Tokenizer saved to: {save_dir}")


if __name__ == "__main__":
    download_hf_model("data/models/specter2/", "allenai/specter2_base")
