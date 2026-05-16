import json
import os
from src.tasks import TAREFAS
from src.prompt_builder import montar_prompt

def run_tests():
    print("--- INICIANDO TESTES LOCAIS ---")
    
    caminho_json = os.path.join("data", "inputs.json")
    
    try:
        with open(caminho_json, "r", encoding="utf-8") as f:
            inputs_data = json.load(f)
        print("1. JSON carregado com sucesso. Nao ha erros de sintaxe.")
    except Exception as e:
        print(f"ERRO CRITICO: Falha ao ler inputs.json: {e}")
        return

    for tarefa in TAREFAS:
        nome_tarefa = tarefa.get("nome")
        print(f"\nTestando integracao da tarefa: {nome_tarefa}")
        
        if nome_tarefa not in inputs_data:
            print(f"ERRO: Tarefa '{nome_tarefa}' nao encontrada no inputs.json!")
            continue
            
        inputs_tarefa = inputs_data[nome_tarefa]
        if len(inputs_tarefa) < 5:
            print(f"AVISO: A tarefa '{nome_tarefa}' tem menos de 5 inputs reais.")
            
        primeiro_input = inputs_tarefa[0].get("input", "")
        
        try:
            prompt_teste = montar_prompt(
                instrucao=tarefa.get("instrucao"),
                contexto="Contexto de teste automatizado",
                input_dados=primeiro_input,
                formato_output=tarefa.get("formato_output")
            )
            print("2. Prompt Builder gerou o texto corretamente:")
            print("-" * 40)
            print(prompt_teste)
            print("-" * 40)
        except Exception as e:
            print(f"ERRO no prompt_builder para a tarefa {nome_tarefa}: {e}")

if __name__ == "__main__":
    run_tests()