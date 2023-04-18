import sys
import time
import threading
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog

#Criando uma classe que representa uma janela de saída de texto
class PrintWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Output")
        self.geometry("600x400")
        self.text = tk.Text(self)
        self.text.pack(fill=tk.BOTH, expand=True)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        sys.stdout = self

    # Método que escreve na janela de saída de texto
    def write(self, message):
        self.text.insert(tk.END, message)
        self.text.see(tk.END)

    def flush(self):
        pass

    # Método que define o comportamento ao fechar a janela
    def on_close(self):
        self.parent.destroy()

#Função que realiza a soma sequencial de uma lista de números
def sequential_sum(numbers):
    start_time = time.time()
    total = 0
    for num in numbers:
        total += num
    end_time = time.time()
    print(f"Tempo de execução sequencial: {end_time - start_time}")
    print(f"Soma dos números de 1 a {len(numbers)}: {total}", file=sys.stdout)
    return total, end_time - start_time

#Função que realiza a soma paralela de uma lista de números utilizando múltiplas threads
def threaded_sum(numbers, num_threads):
    start_time = time.time()
    chunk_size = len(numbers) // num_threads
    threads = []
    results = []

    # Criando e iniciando as threads
    for i in range(num_threads):
        start = i * chunk_size
        end = start + chunk_size if i != num_threads - 1 else len(numbers)
        chunk = numbers[start:end]
        #Criando a thread
        thread = threading.Thread(target=lambda r, c: r.append(sum(c)), args=(results, chunk))
        print(f"Thread {i+1} iniciada para a soma de {len(chunk)} números", file=sys.stdout)
        threads.append(thread)
        thread.start()

    # Aguardando o término de todas as threads
    for i, thread in enumerate(threads):
        thread.join()
        print(f"Thread {i+1} finalizada", file=sys.stdout)

    end_time = time.time()
    print(f"Soma paralela de {len(numbers)} números com {num_threads} threads: {sum(results)}")
    print(f"Tempo de execução com {num_threads} threads: {end_time - start_time}", file=sys.stdout)
    return sum(results), end_time - start_time

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    # Criando uma janela de diálogo para solicitar o valor máximo
    max_number = tk.simpledialog.askinteger("Valor máximo", "Digite o valor máximo para a soma:")

    if max_number is not None:
        numbers = list(range(1, max_number + 1))
        num_threads_list = [1, 2, 4, 8, 16, 32]

        print_window = PrintWindow(root)
        print_window.grab_set()

        print("Execução iniciada.", file=sys.stdout)

        # Executando a soma sequencial e a soma em paralelo com diferentes números de threads
        seq_total, seq_time = sequential_sum(numbers)
        threaded_times = []

        for num_threads in num_threads_list:
            threaded_total, threaded_time = threaded_sum(numbers, num_threads)
            threaded_times.append(threaded_time)

        # Criando gráfico de barras
        x = ["Sequencial"] + [f"{n} threads" for n in num_threads_list]
        y = [seq_time] + threaded_times
        plt.bar(x, y, color=["blue", "orange", "green", "red", "purple", "brown"])
        plt.ylim(0, max(y) * 1.1)
        plt.ylabel("Tempo de execução (s)")
        plt.title("Tempo de execução para diferentes números de threads")

        # Adicionando valores das barras
        for i, v in enumerate(y):
            plt.text(i, v, f"{v:.2f}", ha='center', va='bottom')

        plt.show()

    root.destroy()

