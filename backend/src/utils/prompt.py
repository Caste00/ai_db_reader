from pathlib import Path
import yaml

PROMPTS_PATH = Path(__file__).resolve().parent.parent / "config" / "prompts.yaml"


def _load_prompts(path: Path = PROMPTS_PATH) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


_PROMPTS = _load_prompts()


def get_prompt(key: str, **kwargs) -> str:
    node = _PROMPTS
    for part in key.split("."):
        node = node[part]
    return node.format(**kwargs)