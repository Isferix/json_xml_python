#!/usr/bin/env python
'''
Hackerrank [Python]
Ejercicios de clase
---------------------------
Autor: Ishef Glatzel
Version: 1.0

Descripcion:
Resolucion del ejercicio de Hacker Rank, 
planteado en el archivo: ejercicio_hackerrank.md
'''
__author__ = "Ishef Glatzel"
__email__ = "ishefglatzel@gmail.com"
__version__ = "1.0"

import numpy as np
import re

import json
import requests

import matplotlib.pyplot as plt
import matplotlib.axes
import seaborn as sns


def fetch(page_number, location_id):
    """
    Funcion encargada de extraer los datos a traves de un json de la url\n
    @param page_number: Indica el Nº de pagina donde se buscara la informacion\n
    @param location_id: Indica el ID a buscar\n
    return: Retorna una lista de listas con el formato:\n
        {'userId' : userId, 'amount' : amount}
    """

    url = "https://jsonmock.hackerrank.com/api/transactions/search?txnType=debit&page={}".format(page_number)
    response = requests.get(url)
    dataset = response.json()
    dataset_neto = dataset["data"]
    return [{'userId': data["userId"], 'amount': data["amount"]} for data in dataset_neto if data["location"]["id"] == location_id]


def transform(dataset):
    '''
    Transforma la lista de diccionarios en numeros concretos asociados a la id del usuario\n
    @param dataset: Compendio de datos a transformar\n
    return: Retorna una lista de tuplas con el formato (Id, Monto)
    '''
    usuarios = []
    monto = []
    for diccionario in dataset:
        if diccionario['userId'] not in usuarios:
            usuarios.append(diccionario['userId'])
            monto.append(0)
        monto[usuarios.index(diccionario['userId'])] += float(re.sub(r'[^\d\-.]', '', diccionario['amount']))
    return list(zip(usuarios, monto))


def report(data):
    '''
    Representa graficamente los datos a traves de un grafico de barras\n
    @param data: Lista con los datos netos de los que se extraeran los valores a graficar
    '''
    x = [x[0] for x in data]
    y = [y[1] for y in data]

    fig = plt.figure(figsize=(10,5))
    fig.suptitle('Registro Transacciones', fontsize=16)
    paleta = sns.color_palette('muted', n_colors=len(x))
    for i in range(len(x)):
        exec('ax{} = fig.add_subplot(len(x), 1, {})'.format(i,i+1))
        exec("sns.barplot(y[{}],label='Transaccion {} - ${}',color=paleta[i], ax=ax{})".format(i,i+1,y[i],i))
        exec("ax{}.set_facecolor('whitesmoke')".format(i))
        exec('ax{}.legend()'.format(i))

        scale_factor = sum(y) / y[i]   
        xmin, xmax = plt.xlim()
        plt.xlim(xmin * scale_factor, xmax * scale_factor)
    
    plt.show()

if __name__ == "__main__":
    dataset = fetch(4, 1)
    data = transform(dataset)
    report(data)
