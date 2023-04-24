import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pyglet
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image  
from pathlib import Path
from tkinter.simpledialog import askstring
from tkinter import messagebox, simpledialog

pyglet.font.add_file('./utils/Anton.ttf')  

class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.geometry('630x310')
        self.title('Seja bem vindo ao EstoqueFácil!')
        ttk.Label(self, text='EstoqueFácil', font=('Anton', 62)).pack()
        ttk.Label(self, text='', font=('Anton', 22)).pack()
        ttk.Button(self,text='Iniciar', command=self.message_upload,width=32).pack(expand=False)

    def message_upload(self):
        anwser = messagebox.askquestion('Importação de Inventário', 'Deseja importar o arquivo de inventário?')
        if anwser == 'yes':
            self.show_uploadScreen()
    
    def show_uploadScreen(self):
        self.destroy()
        UploadScreen()

class UploadScreen(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('720x530')
        ttk.Label(self, text='EstoqueFácil', font=('Anton', 62)).pack()
        ttk.Label(self, text='Importação de inventário', font=('Lato', 24)).pack()
        ttk.Label(self, text='', font=('Lato', 32)).pack()
        ttk.Button(self, text='Importar arquivo', command=self.upload_csv, width=32).pack(expand=False)
        ttk.Label(self, text='', font=('Lato', 32)).pack()
        ttk.Label(self, text='Faça upload de um arquivo *.csv neste modelo', font=('Lato', 16)).pack()
        ttk.Label(self, text='', font=('Lato', 16)).pack()

        self.img = ImageTk.PhotoImage(Image.open('./utils/image.png'))
        panel = ttk.Label(self, image = self.img)
        panel.pack()

    def upload_csv(self):
        csv_file_path = askopenfilename()
        if '.csv' in csv_file_path:
            messagebox.showinfo('Importação com sucesso', 'O arquivo foi importado com sucesso!!')
            self.destroy()
            self.show_main_screen()

            # copiando o arquivo do computador do usuario para dentro da pasta dados onde será manipulado
            src = Path(csv_file_path)
            dest = Path('./dados/inventario_inicial.csv')
            dest.write_bytes(src.read_bytes())

            # criando o arquivo que sera modificado
            src = Path('./dados/inventario_inicial.csv')
            dest = Path('./dados/inventario_final.csv')
            dest.write_bytes(src.read_bytes())

        else:
            messagebox.showerror('Importação mal sucedida', 'O arquivo importado não é no formato *csv')

    def show_main_screen(self):
        MainScreen()

class MainScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('860x260')

        ttk.Label(self, text='EstoqueFácil', font=('Anton', 62)).pack()
        ttk.Button(self, text='Registrar entrada/saída', command=MovementsScreen, width=32).pack(expand=False)
        ttk.Button(self, text='Exportar inventário', command=CSVHandler.export_csv, width=32).pack(expand=False)

class MovementsScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('860x360')
        ttk.Label(self, text='EstoqueFácil', font=('Anton', 62)).grid(column=1, row=0)
        ttk.Label(self, text='Registro de Saída de produtos', font=('Lato', 16)).grid(column=0, row=2, sticky="NESW", padx=10)

        ttk.Label(self, text='Código do produto', font=('Lato', 16)).grid(column=0, row=2, sticky="NESW", padx=10)
        self.codigo = ttk.Entry(self, width=10)
        self.codigo.grid(column=1, row=2, sticky="NESW", pady=10)

        ttk.Label(self, text='Quantidade do produto', font=('Lato', 16)).grid(column=0, row=4, sticky="NESW", padx=10)
        self.quantidade = ttk.Entry(self, width=50)
        self.quantidade.grid(column=1, row=4, sticky="NESW", pady=10)
    
        ttk.Button(self, text='Registrar saída', command=lambda:self.get_values_input()).grid(column=1, row=5)

    def get_values_input(self):
        codigo = self.codigo.get()
        quantidade = self.quantidade.get()

        CSVHandler.edit_csv(codigo, quantidade)

class CSVHandler():
    def __init__(self):
        super().__init__()

    def find_code(cod, quant):
        with open('./dados/inventario_final.csv', 'r', encoding='utf-8') as f:
            csv = f.readlines()

        for j,i in enumerate(csv):
            print(i)
            i = i.split(";")
            
            if cod == i[0]:
                print("código encontrado")
                string = f'{i[0]};{i[1]};{int(i[2])+int(quant)}\n'
                return [True, j, string]

        f.close()
        return [False]

    def edit_csv(cod, quant):

        ans = CSVHandler.find_code(cod, quant)

        true = ans[0]

        if true:
            index = ans[1]
            string = ans[2]

            with open('./dados/inventario_final.csv', 'r', encoding='utf-8') as f:
                csv = f.readlines()
                answer = messagebox.askquestion('Alteração de item', f'Deseja alterar o item {string.split(";")[1]}?')
                if answer == 'yes':
                    with open('./dados/inventario_final.csv', 'w', encoding='utf-8') as f:
                        csv[index] = string
                        f.writelines(csv)
                        messagebox.showinfo('Alterado com sucesso', f'Foi alterada a quantidade do produto {string.split(";")[1]}')
                    f.close()
                else:
                    messagebox.showinfo('Sem alteração', 'Nenhum item foi alterado')
            f.close()
        
            
        else:
            anwser = messagebox.askquestion('Cadastrar item', 'Deseja cadastrar esse item?')

            if anwser == 'yes':
                desc = simpledialog.askstring('Descricao', 'Digite o nome do produto a ser cadastrado:')
                with open('./dados/inventario_final.csv', 'a', encoding='utf-8') as f:
                    csv = f'{cod};{desc};{int(quant)}'
                    f.write(csv)         
                    messagebox.showinfo('Cadastrado com sucesso',f'Foi cadastrado o produto {desc}')
                f.close()
             
    def export_csv():
        # copiar um arquivo de um lugar para o outro
        src = Path('./dados/inventario_final.csv')
        dest = Path('./export/inventario.csv')
        dest.write_bytes(src.read_bytes())
        messagebox.showinfo('Exportação realizada com sucesso','O arquivo foi salvo na pasta Export do programa')


if __name__ == "__main__":
    app = App()
    app.mainloop()