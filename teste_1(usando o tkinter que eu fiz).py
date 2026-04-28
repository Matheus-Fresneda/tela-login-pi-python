import tkinter as tk
from tkinter import messagebox

janela = tk.Tk()
janela.title("Show de Química")
janela.geometry("400x500")
janela.configure(bg="#f0f0f0")

tk.Label(janela, text="Show de Química", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=20)

frame = tk.Frame(janela, bg="#d9d9d9", width=300, height=320)
frame.pack(pady=20)
frame.pack_propagate(False)

tk.Label(frame, text="Bem-Vindos!", font=("Arial", 16, "bold"), bg="#d9d9d9").pack(pady=10)

tk.Label(frame, text="Email:", bg="#d9d9d9").pack()
entrada_email = tk.Entry(frame, width=25)
entrada_email.pack(pady=5)

tk.Label(frame, text="Senha:", bg="#d9d9d9").pack()
entrada_senha = tk.Entry(frame, show="*", width=25)
entrada_senha.pack(pady=5)

def entrar_aluno():
    email = entrada_email.get()
    senha = entrada_senha.get()

    if email == "jota.dev@etec.com" and senha == "1234":
        messagebox.showinfo("Login", "Entrou como aluno")
    else:
        messagebox.showerror("Erro", "Email ou senha ETEC incorreto")

def entrar_prof():
    email = entrada_email.get()
    senha = entrada_senha.get()

    if email == "jota.prof@etec.com" and senha == "5678":
        messagebox.showinfo("Login", "Entrou como professor")
    else:
        messagebox.showerror("Erro", "Email ou senha ETEC incorreto")


tk.Button(frame, text="Entrar como Aluno", command=entrar_aluno).pack(pady=10)
tk.Button(frame, text="Entrar como Professor", command=entrar_prof).pack(pady=10)


tk.Label(janela, text="Ao fazer login você concorda com os termos", bg="#f0f0f0").pack(side="bottom", pady=20)

janela.mainloop()