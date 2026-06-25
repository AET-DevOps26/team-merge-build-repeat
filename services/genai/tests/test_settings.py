from __future__ import annotations

from genai_service.settings import load_settings


def test_load_settings_reads_openai_api_key_file(monkeypatch, tmp_path) -> None:
    secret_file = tmp_path / "logos_key"
    secret_file.write_text("lg-test\n", encoding="utf-8")

    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY_FILE", str(secret_file))

    settings = load_settings()

    assert settings.openai_api_key == "lg-test"


def test_load_settings_prefers_openai_api_key_env(monkeypatch, tmp_path) -> None:
    secret_file = tmp_path / "logos_key"
    secret_file.write_text("lg-file\n", encoding="utf-8")

    monkeypatch.setenv("OPENAI_API_KEY", "lg-env")
    monkeypatch.setenv("OPENAI_API_KEY_FILE", str(secret_file))

    settings = load_settings()

    assert settings.openai_api_key == "lg-env"
