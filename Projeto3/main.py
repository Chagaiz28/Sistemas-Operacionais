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

class Process:
    def __init__(self, pid, line):
        self.pid = pid
        self.line = line
        self.burst = len(line)
        self.arrival = 0
        self.start = 0
        self.finish = 0
        self.waiting = 0
        self.turnaround = 0

class CPUScheduler:
    def __init__(self, algorithm='FCFS'):
        self.algorithm = algorithm
        self.queue = []

    def load(self, processes):
        self.queue = processes.copy()

    def schedule_order(self):
        if self.algorithm == 'FCFS':
            return sorted(self.queue, key=lambda p: p.pid)
        elif self.algorithm == 'PS':
            return sorted(self.queue, key=lambda p: p.burst, reverse=True)
        elif self.algorithm == 'SJF':
            return sorted(self.queue, key=lambda p: p.burst)
        else:
            raise ValueError("Algoritmo não suportado.")

    def compute_metrics(self):
        time_cursor = 0
        order = self.schedule_order()
        for p in order:
            p.start = max(time_cursor, p.arrival)
            p.finish = p.start + p.burst
            p.waiting = p.start - p.arrival
            p.turnaround = p.finish - p.arrival
            time_cursor = p.finish

        total_wait = sum(p.waiting for p in order)
        total_turn = sum(p.turnaround for p in order)
        n = len(order)
        avg_wait = total_wait / n
        avg_turn = total_turn / n
        return avg_wait, avg_turn

def comparar(*algorithms):
    resultados = {}

    for algoritmo in algorithms:
        processos = [Process(pid, line) for pid, line in hino_nacional.items()]
        escalonador = CPUScheduler(algoritmo)
        escalonador.load(processos)
        tempo_espera_medio, tempo_total_medio = escalonador.compute_metrics()
        resultados[algoritmo] = (tempo_espera_medio, tempo_total_medio)

    print("\nComparação de algoritmos de escalonamento:")
    print("-" * 40)
    for algoritmo, (espera, turnaround) in resultados.items():
        print(f"{algoritmo:<10} | Waiting: {espera:>6.2f} | Turnaround: {turnaround:>6.2f}")
    print("-" * 40)
    
comparar('FCFS', 'PS', 'SJF')
