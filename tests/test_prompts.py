"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
import re
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_v2_prompt_data():
    """Retorna os dados do prompt v2 alvo da entrega."""
    prompts = load_prompts("prompts/bug_to_user_story_v2.yml")
    assert "bug_to_user_story_v2" in prompts, "Prompt bug_to_user_story_v2 nao encontrado no YAML"
    return prompts["bug_to_user_story_v2"]

class TestPrompts:
    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        prompt = get_v2_prompt_data()
        assert "system_prompt" in prompt
        assert isinstance(prompt["system_prompt"], str)
        assert prompt["system_prompt"].strip() != ""

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        prompt = get_v2_prompt_data()
        system_prompt = prompt.get("system_prompt", "").lower()

        role_markers = [
            "você é",
            "analista",
            "product manager",
            "persona",
        ]

        assert any(marker in system_prompt for marker in role_markers)

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        prompt = get_v2_prompt_data()
        system_prompt = prompt.get("system_prompt", "").lower()

        format_markers = [
            "formato",
            "user story",
            "**título",
            "**como**",
            "critérios de aceite",
        ]

        assert any(marker in system_prompt for marker in format_markers)

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        prompt = get_v2_prompt_data()
        system_prompt = prompt.get("system_prompt", "").lower()

        few_shot_markers = [
            "few-shot",
            "exemplo",
            "relato:",
            "user story:",
        ]

        assert any(marker in system_prompt for marker in few_shot_markers)

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        prompt = get_v2_prompt_data()
        serialized = yaml.dump(prompt, allow_unicode=True).lower()
        # Evita falso positivo com palavras como "todos".
        assert "[todo]" not in serialized
        assert re.search(r"\btodo\b", serialized) is None

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        prompt = get_v2_prompt_data()
        techniques = prompt.get("techniques_applied", [])

        assert isinstance(techniques, list)
        assert len(techniques) >= 2

    def test_prompt_structure_valid(self):
        """Validação estrutural extra usando utilitário do projeto."""
        prompt = get_v2_prompt_data()
        is_valid, errors = validate_prompt_structure(prompt)
        assert is_valid, f"Estrutura invalida: {errors}"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])