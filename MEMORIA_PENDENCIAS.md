# Memoria de Pendencias e Decisoes

## Estado Atual
- Durante construcao, a avaliacao esta configurada para usar Ollama por padrao no modo de teste.
- Objetivo: economizar quota gratuita de Gemini/OpenAI enquanto refinamos prompt e fluxo.

## Enunciado (resumo salvo)
- Pull do prompt ruim no LangSmith Hub.
- Otimizar prompt com few-shot obrigatorio + tecnicas avancadas.
- Push do prompt otimizado para o Hub.
- Avaliar com 5 metricas (helpfulness, correctness, f1_score, clarity, precision).
- Meta final: >= 0.8 em todas as metricas.
- Entregaveis esperados: implementacoes de pull/push, prompt v2, testes e README.

## Decisoes de Teste
- Modo de construcao: EVAL_BUILD_MODE=1
- Provider de teste padrao: ollama
- Modelo de teste padrao: qwen2.5:3b (mais rapido)
- Amostra padrao para teste rapido: EVAL_MAX_EXAMPLES=1
- Timeout de inferencia por exemplo: EVAL_INFERENCE_TIMEOUT_SEC
- Limite de geracao no Ollama: OLLAMA_NUM_PREDICT

## Pendencias Principais
- Corrigir pull oficial no Hub publico conforme enunciado.
- Corrigir push oficial no Hub publico conforme enunciado.
- Revisar configuracao de workspace/handle no LangSmith para habilitar nome publico.
- Revalidar fluxo oficial completo depois: push -> pull -> evaluate com metricas oficiais.
- Consolidar README da entrega.

## Item 5 (Testes) - Status
- tests/test_prompts.py implementado com os 6 testes obrigatorios do enunciado.
- Foi adicionado 1 teste extra de estrutura (test_prompt_structure_valid) para seguranca.
- Validacao executada com sucesso: `python -m pytest tests/test_prompts.py -q` -> 7 passed.

## Problemas Conhecidos
- Prompt oficial com username pode retornar not found no Hub publico.
- Fallback privado funciona (bug_to_user_story_v2), mas nao atende plenamente o requisito de publicacao oficial.
- Quota gratuita do Gemini estourou em tentativas anteriores.
- Ollama 7b e 3b podem ficar lentos sem timeout; por isso foi adicionado timeout por exemplo no evaluate.

## Proximo Passo Planejado
- Fechar primeiro o fluxo de desenvolvimento em modo economico (Ollama).
- Depois voltar para a trilha oficial do enunciado e resolver publicacao/pull no Hub.

## Alteracoes tecnicas ja aplicadas
- Suporte a provider ollama no projeto (utils + requirements).
- evaluate em modo construcao forca provider/modelo de teste local.
- evaluate em modo construcao usa prompt local: prompts/bug_to_user_story_v2.yml.
- evaluate em modo construcao evita tentativa de pull publico para nao poluir log.
- evaluate possui timeout por exemplo para evitar travamento.
- metricas locais aproximadas ativadas no modo construcao para reduzir consumo de API.

## Inventario de caminhos alternativos ativos
- EVAL_BUILD_MODE=1:
	Usa score local aproximado (nao oficial) para iteracao rapida.
- EVAL_FORCE_LOCAL_PROMPT=1:
	Usa prompt local no modo oficial para validar sem depender de push/pull.
- TEST_LLM_PROVIDER / TEST_LLM_MODEL / TEST_EVAL_MODEL:
	Sobrescrevem provider/modelos em modo de construcao.
- EVAL_INFERENCE_TIMEOUT_SEC:
	Evita travas por inferencia longa em modelos locais.
- EVAL_MAX_EXAMPLES:
	Permite amostragem pequena durante desenvolvimento.
- EVAL_DEBUG=1:
	Exibe pergunta/resposta/referencia por exemplo para diagnostico de precision/clarity.
- OLLAMA_NUM_PREDICT:
	Limita tokens para reduzir latencia.
- Fallback de parse de JSON em metrics.py:
	Recupera score/precision/recall de respostas truncadas.

## Plano de limpeza para entrega final
- Manter somente fluxo oficial exigido no enunciado para execucao final.
- Revisar/remover flags de override local se nao forem necessarias na entrega.
- Garantir push/pull oficial no Hub com nome publico valido.
- Reexecutar avaliacao final com configuracao oficial e registrar evidencias no README.

## Observacao adicionada em 2026-06-22
- Foi reportado erro em outro chat/sessao.
- Este chat nao tem acesso automatico ao historico completo de outras conversas.
- Acao pendente: colar aqui o log completo do erro (stack trace + comando executado) para registro definitivo e diagnostico.

## Erro de infraestrutura do Chat (2026-06-22)
- Mensagem: Request Failed: 400 - Invalid 'input[3].id': 'thinking_0'. Expected an ID that begins with 'rs'.
- Copilot Request id: 92956993-e1a9-43cf-b0a4-42927040cb7d
- GH Request Id: C085:331A9:2349242:28BB565:6A38B671
- Diagnostico: falha de protocolo/infra do servico de chat (nao relacionada ao codigo do projeto).
- Mitigacao pratica: abrir nova mensagem/chat e repetir a solicitacao; se persistir, manter os IDs para suporte e seguir pelo terminal local no projeto.

## Ponto atual para retomada (fim do dia - 2026-06-22)
- Pedido do usuario: registrar o passo atual e encerrar para continuar amanha.
- Estado tecnico atual: execucao recente do evaluate com 1 exemplo concluiu com sucesso (exit code 0) usando Ollama local.
- Ultimo bloqueio relevante: erro de infraestrutura no Copilot Chat (HTTP 400) registrado acima, sem impacto direto no codigo do projeto.
- Arquivo de memoria atualizado com sucesso nesta sessao.

## Checklist rapido para amanha
- Rodar evaluate com 3 exemplos para diagnostico mais representativo.
- Coletar metricas atuais por prompt e identificar gargalo principal (helpfulness/correctness/f1/clarity/precision).
- Ajustar prompt v2 com foco no gargalo e repetir ciclo de avaliacao.
