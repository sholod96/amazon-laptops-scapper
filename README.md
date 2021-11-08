---
title: "uoc-datascrapping-amazon: Datos sobre portátiles de Amazon"
author: "Sofia Holod"
date: "8 de Noviembre de 2021"
---

# Ficheros

## Doc

* PDF

## Código

* Crawlers:
  * base_crawler.
  * amazon_crawler.
* Models:
  * article.

* main.py: fichero principal, su ejecución da lugar a la base de datos ejecutando todos los crawlers.

## Datos

* amazon_laptops_dataset

# Instalación 

## Requirements

* python version > 3.8

```bash
python -m venv venv
venv\bin\pip -r install requirements.txt
```

# Ejecución

```bash
make
```
o 

```bash
venv/bin/python  main.py
```
