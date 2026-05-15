import os
import time
import requests
from dotenv import load_dotenv

load_dotenv() # Carrega variáveis do arquivo .env utilizados pela conexão com Ollama

class LLMClient:
    def __init__(self): 
        self.host = os.getenv("OLLAMA_HOST", "https://ollama.com").rstrip("/") # Determina o host do modelo
        self.model = os.getenv("OLLAMA_MODEL", "gpt-oss:120b") 
        self.timeout = int(os.getenv("OLLAMA_TIMEOUT", "60")) # Determina tempo de expiração - 60s
        self.max_retries = int(os.getenv("OLLAMA_MAX_RETRIES", "3")) # Determina número máximo de tentativas - 3x

    def chat(self, prompt, system="", temp=0.3, max_tokens=500): 
        
        """
                Envia mensagens ao modelo via endpoint /api/chat do Ollama.

                Parâmetros esperados:
                - prompt:
                    Prompt final gerado pelo prompt_builder.py
                    e organizado pelas técnicas em techniques.py

                - system:
                    System prompt utilizado no Role Prompting carregado  na técnica de Role Prompting

                - temp:
                    Temperatura da inferência.
                    Controla criatividade/variabilidade da resposta.

                - max_tokens:
                    Quantidade máxima de tokens gerados pelo modelo.

                Retorno:
                dict contendo:
                - resposta do modelo
                - tokens do prompt
                - tokens da resposta
                - tempo total da inferência
        """


        if not prompt or not prompt.strip():
            raise ValueError("O prompt não pode ser vazio.")
        
        url = f"{self.host}/api/chat"

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system}, 
                {"role": "user", "content": prompt} 
            ],
            "options": {
                "temperature": temp,
                "num_predict": max_tokens
            },
            "stream": False # Retorna resposta do modelo de uma vez, sem estar separada token a token
        }

        last_error = None # Armazena o último erro ocorrido durante retries
        start_time = time.time() # Começa a cronometrar tempo de operação do modelo

        for attempt in range(self.max_retries): # Tenta o máximo número de vezes fazer o request (3x)
            try:
                response = requests.post(url, json=payload, timeout=self.timeout) # Envia o prompt final montado pelo prompt_builder para o modelo via Ollama
                response.raise_for_status()
                data = response.json()

                tempo_ms = round((time.time() - start_time) * 1000) # Calcula tempo de resposta da LLM

                return {
                    "resposta": data["message"]["content"].strip(),
                    "tokens_prompt": data.get("prompt_eval_count", 0),
                    "tokens_resposta": data.get("eval_count", 0),
                    "tempo_ms": tempo_ms
                } 

            except requests.exceptions.Timeout as e:
                last_error = f"Timeout na tentativa {attempt + 1}: {e}" #Timeout da API

            except requests.exceptions.RequestException as e:
                last_error = f"Erro de requisição na tentativa {attempt + 1}: {e}" # Erros HTTP ou de requisição
            except (KeyError, ValueError) as e:
                last_error = f"Erro ao interpretar resposta da API: {e}" # Estrutura inesperada do JSON
                break

            time.sleep(2 ** attempt) # Retry Exponencial: mais tentavias --> maior espera para a próxima tentativa

        return { # Retorno padronizado em caso de falha total
            "resposta": f"Erro: {last_error}",
            "tokens_prompt": 0,
            "tokens_resposta": 0,
            "tempo_ms": round((time.time() - start_time) * 1000)
        }