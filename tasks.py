from celery_app import celery_app
import time

@celery_app.task(bind=True)
def somar(self, a, b):
    time.sleep(3)
    return a + b

@celery_app.task(bind=True)
def fatorial(self, n):
    time.sleep(3)
    if n < 0:
        raise ValueError("Número negativo não permitido!")
    
    resultado = 1

    for i in range(2, n + 1):
        resultado *= i
    
    return resultado

# 1 - Vamos criar algumas tarefas
# 2 - Vamos rodar essas tarefas em background usando o Celery
# 3 - Vamos jogar essas tarefas para o Redis usando-o como sistema de fila