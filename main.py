import threading
import time
import random

# Lock para sincronização
lock = threading.Lock()

# Trechos do Hino Nacional Brasileiro (só um pedaço para exemplo)
hino_nacional = [
    "Ouviram do Ipiranga as margens plácidas",
    "De um povo heroico o brado retumbante,",
    "E o sol da liberdade, em raios fúlgidos,",
    "Brilhou no céu da Pátria nesse instante.",
    "Se o penhor dessa igualdade",
    "Conseguimos conquistar com braço forte,",
    "Em teu seio, ó liberdade,",
    "Desafia o nosso peito a própria morte!"
]

# Cada processo terá essas informações
class Processo:
    def __init__(self, id, prioridade):
        self.id = id
        self.prioridade = prioridade
        self.chegada = time.time()  # Momento de criação

def escrever_hino_palavra_por_palavra(process, uso_lock, arquivo):
    palavras = hino_nacional[process.id].split()  # Divide a linha em palavras
    if uso_lock:
        with lock:  # Protege toda a operação de escrita
            with open(arquivo, 'a', encoding='utf-8') as f:
                for palavra in palavras:
                    f.write(palavra + " ")
                    time.sleep(random.uniform(0.05, 0.15))  # Pequena pausa entre palavras
                f.write("\n")  # Adiciona quebra de linha após a linha completa
    else:
        with open(arquivo, 'a', encoding='utf-8') as f:
            for palavra in palavras:
                f.write(palavra + " ")
                time.sleep(random.uniform(0.05, 0.15))  # Pequena pausa entre palavras
            f.write("\n")  # Adiciona quebra de linha após a linha completa

# Algoritmo de Escalonamento FCFS
def escalonamento_fcfs(processos):
    return sorted(processos, key=lambda p: p.chegada)

# Algoritmo de Escalonamento por Prioridade
def escalonamento_prioridade(processos):
    return sorted(processos, key=lambda p: p.prioridade)

def simular(nome_algoritmo, escalonador, uso_lock, arquivo_saida):
    print(f"\n--- Simulação usando {nome_algoritmo} {'com' if uso_lock else 'sem'} sincronização ---\n")
    
    # Cria processos para cada linha do hino
    processos = [Processo(id=i, prioridade=random.randint(1, 10)) for i in range(len(hino_nacional))]

    # Limpa o arquivo antes de começar
    open(arquivo_saida, 'w', encoding='utf-8').close()

    # Escalona os processos
    processos_ordenados = escalonador(processos)

    threads = []
    for processo in processos_ordenados:
        t = threading.Thread(target=escrever_hino_palavra_por_palavra, args=(processo, uso_lock, arquivo_saida))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

def main():
    simular("FCFS", escalonamento_fcfs, uso_lock=False, arquivo_saida="hino_fcfs_sem_lock.txt")
    simular("FCFS", escalonamento_fcfs, uso_lock=True, arquivo_saida="hino_fcfs_com_lock.txt")
    simular("Priority Scheduling", escalonamento_prioridade, uso_lock=False, arquivo_saida="hino_priority_sem_lock.txt")
    simular("Priority Scheduling", escalonamento_prioridade, uso_lock=True, arquivo_saida="hino_priority_com_lock.txt")

if __name__ == "__main__":
    main()
