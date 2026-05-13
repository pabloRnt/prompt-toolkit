# src/llm_client.py
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
        self.model = os.getenv("OLLAMA_MODEL", "gpt-oss:120b")
        self.timeout = int(os.getenv("OLLAMA_TIMEOUT", "60"))
        self.max_retries = int(os.getenv("OLLAMA_MAX_RETRIES", "3"))

    def chat(self, prompt, system="", temp=0.3, max_tokens=500):
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
            "stream": False
        }

        last_error = None
        start_time = time.time()

        for attempt in range(self.max_retries):
            try:
                response = requests.post(url, json=payload, timeout=self.timeout)
                response.raise_for_status()
                data = response.json()

                tempo_ms = round((time.time() - start_time) * 1000)

                return {
                    "resposta": data["message"]["content"].strip(),
                    "tokens_prompt": data.get("prompt_eval_count", 0),
                    "tokens_resposta": data.get("eval_count", 0),
                    "tempo_ms": tempo_ms
                }

            except requests.exceptions.Timeout as e:
                last_error = f"Timeout na tentativa {attempt + 1}: {e}"

            except requests.exceptions.RequestException as e:
                last_error = f"Erro de requisição na tentativa {attempt + 1}: {e}"

            except (KeyError, ValueError) as e:
                last_error = f"Erro ao interpretar resposta da API: {e}"
                break

            time.sleep(1)

        return {
            "resposta": f"Erro: {last_error}",
            "tokens_prompt": 0,
            "tokens_resposta": 0,
            "tempo_ms": round((time.time() - start_time) * 1000)
        }