# Autor: Eduardo S. F. Reis
# E-mail: edufrancoreis@hotmail.com
# Produção:  15/12/2022
# Ultima atualização: 31/01/2023

import cv2
import csv
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import csv  

print('Primeiro leia os arquivos fixation_on_surface e depois a imagem correspondente')
print('Em caso de error ou fechar a janela sem querer renicie o terminal')

#Abre a pagina de arquivo
root = tk.Tk()
root.withdraw()
file_csv = filedialog.askopenfilename(title="Selecione o fixation_on_surface")

#Define a imagem
root = tk.Tk()
root.withdraw()
file_image = filedialog.askopenfilename(title="Selecione a imagem")
imagem = (file_image)

#Le a imagem e reconhece o tamanho da imagem
im = Image.open(imagem)
width, height = im.size

#Define o tamanho da imagem
L = width  #Largura(x)
H = height #Altura(y)

#Abre a imagem
image = plt.imread(imagem)
fig, ax = plt.subplots()

# Acompanha a posição do círculo anterior
prev_x, prev_y = None, None

#Acompanha os id
prev_id = None
id = 0

#Abre o arquivo
with open(file_csv, mode ='r')as file:  
    df = csv.reader(file)  
    # ignora a primeira linha do arquivo
    next(df) 
    for i in df:
        world_timestamp = i[0]
        world_index = i[1]
        fixation_id = int(i[2])
        start_timestamp = i[3]
        duration = float(i[4])
        dispersion = i[5]
        norm_pos_x = float(i[6])
        norm_pos_y = float(i[7])
        x_scaled = i[8]
        y_scaled = i[9]
        on_surf = i[10]
        # verifica se as coordenadas são válidas
        if norm_pos_x > 1 or norm_pos_y > 1:
            continue
        
        y= norm_pos_y * H
        x = norm_pos_x * L
        r = duration / 2
        
        #Salva os id para criar o plot
        if prev_id != fixation_id:
            ax.scatter(x,y, s=r,color='red')
            
         # Se este não for o primeiro círculo, desenhe uma linha conectando-o ao círculo anterior
            if prev_x is not None and prev_y is not None:
                ax.plot([prev_x,x], [prev_y, y], 'g-')            
               
         #Escreve o numero
            id = id + 1
            ax.text(x, y,id, fontsize=10, color='k')
        
        # # Salve a posição do círculo atual para a próxima iteração
            prev_x = x
            prev_y = y
            prev_id = fixation_id


plt.axis('off');
image = cv2.flip(image, 0)
plt.imshow(image)
plt.gca().invert_yaxis()
plt.show()
