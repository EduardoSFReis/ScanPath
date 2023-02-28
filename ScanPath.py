# Autor: Eduardo S. F. Reis
# E-mail: edufrancoreis@hotmail.com
# Produção:  15/12/2022
# Ultima atualização: 31/01/2023

import cv2
import pandas as pd
import csv
import math as m
import matplotlib.pyplot as plt
from PIL import Image
import tkinter as tk
from tkinter import filedialog

def SelecionarCSV():
    root = tk.Tk()

    file_csv = filedialog.askopenfilename(title='Primeiro leia os arquivos fixation_on_surface')
    return file_csv

def SelecionarImagem():
    root = tk.Tk()
 
   
    file_image = filedialog.askopenfilename(title='Leia a Imagem')
    return file_image

def LerCSV(file_csv):
    df = pd.read_csv(file_csv)
    return df

def PlotGrafico(data, image, corC, corL, tL):
    width, height = Image.open(image).size
    L = width - 20  #Largura(x)
    H = height #Altura(y)
    
    # Define a imagem
    image = plt.imread(image)
    fig, ax = plt.subplots()

    # Acompanha a posição do círculo anterior
    prev_x, prev_y = None, None

    # Acompanha os id
    prev_id = None
    id = 0

    # Lê o arquivo
    for index, row in data.iterrows():
        world_timestamp = row['world_timestamp']
        world_index = row['world_index']
        fixation_id = int(row['fixation_id'])
        start_timestamp = row['start_timestamp']
        duration = float(row['duration'])
        dispersion = row['dispersion']
        norm_pos_x = float(row['norm_pos_x'])
        norm_pos_y = float(row['norm_pos_y'])
        x_scaled = row['x_scaled']
        y_scaled = row['y_scaled']
        on_surf = row['on_surf']

        y = norm_pos_y * H
        x = norm_pos_x * L
        r = duration / 2

        # Salva os id para criar o plot
        if prev_id != fixation_id:
            ax.scatter(x,y, s=r,color=corC,alpha=0.5)
            
            # Se este não for o primeiro círculo, desenhe uma linha conectando-o ao círculo anterior
            if prev_x is not None and prev_y is not None:
                ax.plot([prev_x,x], [prev_y, y],color=corC,alpha=0.6)
               
            # Escreve o numero
            id += 1
            ax.text(x, y, id, fontsize=tL, color=corL)
        
            # Salve a posição do círculo atual para a próxima iteração
            prev_x = x
            prev_y = y
            prev_id = fixation_id

    plt.axis('off');
    image = cv2.flip(image, 0)
    plt.imshow(image)
    plt.gca().invert_yaxis()
    plt.show()


print('Primeiro leia os arquivos fixation_on_surface e depois a imagem correspondente\n')
print('Em caso de error ou fechar a janela sem querer renicie o terminal \n')
print("Cores disponiveis no site https://matplotlib.org/3.1.0/gallery/color/named_colors.html \n")
    
corC = input("Escreva a cor da circulo: ")
corL = input("Escreva a cor da Letra: ")
tL = input("Escreva o tamanho da letra recomendo 10:")


file_csv = SelecionarCSV()
file_image = SelecionarImagem()

df = LerCSV(file_csv)
PlotGrafico(df, file_image, corC, corL, tL)
