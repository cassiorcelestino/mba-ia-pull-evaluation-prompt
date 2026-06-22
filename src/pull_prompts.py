"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import load_yaml, save_yaml, check_env_vars, print_section_header

load_dotenv()


def serialize_prompt(prompt):
    """Converte o prompt puxado do Hub em um dicionário serializável."""
    return prompt.to_json()


def pull_prompts_from_langsmith():
    """Valida o ambiente e faz o pull do prompt do Hub."""
    required_vars = ["LANGSMITH_API_KEY", "LANGSMITH_PROJECT"]
    prompt_name = "leonanluppi/bug_to_user_story_v1"
    output_file = "prompts/bug_to_user_story_v1.yml"

    if not check_env_vars(required_vars):
        return False

    print_section_header("Preparando pull do prompt do LangSmith")
    print(f"🔗 Conectando ao Hub e fazendo pull de: {prompt_name}")

    try:
        prompt = hub.pull(prompt_name)
        print("✅ Prompt carregado com sucesso.")
        print(f"📦 Tipo do objeto retornado: {type(prompt).__name__}")

        prompt_data = serialize_prompt(prompt)
        print("🧩 Prompt convertido para estrutura serializável.")
        print(f"📄 Chaves principais: {list(prompt_data.keys())}")

        if save_yaml(prompt_data, output_file):
            print(f"💾 Prompt salvo com sucesso em: {output_file}")
            return prompt_data

        print("❌ Falha ao salvar o prompt localmente.")
        return False
    except Exception as e:
        print("❌ Falha ao fazer pull do prompt no LangSmith Hub.")
        print(f"🔎 Detalhe: {e}")
        print("💡 Dica: verifique se o prompt existe e se voce tem permissao para acessa-lo.")
        print("↩️ Tentando fallback com o arquivo local existente...")

        local_prompt = load_yaml(output_file)
        if local_prompt:
            print(f"✅ Fallback carregado com sucesso de: {output_file}")
            return local_prompt

        print("❌ Fallback local indisponivel. Nao foi possivel carregar o prompt v1.")
        return False


def main():
    """Função principal"""
    prompt_data = pull_prompts_from_langsmith()

    if prompt_data:
        print("✅ Etapa de carga do prompt v1 concluida.")
        print("➡️ Proximo micro-passo: analisar o v1 e criar o v2 otimizado.")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
