# src/tasks.py

TAREFAS = [
    {
        "nome": "classificacao_urgencia",
        "tipo": "classificacao",
        "instrucao": "Classifique a urgencia do ticket de suporte de TI como ALTA, MEDIA ou BAIXA.",
        "formato_output": "Responda APENAS com a classificacao.",
        "exemplos_fewshot": [
            {
                "input": "O banco de dados de producao caiu e o sistema de vendas esta travado.", 
                "output": "ALTA"
            },
            {
                "input": "Gostaria de solicitar a instalacao do pacote Office na minha maquina.", 
                "output": "BAIXA"
            }
        ],
        "passos_cot": [
            "Identifique o escopo do problema relatado e quantos usuarios sao afetados.",
            "Avalie se ha impacto direto em producao ou bloqueio critico de trabalho.",
            "Compare a gravidade com a matriz de risco e determine a classificacao final."
        ],
        "persona": "coordenador_ti"
    },
    {
        "nome": "extracao_entidades_erro",
        "tipo": "extracao",
        "instrucao": "Extraia o codigo de erro e o microsservico afetado a partir da mensagem de log.",
        "formato_output": "Responda em formato JSON com as chaves 'codigo_erro' e 'servico'.",
        "exemplos_fewshot": [
            {
                "input": "2026-05-15 10:00 [ERROR] auth-service falhou com timeout. Code: 504.", 
                "output": '{"codigo_erro": "504", "servico": "auth-service"}'
            },
            {
                "input": "Crash no payment-gateway. NullPointerException detected (Error 500).", 
                "output": '{"codigo_erro": "500", "servico": "payment-gateway"}'
            }
        ],
        "passos_cot": [
            "Leia a mensagem de log atentamente.",
            "Localize padroes de codigos de erro HTTP ou codigos internos.",
            "Identifique o nome do servico, modulo ou aplicacao mencionada.",
            "Formate os dados extraidos estritamente como um JSON."
        ],
        "persona": "engenheiro_devops"
    },
    {
        "nome": "geracao_resposta_cliente",
        "tipo": "geracao",
        "instrucao": "Gere uma resposta curta, empatica e profissional para o usuario, informando que o time tecnico ja esta atuando no problema.",
        "formato_output": "Texto claro e profissional, com no maximo 3 frases.",
        "exemplos_fewshot": [
            {
                "input": "Meu acesso ao e-mail foi bloqueado do nada, estou perdendo reunioes!", 
                "output": "Ola! Entendemos a urgencia do seu bloqueio de e-mail e os transtornos causados. Nossa equipe tecnica ja priorizou seu caso e esta trabalhando para restaurar o acesso o mais rapido possivel."
            }
        ],
        "passos_cot": [
            "Analise o tom e a dor do usuario no input.",
            "Crie uma primeira frase que demonstre empatia e confirme o recebimento do problema.",
            "Adicione uma frase informando que a equipe tecnica ja esta analisando a situacao.",
            "Encerre garantindo um breve retorno."
        ],
        "persona": "agente_suporte"
    }
]