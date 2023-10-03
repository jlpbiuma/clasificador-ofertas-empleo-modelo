# Diccionarios

## Definición

Se definen por ser la fuente de los datos con los que se van a ir contrastando las palabras de las ofertas

## Sustantivos y adjetivos

Estos dos diccionarios cuenta con dos posibles fuentes de datos:

1. List_unstructured: Una lista con todas las formas e infinitivos (aquí se buscará)
2. Df_structured (FORMA, LEMA): Un dataframe con el que conociendo el índice de la conjugación encontrada en la lista desordenada se puede normalizar a su lexema

## Verbos

En el caso de los verbos también tenemos dos fuentes de datos.

1. List_unstructured: Exactamente mismo caso que el anterior
2. Df_structured (FORMA, INF): Misma filosofía de lógica que el caso anterior pero en esta fuente se debe de normalizar a su forma en "Infinitivo Simple"
