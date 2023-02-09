import customtkinter as ctk 
from tkinter import *
import sqlite3
from tkinter import messagebox


class BackEnd():
    def conecta_db(self):
        self.conn = sqlite3.connect("Sistema_usuarios.db")
        self.cursor = self.conn.cursor()
        print("Banco de dados conectado!")
    
    def desconecta_db(self):
        self.conn.close()
        print("Banco de dados desconectado")

    def cria_tabela(self):
        self.conecta_db()
        
        self.cursor.execute("""
             CREATE TABLE IF NOT EXISTS Usuarios(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL,
                Email TEXT NOT NULL,
                Senha TEXT NOT NULL,
                Confirma_senha TEXT NOT NULL
                );
        """)
        self.conn.commit()
        print("Tabela criada com sucesso!")
        self.desconecta_db()

    def cadastrar_usuario(self):
        self.username_cadastro = self.username_cadastro_entry.get()
        self.email_cadastro = self.email_cadastro_entry.get()
        self.senha_cadastro = self.senha_cadastro_entry.get()
        self.confirma_senha_cadastro = self.confirma_senha_entry.get()

        self.conecta_db()

        self.cursor.execute("""
            INSERT INTO Usuarios (Username, Email, Senha, Confirma_senha)
            VALUES (?, ?, ?, ?)""", (self.username_cadastro, self.email_cadastro, self.senha_cadastro, self.confirma_senha_cadastro))

        try:
            if (self.username_cadastro == '' or self.email_cadastro == '' or self.senha_cadastro == '' or self.confirma_senha_cadastro == ''):
                messagebox.showerror(title="Sistema de login", message="ERRO!!!\nPor favor preeencha todos os campos!")
            elif (len(self.username_cadastro) < 4):
                messagebox.showwarning(title="Sistema de Login", message="O nome de usuário deve ser de pelo menos 4 caracteres.")
            elif (len(self.senha_cadastro) < 4):
                messagebox.showwarning(title="Sistema de Login", message="A senha deve ser de pelo menos 4 caracteres.")
            
            elif (self.senha_cadastro != self.confirma_senha_cadastro):
                messagebox.showerror(title="Sistema de login", message="ERRO!!!\nAs senhas colocadas não são iguais!")
            else:
                self.conn.commit()
                messagebox.showinfo(title="Sistema de login", message=f"Parabens {self.username_cadastro}\nOs seus dados foram cadastrados com sucesso!")
                self.desconecta_db()
                self.limpa_entry_cadastro()


        except:
            messagebox.showerror(title="Sistema de login", message="Erro no processamento do seu cadastro!\nPor favor tente novamente!")
            self.desconecta_db()

    def verifica_login(self):
        self.username_login = self.username_login_entry.get()
        self.senha_login = self.senha_login_entry.get()
        self.conecta_db()
        self.cursor.execute("""SELECT * FROM Usuarios WHERE (Username = ? AND Senha = ?)""", (self.username_login, self.senha_login))

        self.verifica_dados = self.cursor.fetchone() #Percorrendo na tabela usuarios

        try:
            if(self.username_login in self.verifica_dados and self.senha_login in self.verifica_dados):
                messagebox.showinfo(title='Sistema de Login', message=f'Parabéns {self.username_login}\nLogin feito com sucesso!')
                self.desconecta_db()
                self.limpa_entry_login()
        except:
            messagebox.showerror(title='Sistema de login', message="ERRO!!!\nDados não encontrados no sistema!")
            self.desconecta_db()


class App(ctk.CTk, BackEnd):
    def __init__(self):
        super().__init__()
        self.configuracoes_da_janela_inicial()
        self.tela_de_login()
        self.cria_tabela()
    
    
    def configuracoes_da_janela_inicial(self):
        self.geometry("700x400")
        self.title("Sistema Usuário")
        self.resizable(False, False)


    def tela_de_login(self):
  
        #Imagem
        self.img = PhotoImage(file="PngItem_380681.png")
        self.lb_img = ctk.CTkLabel(self, text=None, image=self.img)
        self.lb_img.grid(row=1, column=0, padx=10)
        
        #Título da plataforma

        self.title = ctk.CTkLabel(self, text="Faça seu login ou Cadastre-se!", font=('Century Gothic bold', 14))
        self.title.grid(row=0, column=0, pady=10, padx=10)
        
        #Frame formulario login
        self.frame_login = ctk.CTkFrame(self, width=350, height=380)
        self.frame_login.place(x=350, y=10)
        
        #colocando widgets dentro do frame
        self.lb_title = ctk.CTkLabel(self.frame_login, text="Faça seu login", font=('Century Gothic bold', 22), corner_radius=15)
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)

        self.username_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Seu nome de usuario..", font=("Century Gothic bold", 16), corner_radius=15, border_color="#005")
        self.username_login_entry.grid(row=1, column=0, padx=10, pady=10)
        
        self.senha_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Sua senha..", font=("Century Gothic bold", 16), corner_radius=15, border_color="#005", show="*")
        self.senha_login_entry.grid(row=2, column=0, padx=10, pady=10)

        self.ver_senha = ctk.CTkCheckBox(self.frame_login, text='Clique para ver a senha', font=("Century Gothic bold", 14), corner_radius=20)
        self.ver_senha.grid(row=3, column=0, padx=10, pady=10)

        self.botao_login = ctk.CTkButton(self.frame_login, width=300, text='Fazer Login', font=("Century Gothic bold", 16), corner_radius=15, command=self.verifica_login)
        self.botao_login.grid(row=4, column=0, padx=10, pady=10)

        self.spam = ctk.CTkLabel(self.frame_login, text="Se não tem conta, clique no botão abaixo para poder se cadastrar!", font=("Century Gothic", 10))
        self.spam.grid(row=5, column=0, padx=10, pady=10)
        
        self.botao_cadastro = ctk.CTkButton(self.frame_login, width=300, fg_color="green", hover_color="#050" ,text='Cadastro', font=("Century Gothic bold", 16), corner_radius=15, command=self.tela_de_cadastro)
        self.botao_cadastro.grid(row=6, column=0, padx=10, pady=10)


    def tela_de_cadastro(self):
        #remover tela de login
        self.frame_login.place_forget()
        #frame de cadastro
        self.frame_cadastro = ctk.CTkFrame(self, width=350, height=380)
        self.frame_cadastro.place(x=350, y=10)
        #Titulo
        self.lb_title = ctk.CTkLabel(self.frame_cadastro, text="Faça seu Cadastro", font=('Century Gothic bold', 22))
        self.lb_title.grid(row=0, column=0, padx=10, pady=5)

        #Criar os widgets da tela de cadastro
        self.username_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Seu nome de usuario..", font=("Century Gothic bold", 16), corner_radius=15, border_color="#005")
        self.username_cadastro_entry.grid(row=1, column=0, padx=10, pady=5)
        
        self.email_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Seu email..", font=("Century Gothic bold", 16), corner_radius=15, border_color="#005")
        self.email_cadastro_entry.grid(row=2, column=0, padx=10, pady=5)
        

        self.senha_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Sua senha..", font=("Century Gothic bold", 16), corner_radius=15, border_color="#005", show="#")
        self.senha_cadastro_entry.grid(row=3, column=0, padx=10, pady=5)
        
        self.confirma_senha_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Confirme sua senha..", font=("Century Gothic bold", 16), corner_radius=15, border_color="#005", show="#")
        self.confirma_senha_entry.grid(row=4, column=0, padx=10, pady=5)

        self.ver_senha = ctk.CTkCheckBox(self.frame_cadastro, text='Clique para ver a senha', font=("Century Gothic bold", 14), corner_radius=20)
        self.ver_senha.grid(row=5, column=0, pady=5)

        self.botao_cadastrar_user = ctk.CTkButton(self.frame_cadastro, width=300, fg_color="green", hover_color="#050" ,text='Fazer Cadastro', font=("Century Gothic bold", 16), corner_radius=15, command=self.cadastrar_usuario)
        self.botao_cadastrar_user.grid(row=6, column=0, padx=10, pady=10)


        self.botao_login_back = ctk.CTkButton(self.frame_cadastro, width=300, text='Voltar a tela de login', font=("Century Gothic bold", 16), corner_radius=15, fg_color="#444", hover_color="#333", command=self.tela_de_login)
        self.botao_login_back.grid(row=7, column=0, padx=10, pady=10)

    def limpa_entry_cadastro(self):
        self.username_cadastro_entry.delete(0, END)
        self.email_cadastro_entry.delete(0, END)
        self.senha_cadastro_entry.delete(0, END)
        self.confirma_senha_entry.delete(0, END)
      
    def limpa_entry_login(self):
        self.username_login_entry.delete(0, END)
        self.senha_login_entry.delete(0, END)




if __name__ == '__main__':
    app = App()
    app.mainloop()



