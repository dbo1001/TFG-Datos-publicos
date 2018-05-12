import pandas as pd
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from functools import reduce


# Formatos permitidos
filetypes = (('csv', '*.csv'), ('Todos', '*.*'))
# Lista de ficheros a juntar
ficheros = set()


def muestra_ficheros():
    """
    Muestra el nombre de los ficheros
    """
    files = [f for f in ficheros]
    texto = '\n'.join(files)
    ficheros_text.set(texto)


def vacia_ficheros():
    """
    Vacía la lista de ficheros
    """
    ficheros.clear()
    muestra_ficheros()
    vaciar_btn.grid_remove()
    lista_lbl.grid_remove()


def selecciona_ficheros(*args):
    """
    Acción al pulsar el botón para subir ficheros.
    """
    files = filedialog.askopenfilenames(filetypes=filetypes)
    for file in files:
        ficheros.add(file)
    muestra_ficheros()
    vaciar_btn.grid()
    lista_lbl.grid()


def selecciona_fichero_resultado():
    """
    Selecciona el fichero donde se guarda el resultado
    """
    file = filedialog.asksaveasfile(filetypes=filetypes)
    if file:
        return file
    messagebox.showerror('Error', 'Fichero no válido')
    return


def join():
    """
    Hace join de todos los ficheros csv
    """
    if len(ficheros) < 2:
        messagebox.showwarning('Warning', 'Selecciona al menos dos ficheros')
        return
    try:
        fichero = selecciona_fichero_resultado()
        if fichero:
            dataframes = [pd.read_csv(f) for f in ficheros]
            join_on = columna_join.get()
            if join_on == '':
                join_on = None
            how = how_join.get()
            df = reduce(lambda x, y: pd.merge(x, y, how=how, on=join_on), dataframes)
            df.to_csv(fichero)
    except:
        messagebox.showerror('Error', 'No se ha podido hacer el join')


# Raíz
root = Tk()
root.title("Join csv")

# Cuadro principal
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid()
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

# Variables
columna_join = StringVar()
how_join = StringVar()
ficheros_text = StringVar()

# Botón para subir csv
ttk.Button(mainframe, text="Subir csv", command=selecciona_ficheros).grid(row=0, columnspan=2, pady=5)

# Columna por la que hacer join
ttk.Label(mainframe, text="Columna:").grid(row=1, column=0)
columna_join_entry = ttk.Entry(mainframe, textvariable=columna_join)
columna_join_entry.grid(row=1, column=1, pady=5)

# Columna por la que hacer join
ttk.Label(mainframe, text="Columna:").grid(row=1, column=0)
columna_join_entry = ttk.Entry(mainframe, textvariable=columna_join, width=22)
columna_join_entry.grid(row=1, column=1, pady=3)

# Forma de hacer el join
how_join_box = ttk.Combobox(mainframe, textvariable=how_join, state='readonly', width=20)
how_join_box.grid(row=2, column=1, pady=3)
# print(how_join_box['values'])
how_join_box['values'] = ('inner', 'outer', 'left', 'right')
how_join_box.current(0)

# Botón para hacer join
ttk.Button(mainframe, text="Join", command=join).grid(row=3, column=1, pady=10, sticky='W')

# Lista de ficheros
lista_lbl = ttk.Label(mainframe, text='Ficheros seleccionados:')
lista_lbl.grid(row=4, columnspan=2, sticky='W')
ttk.Label(mainframe, textvariable=ficheros_text).grid(row=5, columnspan=2)
vaciar_btn = ttk.Button(mainframe, text='Vaciar', command=vacia_ficheros)
vaciar_btn.grid(row=6)
# Oculta los elementos
vaciar_btn.grid_remove()
lista_lbl.grid_remove()


# Ejecuta el programa
if __name__ == '__main__':
    root.mainloop()
