import customtkinter as ctk
from tkinter import messagebox
import os
from PIL import Image, ImageTk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme(os.path.join(os.path.dirname(__file__), "cor_vermelha.json"))
janela = ctk.CTk()
janela.title("Show de Química")
janela.geometry("1200x700")
janela.minsize(900, 600)
janela.configure(fg_color="#e6e6e6")
janela.state("zoomed")

canvas = ctk.CTkCanvas(janela, highlightthickness=0, bg="#e6e6e6")
canvas.place(x=0, y=0, relwidth=1, relheight=1)

logo_path = os.path.join(os.path.dirname(__file__), "logoETEC.png")
logo_base = Image.open(logo_path).convert("RGBA") if os.path.exists(logo_path) else None
logo_img_fundo = None

def desenhar_fundo(_event=None):
    global logo_img_fundo

    largura = janela.winfo_width()
    altura = janela.winfo_height()
    canvas.delete("bg")

    # Circulos decorativos dos cantos com base no tamanho atual da janela
    canvas.create_oval(-90, altura - 120, 60, altura + 30, fill="#c10000", outline="#c10000", tags="bg")
    canvas.create_oval(largura - 90, -70, largura + 60, 80, fill="#c10000", outline="#c10000", tags="bg")

    # Marca d'agua com a logo da ETEC em baixa opacidade
    if logo_base is not None:
        largura_logo = max(620, int(largura * 0.72))
        proporcao = largura_logo / logo_base.width
        altura_logo = max(240, int(logo_base.height * proporcao))

        logo_redimensionada = logo_base.resize((largura_logo, altura_logo), Image.LANCZOS)
        logo_suave = logo_redimensionada.copy()
        alpha = logo_suave.getchannel("A")
        alpha = alpha.point(lambda pixel: int(pixel * 0.16))
        logo_suave.putalpha(alpha)

        logo_img_fundo = ImageTk.PhotoImage(logo_suave)
        canvas.create_image(
            int(largura * 0.49),
            int(altura * 0.44),
            image=logo_img_fundo,
            anchor="center",
            tags="bg"
        )


janela.bind("<Configure>", desenhar_fundo)
desenhar_fundo()

if logo_base is not None:
    logo_pil = logo_base.copy()
    logo_img = ctk.CTkImage(light_image=logo_pil, dark_image=logo_pil, size=(96, 38))
    logo_label = ctk.CTkLabel(janela, text="", image=logo_img, fg_color="transparent")
else:
    logo_label = ctk.CTkLabel(janela, text="Etec", font=("Arial", 20, "bold"), text_color="#333333", fg_color="transparent")
logo_label.place(x=20, y=14)

titulo = ctk.CTkLabel(janela, text="Show de Quimica", font=("Arial", 33, "bold"), text_color="#111111", fg_color="transparent")
titulo.place(relx=0.5, y=122, anchor="center")

frame = ctk.CTkFrame(janela, width=340, height=370, corner_radius=22, fg_color="#c5c5c5")
frame.place(relx=0.5, rely=0.5, anchor="center")
frame.pack_propagate(False)

bem_vindo = ctk.CTkLabel(frame, text="Bem-Vindos!", font=("Arial", 34, "bold"), text_color="#111111")
bem_vindo.pack(pady=(58, 48))


def entrar_aluno():
    messagebox.showinfo("Login", "Entrou como aluno")


def entrar_prof():
    messagebox.showinfo("Login", "Entrou como professor")


btn_aluno = ctk.CTkButton(
    frame,
    text="Entrar como Aluno",
    width=240,
    height=40,
    corner_radius=22,
    fg_color="#ebebeb",
    text_color="#7f7f7f",
    hover_color="#dddddd",
    border_width=1,
    border_color="#bcbcbc",
    command=entrar_aluno
)
btn_aluno.pack(pady=(0, 30))

btn_prof = ctk.CTkButton(
    frame,
    text="Entrar como Professor",
    width=240,
    height=40,
    corner_radius=22,
    fg_color="#ebebeb",
    text_color="#7f7f7f",
    hover_color="#dddddd",
    border_width=1,
    border_color="#bcbcbc",
    command=entrar_prof
)
btn_prof.pack(pady=(0, 18))

termos_frame = ctk.CTkLabel(
    frame,
    text="Ao fazer login voce concorda com os Termo\nde Uso, Politica de Privacidade e Cookies",
    font=("Arial", 12),
    text_color="#2068a8",
    justify="center"
)
termos_frame.place(relx=0.5, rely=0.94, anchor="s")

janela.mainloop()