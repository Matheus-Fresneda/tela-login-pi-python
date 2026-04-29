import customtkinter as ctk
import os
from PIL import Image, ImageTk, ImageFilter


def abrir_login_professor(janela_pai=None):
    login_prof = ctk.CTk()
    login_prof.title("Login Professor")
    login_prof.geometry("1200x700")
    login_prof.minsize(900, 600)
    login_prof.configure(fg_color="#e6e6e6")
    login_prof.state("zoomed")

    canvas = ctk.CTkCanvas(login_prof, highlightthickness=0, bg="#e6e6e6")
    canvas.place(x=0, y=0, relwidth=1, relheight=1)

    logo_path = os.path.join(os.path.dirname(__file__), "logoETEC.png")
    logo_img_fundo = None

    def preparar_logo_hd(path):
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

    logo_base = preparar_logo_hd(logo_path) if os.path.exists(logo_path) else None

    def desenhar_fundo(_event=None):
        nonlocal logo_img_fundo
        largura = login_prof.winfo_width()
        altura = login_prof.winfo_height()
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

    login_prof.bind("<Configure>", desenhar_fundo)
    desenhar_fundo()

    if logo_base is not None:
        logo_pil = logo_base.copy()
        logo_img = ctk.CTkImage(light_image=logo_pil, dark_image=logo_pil, size=(96, 38))
        logo_label = ctk.CTkLabel(login_prof, text="", image=logo_img, fg_color="transparent")
    else:
        logo_label = ctk.CTkLabel(login_prof, text="Etec", font=("Quicksand", 20, "bold"), text_color="#333333", fg_color="transparent")
    logo_label.place(x=20, y=14)

    # Frame central
    frame = ctk.CTkFrame(login_prof, width=370, height=320, corner_radius=22, fg_color="#d1d1d1")
    frame.place(relx=0.5, rely=0.5, anchor="center")
    frame.pack_propagate(False)
    frame.lift()  # Garante que o frame fique acima do canvas
    # Não usar border_width nem fg_color transparente

    # Labels e campos
    label_login = ctk.CTkLabel(frame, text="Login", font=("Quicksand", 18, "bold"), text_color="#111111")
    label_login.pack(pady=(30, 0), anchor="w", padx=30)
    entry_login = ctk.CTkEntry(frame, placeholder_text="xxxxxx@cps.sp.gov", width=270, height=38, font=("Quicksand", 15))
    entry_login.pack(pady=(0, 18), padx=30)

    label_senha = ctk.CTkLabel(frame, text="Senha", font=("Quicksand", 18, "bold"), text_color="#111111")
    label_senha.pack(pady=(0, 0), anchor="w", padx=30)
    entry_senha = ctk.CTkEntry(frame, placeholder_text="Digite sua senha:", show="*", width=270, height=38, font=("Quicksand", 15))
    entry_senha.pack(pady=(0, 18), padx=30)

    def entrar():
        # Aqui você pode validar o login/senha e abrir o dashboard do professor
        ctk.CTkMessagebox(title="Login", message="Login realizado (simulação)")

    btn_entrar = ctk.CTkButton(frame, text="Entrar", width=120, height=38, corner_radius=18, command=entrar)
    btn_entrar.pack(pady=(0, 10))

    voltar_label = ctk.CTkLabel(frame, text="Voltar para tela inicial", font=("Quicksand", 13), text_color="#2068a8", cursor="hand2")
    voltar_label.pack(pady=(8, 0))
    def voltar_tela_inicial():
        login_prof.destroy()
        import dashboard_principal as tela_principal
        tela_principal.reabrir_dashboard()
    voltar_label.bind("<Button-1>", lambda e: voltar_tela_inicial())

if __name__ == "__main__":
    root = ctk.CTk()
    abrir_login_professor(root)
    root.mainloop()


