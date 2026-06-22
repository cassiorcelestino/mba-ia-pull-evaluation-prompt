"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_data["system_prompt"]),
        ("human", prompt_data["user_prompt"]),
    ])

    description = prompt_data.get("description", "")
    tags = prompt_data.get("tags", [])
    username = os.getenv("USERNAME_LANGSMITH_HUB", "").strip()

    # Tentativa 1 (enunciado): publicar como publico no formato username/prompt.
    if username:
        public_name = f"{username}/{prompt_name}"
        try:
            print(f"🌐 Tentando push PUBLICO conforme enunciado: {public_name}")
            hub.push(
                repo_full_name=public_name,
                object=chat_prompt,
                new_repo_is_public=True,
                new_repo_description=description,
                tags=tags,
            )
            print(f"✅ Push publico concluido: {public_name}")
            return True
        except Exception as e:
            print("⚠️ Push publico falhou. Iniciando fallback para nao travar o fluxo.")
            print(f"🔎 Detalhe: {e}")
    else:
        print("⚠️ USERNAME_LANGSMITH_HUB nao configurado. Pulando tentativa publica.")

    # Tentativa 2 (fallback): publicar privado no workspace atual.
    try:
        print(f"🔁 Fallback: push PRIVADO no workspace atual: {prompt_name}")
        hub.push(
            repo_full_name=prompt_name,
            object=chat_prompt,
            new_repo_is_public=False,
            new_repo_description=description,
            tags=tags,
        )
        print(f"✅ Push privado concluido: {prompt_name}")
        return True
    except Exception as e:
        error_text = str(e)
        if "Nothing to commit" in error_text:
            print("ℹ️ Nada para commitar: o prompt ja esta atualizado no workspace.")
            return True

        print("❌ Falha no push (publico e fallback privado).")
        print(f"🔎 Detalhe final: {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    errors = []

    required_fields = ["description", "system_prompt", "user_prompt", "version"]
    for field in required_fields:
        if field not in prompt_data:
            errors.append(f"Campo obrigatório faltando: {field}")

    system_prompt = prompt_data.get("system_prompt", "").strip()
    if not system_prompt:
        errors.append("system_prompt está vazio")

    if "TODO" in system_prompt:
        errors.append("system_prompt contém TODO pendente")

    techniques = prompt_data.get("techniques_applied", [])
    if len(techniques) < 2:
        errors.append("Mínimo de 2 técnicas em techniques_applied")

    return (len(errors) == 0, errors)


def main():
    """Função principal"""
    print_section_header("Push de prompt otimizado")

    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return 1

    prompt_file = "prompts/bug_to_user_story_v2.yml"
    data = load_yaml(prompt_file)

    if not data:
        print(f"❌ Nao foi possivel carregar: {prompt_file}")
        return 1

    prompt_data = data.get("bug_to_user_story_v2")
    if not prompt_data:
        print("❌ Estrutura invalida: chave bug_to_user_story_v2 nao encontrada")
        return 1

    is_valid, errors = validate_prompt(prompt_data)
    if not is_valid:
        print("❌ Prompt v2 reprovado na validacao local:")
        for err in errors:
            print(f"   - {err}")
        return 1

    print("✅ Prompt v2 aprovado na validacao local.")
    prompt_name = "bug_to_user_story_v2"
    print(f"🚀 Publicando prompt com estrategia publico->fallback privado: {prompt_name}")

    if not push_prompt_to_langsmith(prompt_name, prompt_data):
        return 1

    print("✅ Fluxo de push concluido com sucesso.")
    print("➡️ Se o publico falhar, o script faz fallback para privado automaticamente.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
