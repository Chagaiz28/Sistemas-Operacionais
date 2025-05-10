import threading
import time
import random

hino_nacional = {
    1: "Ouviram do Ipiranga as margens plácidas",
    2: "De um povo heroico o brado retumbante,",
    3: "E o sol da liberdade, em raios fúlgidos,",
    4: "Brilhou no céu da Pátria nesse instante.",
    5: "Se o penhor dessa igualdade",
    6: "Conseguimos conquistar com braço forte,",
    7: "Em teu seio, ó liberdade,",
    8: "Desafia o nosso peito a própria morte!",
    9: "Ó Pátria amada,",
    10: "Idolatrada,",
    11: "Salve! Salve!",
    12: "Brasil, um sonho intenso, um raio vívido",
    13: "De amor e de esperança à terra desce,",
    14: "Se em teu formoso céu, risonho e límpido,",
    15: "A imagem do Cruzeiro resplandece.",
    16: "Gigante pela própria natureza,",
    17: "És belo, és forte, impávido colosso,",
    18: "E o teu futuro espelha essa grandeza.",
    19: "Terra adorada",
    20: "Entre outras mil,",
    21: "És tu, Brasil,",
    22: "Ó Pátria amada!",
    23: "Dos filhos deste solo és mãe gentil,",
    24: "Pátria amada,",
    25: "Brasil!"
}


lock = threading.Lock()

class Processo:
    def __init__(self, id):
        self.id = id
        self.linha = hino_nacional[id]

def escrever_palavras(process, uso_lock, arquivo_saida):
    palavras = process.linha.split()
    if uso_lock:
        with lock:
            with open(arquivo_saida, 'a', encoding='utf-8') as f:
                for palavra in palavras:
                    f.write(f"{palavra} ")
                    time.sleep(random.uniform(0.05, 0.15))
                f.write("\n")
    else:
        with open(arquivo_saida, 'a', encoding='utf-8') as f:
            for palavra in palavras:
                f.write(f"{palavra} ")
                time.sleep(random.uniform(0.05, 0.15))
            f.write("\n")

def simular(nome_algoritmo, uso_lock, arquivo_saida):
    print(f"\n--- {nome_algoritmo} ---\n")
    
    open(arquivo_saida, 'w', encoding='utf-8').close()
    
    processos = [Processo(id=i) for i in hino_nacional.keys()]
    
    threads = []
    for processo in processos:
        t = threading.Thread(target=escrever_palavras, args=(processo, uso_lock, arquivo_saida))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

def main():
    simular("Sem Lock (com race condition)", uso_lock=False, arquivo_saida="sem_lock.txt")
    simular("Com Lock (sincronizado)", uso_lock=True, arquivo_saida="com_lock.txt")

main()
