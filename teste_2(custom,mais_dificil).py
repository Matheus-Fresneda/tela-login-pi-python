import customtkinter as ctk
from tkinter import messagebox
import os
import ctypes
from PIL import Image, ImageTk, ImageFilter, ImageEnhance

# Carrega a fonte Quicksand antes de criar os widgets
_font_path = os.path.join(os.path.dirname(__file__), "Quicksand.ttf")
if os.path.exists(_font_path):
    ctypes.windll.gdi32.AddFontResourceExW(_font_path, 0x10, 0)



def reabrir_dashboard():
    import customtkinter as ctk
    from tkinter import messagebox
    import os
    import ctypes
    from PIL import Image, ImageTk, ImageFilter, ImageEnhance

    _font_path = os.path.join(os.path.dirname(__file__), "Quicksand.ttf")
    if os.path.exists(_font_path):
        ctypes.windll.gdi32.AddFontResourceExW(_font_path, 0x10, 0)

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
    logo_img_fundo = None

    def _preparar_logo_hd(path):
        cache_path = path.replace(".png", "_hd_cache.png")
        if os.path.exists(cache_path) and os.path.getmtime(cache_path) >= os.path.getmtime(path):
            return Image.open(cache_path).convert("RGBA")
        img = Image.open(path).convert("RGBA")
        r, g, b, a = img.split()
        rgb = Image.merge("RGB", (r, g, b))
        target_w = img.width * 8
        target_h = img.height * 8
        rgb = rgb.resize((target_w, target_h), Image.LANCZOS)
        rgb = rgb.filter(ImageFilter.UnsharpMask(radius=1.0, percent=80, threshold=3))
        a_scaled = a.resize((target_w, target_h), Image.LANCZOS)
        img = Image.merge("RGBA", (*rgb.split(), a_scaled))
        img.save(cache_path, "PNG", optimize=False, compress_level=1)
        return img

    logo_base = _preparar_logo_hd(logo_path) if os.path.exists(logo_path) else None

    def desenhar_fundo(_event=None):
        nonlocal logo_img_fundo
        largura = janela.winfo_width()
        altura = janela.winfo_height()
        canvas.delete("bg")
        canvas.create_oval(-90, altura - 120, 60, altura + 30, fill="#c10000", outline="#c10000", tags="bg")
        canvas.create_oval(largura - 90, -70, largura + 60, 80, fill="#c10000", outline="#c10000", tags="bg")
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
        logo_label = ctk.CTkLabel(janela, text="Etec", font=("Quicksand", 20, "bold"), text_color="#333333", fg_color="transparent")
    logo_label.place(x=20, y=14)

    titulo = ctk.CTkLabel(janela, text="Show de Quimica", font=("Quicksand", 33, "bold"), text_color="#111111", fg_color="transparent")
    titulo.place(relx=0.5, y=122, anchor="center")

    frame = ctk.CTkFrame(janela, width=340, height=370, corner_radius=22, fg_color="#c5c5c5")
    frame.place(relx=0.5, rely=0.5, anchor="center")
    frame.pack_propagate(False)

    bem_vindo = ctk.CTkLabel(frame, text="Bem-Vindos!", font=("Quicksand", 34, "bold"), text_color="#111111")
    bem_vindo.pack(pady=(58, 48))

    def entrar_aluno():
        janela.destroy()
        from deashboard_login_aluno import abrir_login_aluno
        abrir_login_aluno()

    from deashboard_login_professor import abrir_login_professor
    def entrar_prof():
        janela.destroy()
        abrir_login_professor()

    _icone_aluno_path = os.path.join(os.path.dirname(__file__), "icone_aluno.png")
    _icone_aluno_pil = Image.open(_icone_aluno_path).convert("RGBA") if os.path.exists(_icone_aluno_path) else None
    icone_aluno = ctk.CTkImage(light_image=_icone_aluno_pil, dark_image=_icone_aluno_pil, size=(22, 22)) if _icone_aluno_pil else None

    btn_aluno = ctk.CTkButton(
        frame,
        text="Entrar como Aluno",
        image=icone_aluno,
        compound="left",
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

    _icone_prof_path = os.path.join(os.path.dirname(__file__), "icone_prof.png")
    _icone_prof_pil = Image.open(_icone_prof_path).convert("RGBA") if os.path.exists(_icone_prof_path) else None
    icone_prof = ctk.CTkImage(light_image=_icone_prof_pil, dark_image=_icone_prof_pil, size=(22, 22)) if _icone_prof_pil else None

    btn_prof = ctk.CTkButton(
        frame,
        text="Entrar como Professor",
        image=icone_prof,
        compound="left",
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
        font=("Quicksand", 12),
        text_color="#2068a8",
        justify="center"
    )
    termos_frame.place(relx=0.5, rely=0.94, anchor="s")

    janela.mainloop()

if __name__ == "__main__":
    reabrir_dashboard()

canvas = ctk.CTkCanvas(janela, highlightthickness=0, bg="#e6e6e6")
canvas.place(x=0, y=0, relwidth=1, relheight=1)

logo_path = os.path.join(os.path.dirname(__file__), "logoETEC.png")
logo_img_fundo = None

def _preparar_logo_hd(path):
    """Upscale limpo com LANCZOS e sharpening mínimo."""
    cache_path = path.replace(".png", "_hd_cache.png")
    if os.path.exists(cache_path) and os.path.getmtime(cache_path) >= os.path.getmtime(path):
        return Image.open(cache_path).convert("RGBA")

    img = Image.open(path).convert("RGBA")
    r, g, b, a = img.split()
    rgb = Image.merge("RGB", (r, g, b))

    # Upscale único para ~8× o tamanho original — LANCZOS é suficiente
    target_w = img.width * 8
    target_h = img.height * 8
    rgb = rgb.resize((target_w, target_h), Image.LANCZOS)

    # Sharpening leve apenas para compensar o suavizamento do LANCZOS
    rgb = rgb.filter(ImageFilter.UnsharpMask(radius=1.0, percent=80, threshold=3))

    a_scaled = a.resize((target_w, target_h), Image.LANCZOS)
    img = Image.merge("RGBA", (*rgb.split(), a_scaled))

    img.save(cache_path, "PNG", optimize=False, compress_level=1)
    return img

logo_base = _preparar_logo_hd(logo_path) if os.path.exists(logo_path) else None

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

        # Reduz da versão HD pré-processada (downscale = muito mais nítido que upscale)
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
    logo_label = ctk.CTkLabel(janela, text="Etec", font=("Quicksand", 20, "bold"), text_color="#333333", fg_color="transparent")
logo_label.place(x=20, y=14)

titulo = ctk.CTkLabel(janela, text="Show de Quimica", font=("Quicksand", 33, "bold"), text_color="#111111", fg_color="transparent")
titulo.place(relx=0.5, y=122, anchor="center")

frame = ctk.CTkFrame(janela, width=340, height=370, corner_radius=22, fg_color="#c5c5c5")
frame.place(relx=0.5, rely=0.5, anchor="center")
frame.pack_propagate(False)

bem_vindo = ctk.CTkLabel(frame, text="Bem-Vindos!", font=("Quicksand", 34, "bold"), text_color="#111111")
bem_vindo.pack(pady=(58, 48))


def entrar_aluno():
    janela.destroy()
    from deashboard_login_aluno import abrir_login_aluno
    abrir_login_aluno()




# Importa a tela de login do professor
from deashboard_login_professor import abrir_login_professor

def entrar_prof():
    janela.destroy()
    abrir_login_professor()


_icone_aluno_path = os.path.join(os.path.dirname(__file__), "icone_aluno.png")
_icone_aluno_pil = Image.open(_icone_aluno_path).convert("RGBA") if os.path.exists(_icone_aluno_path) else None
icone_aluno = ctk.CTkImage(light_image=_icone_aluno_pil, dark_image=_icone_aluno_pil, size=(22, 22)) if _icone_aluno_pil else None

btn_aluno = ctk.CTkButton(
    frame,
    text="Entrar como Aluno",
    image=icone_aluno,
    compound="left",
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

_icone_prof_path = os.path.join(os.path.dirname(__file__), "icone_prof.png")
_icone_prof_pil = Image.open(_icone_prof_path).convert("RGBA") if os.path.exists(_icone_prof_path) else None
icone_prof = ctk.CTkImage(light_image=_icone_prof_pil, dark_image=_icone_prof_pil, size=(22, 22)) if _icone_prof_pil else None

btn_prof = ctk.CTkButton(
    frame,
    text="Entrar como Professor",
    image=icone_prof,
    compound="left",
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
    font=("Quicksand", 12),
    text_color="#2068a8",
    justify="center"
)
termos_frame.place(relx=0.5, rely=0.94, anchor="s")

janela.mainloop()