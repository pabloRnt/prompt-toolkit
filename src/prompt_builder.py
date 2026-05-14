# --- FUNÇÃO PARA CONSTRUÇÃO DO PROMPT ---

"""
Responsável pela construção e modificação de prompts.

Fluxo arquitetural:
tasks.py
    ↓
techniques.py seleciona técnica
    ↓
prompt_builder.py monta o prompt
    ↓
llm_client.py envia ao modelo

Este módulo NÃO:
- envia requests ao modelo;
- executa inferência;
- avalia respostas;
- acessa diretamente o Ollama.

Sua responsabilidade é apenas estruturar prompts.

Essas funções são utilizadas principalmente pelo módulo techniques.py para construir
prompts específicos de cada técnica.
"""

def montar_prompt(instrucao, contexto, input_dados, formato_output):

    componentes = {
        "instrucao": instrucao,
        "contexto": contexto,
        "input_dados": input_dados,
        "formato_output": formato_output
    }

    for nome, valor in componentes.items(): # Verifica se uma parte do prompt está faltando
        if not valor or not str(valor).strip():
            raise ValueError(f"O componente '{nome}' não pode ser vazio.")

    prompt = f""" 
INSTRUÇÃO:
{instrucao}

CONTEXTO:
{contexto}

DADOS:
{input_dados}

FORMATO DA RESPOSTA:
{formato_output}
""".strip()
# Caso não esteja faltando nenhum componente do prompt, constrói-se o prompt delimitando o que é intrução e o que é dado

    return prompt

# --- FEW-SHOT ---

def adicionar_exemplos(prompt, exemplos): # Recebe exemplos previamente carregados pela técnica Few-Shot para adicioná-los ao prompt final

    """
    Adiciona exemplos Few-Shot ao prompt base.

    Parâmetros:
    - prompt: prompt já estruturado
    - exemplos: lista de exemplos input/output

    Retorna:
    - prompt final contendo exemplos Few-Shot
    """

    if not exemplos:
        raise ValueError("A lista de exemplos não pode ser vazia.") # Se faltar exemplos, retorna erro

    bloco_exemplos = "\n\nEXEMPLOS:\n"

    for exemplo in exemplos:

        entrada = exemplo.get("input")
        saida = exemplo.get("output") 

        # Cada exemplo deve seguir o formato:
        # {
        #   "input": "...",
        #   "output": "..."
        # }

        if not entrada or not saida:
            raise ValueError("Cada exemplo deve conter 'input' e 'output'.") # Se faltar entrada ou saída, retorna erro

        bloco_exemplos += f"""
Input: {entrada}
Output: {saida}
"""

    return prompt + bloco_exemplos # Adiciona exemplos Few-Shot ao prompt final

# --- CoT ---

def adicionar_cot(prompt, passos):

    if not passos:
        raise ValueError("A lista de passos não pode ser vazia.") # A técnica CoT precisa de pelo menos um passo de raciocínio

    bloco_cot = "\n\nRACIOCINE PASSO A PASSO:\n"

    for i, passo in enumerate(passos, start=1):
        bloco_cot += f"{i}. {passo}\n" # Estrutura os passos sequencialmente para induzir raciocínio passo a passo no modelo

    return prompt + bloco_cot # Adiciona o CoT no prompt 