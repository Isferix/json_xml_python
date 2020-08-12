#!/usr/bin/env python
'''
Mercado Libre [Python]
Ejercicios de clase
---------------------------
Autor: Ishef Glatzel
Version: 1.0

Descripcion:
Resolucion del ejercicio de Mercado Libre, 
planteado en el archivo: ejercicio_meli.md
'''
__author__ = "Ishef Glatzel"
__email__ = "ishefglatzel@gmail.com"
__version__ = "1.0"

import requests
import json

import matplotlib.pyplot as plt
import matplotlib.axes

def fetch():
    '''
    Funcion encargada de extraer los datos a traves de un json de la url\n
    return: Retorna una lista de diccionarios con el formato:\n
        {'price' : price, 'condition' : condition}
    '''
    url = 'https://api.mercadolibre.com/sites/MLA/search?category=MLA1459&q=Departamentos%20Alquilers%20Mendoza%20&limit=50'
    response = requests.get(url)
    dataset = response.json()
    dataset_neto = dataset['results']
    filtrado_1 = [{"price": data["price"], "condition": data["condition"]} for data in dataset_neto if data["currency_id"] == "ARS"]
    return filtrado_1


def transform(dataset, minimo, maximo):
    '''
    Clasifica los datos obtenidos en 3 listas segun hayan estado debajo, dentro o fuera del rango especificado\n
    @param dataset: Compendio de datos a clasificar\n
    @param minimo: Entero que indica el minimo del rango de la busqueda\n
    @param maximo: Entero que indica el limite del rango de la busqueda\n
    return: Retorna una lista de enteros con el formato:
        [len(lista_min), len(lista_min_max), len(lista_max)]
    '''
    lista_min = [data['price'] for data in dataset if data["price"] < minimo]
    lista_min_max = [data['price'] for data in dataset if minimo <= data["price"] <= maximo]
    lista_max = [data['price'] for data in dataset if data["price"] > maximo]
    # Todas las listas guardan los valores de los precios para que en caso de debug sea facil detectar errores
    # el programa funciona correctamente si en vez de data['price'] se reemplaza por la expresion data

    return [len(lista_min), len(lista_min_max), len(lista_max)]


def report(data):
    '''
    Representa graficamente los datos a traves de un grafico de barras\n
    @param data: Lista con los datos netos de los que se extraeran los valores a graficar
    '''
    fig = plt.figure()
    fig.suptitle('Reparto del precio de alquileres', fontsize=16)
    ax = fig.add_subplot()

    ax.pie(data, labels=['Alquileres por debajo del min', 'Alquileres dentro del rango', 'Alquileres que superan el rango'],
           autopct='%1.0f%%', shadow=True, startangle=90
           )
    ax.axis('equal')
    plt.show()


if __name__ == "__main__":
    minimo = int(input("Presupuesto minimo: "))
    maximo = int(input("Presupuesto maximo: "))

    dataset = fetch()
    data = transform(dataset, minimo, maximo)
    report(data)