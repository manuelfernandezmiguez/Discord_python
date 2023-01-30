import pymongo
import discord
import os # default module
import random
from datetime import datetime

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["brawl-starts_liga"]
mycollection = db["partidos"]
mycollection2 = db["equipos"]

def clasificacion(ctx):
    return ctx.respond(project_columns())




def tirar(ctx,caras: int,numero: int ):
    random.seed(datetime.now().timestamp())
    aleatorio=0
    for i in numero:
        aleatorio +=random.randint(1, caras)
    return ctx.respond(aleatorio)

def project_columns():
    columns = {"_id":0, "nome":1,"puntos":1}
    equipos = list(mycollection2.find({},columns).sort("puntos",pymongo.DESCENDING))
    devolto="esta é a lista dos equipos por puntos:"+"\n"
    lista=["1º Posicion","2º Posicion","3º Posicion","4º Posicion","5º Posicion","6º Posicion"]
    i=0
    valT=" "
    for equipo in equipos:
        valT= lista[i]+" : "
        for key, val in equipo.items():
            valT+=str(val)+"\t"
        devolto+= valT + "\n"
        i+=1
    return devolto


