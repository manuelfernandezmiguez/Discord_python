import pymongo
import pprint

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["brawl-starts_liga"]
print(db)
mycollection = db["partidos"]
mycollection2 = db["equipos"]
print(mycollection)
one_record = mycollection.find_one()
print(one_record)
all_records=mycollection.find()
i=0
#for row in all_records:
 #   if(i!=0):
  #      print(row)
   # i+=1

def insertar(nome1,nome2):
    myDocument = {
        "equipo1":nome1,
        "equipo2":nome2,
        "gañador": None
    }
    id = mycollection.insert_one(myDocument).inserted_id
    print(id)
#equipo1 = input('¿Cal é o nome do primeiro equipo?')
#equipo2 = input('¿Cal é o nome do segundo equipo?')
#insertar(equipo1,equipo2)
printer = pprint.PrettyPrinter()
def buscar_equipos():
    equipos=mycollection2.find()
    for equipo in equipos:
        printer.pprint(equipo)

def buscar_equipos_por_nome(nome: str):
    equipos=list(mycollection.find({"equipo1":nome}))
    equipos2=list(mycollection.find({"equipo2":nome}))
    equipoXeneral=equipos+equipos2
    for equipo in equipoXeneral:
        printer.pprint(equipo)

def project_columns():
    columns = {"_id":0, "nome":2,"puntos":2}
    equipos = list(mycollection2.find({},columns).sort("puntos",pymongo.DESCENDING))
    return equipos

def actualizar_victoria(nome: str):

    retorno=mycollection2.update_one({
        'nome': nome
        },{
        '$inc': {
            'puntos': 1
                }
    }, upsert=False).raw_result
    return retorno
#actualizar_victoria("eLes")
buscar_equipos_por_nome("eLes")
