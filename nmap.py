import tkinter as tk
from tkinter import messagebox
import socket
from concurrent.futures import ThreadPoolExecutor
from urllib import request


#REFERENCIAS
#Para a construcao do listener
#https://thepythoncode.com/article/make-port-scanner-python
#https://www.geeksforgeeks.org/port-scanner-using-python/


#para a construcao do GUI
#https://codeonby.com/2021/02/24/port-scanner-gui-in-python-3/


#TRADUTOR DE NOME DE PORTAS
#OBRIGADO Fahri Yesil: https://systemweakness.com/navigating-network-security-building-a-python-port-scanner-eaf6ff59402a

def get_service_name(port):
    try:
        service = socket.getservbyport(port)
        return service
    except Exception as e:
        print("Erro ao obter o nome do serviço:", e)
    return "Desconhecido"

#funcao para ficar pingando as portas e retornar uma lista
def scan_ports(host, port_range):
    open_ports = []
    for port in port_range:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)  # Tempo limite de conexão
                result = s.connect_ex((host, port))
                if result == 0:
                    open_ports.append(port)
                    service_name = get_service_name(port)
                    print(f"Porta {port} ({service_name}) está aberta.")
        except socket.error:
            pass
    return open_ports

#FUNCAO PRINCIPAL
def start_scan():
    host = entry_host.get()
    port_range = range(int(entry_start_port.get()), int(entry_end_port.get()) + 1)
    open_ports = []  
    services = [] 

    with ThreadPoolExecutor(max_workers=10) as executor:
        future = executor.submit(scan_ports, host, port_range)
        open_ports = future.result()

    for port in open_ports:
        service_name = get_service_name(port)
        services.append(f"{port} ({service_name})")

    if services:
        messagebox.showinfo("Resultado", "Portas abertas:\n" + "\n".join(services))
    else:
        messagebox.showinfo("Resultado", "Nenhuma porta aberta encontrada.")

#gui
root = tk.Tk()
root.title("Escaneamento de Portas")

label_host = tk.Label(root, text="Host:")
label_host.grid(row=0, column=0, padx=5, pady=5)
entry_host = tk.Entry(root)
entry_host.grid(row=0, column=1, padx=5, pady=5)

label_start_port = tk.Label(root, text="Porta inicial:")
label_start_port.grid(row=1, column=0, padx=5, pady=5)
entry_start_port = tk.Entry(root)
entry_start_port.grid(row=1, column=1, padx=5, pady=5)

label_end_port = tk.Label(root, text="Porta final:")
label_end_port.grid(row=2, column=0, padx=5, pady=5)
entry_end_port = tk.Entry(root)
entry_end_port.grid(row=2, column=1, padx=5, pady=5)

button_scan = tk.Button(root, text="Escanear", command=start_scan)
button_scan.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
