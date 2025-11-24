import tornado, asyncio, bson
from pymongo import AsyncMongoClient
from bson import ObjectId

"""Serie di comandi che vanno ad iniziallizzare il database di mongo e se non è inizilizzato lo fa"""
client  = AsyncMongoClient("localhost",27017)
db = client["publisher_db"]
publishers = db["publishers"]
books = db["books"]

#Funzioni per l'inserimento dei libri su mongo
async def insert_book():
   await books.insert_many([
           {
               "title": "Se una notte d'inverno un viaggiatore",
               "author": "Italo Calvino",
               "genre": "Romanzo",
               "year": 1979,
               "publisher_id": "OBJECT_ID_EINAUDI"
           },
           {
               "title": "Il nome della rosa",
               "author": "Umberto Eco",
               "genre": "Giallo",
               "year": 1980,
               "publisher_id": "OBJECT_ID_EINAUDI"
           },
           {
               "title": "Il codice da Vinci",
               "author": "Dan Brown",
               "genre": "Giallo",
               "year": 2003,
               "publisher_id": "OBJECT_ID_PENGUIN"
           },
           {
               "title": "Harry Potter e la pietra filosofale",
               "author": "J.K. Rowling",
               "genre": "Fantasy",
               "year": 1997,
               "publisher_id": "OBJECT_ID_PENGUIN"
           },
           {
               "title": "Il signore degli anelli",
               "author": "J.R.R. Tolkien",
               "genre": "Fantasy",
               "year": 1954,
               "publisher_id": "OBJECT_ID_PENGUIN"
           },
           {
               "title": "1984",
               "author": "George Orwell",
               "genre": "Romanzo",
               "year": 1949,
               "publisher_id": "OBJECT_ID_MONDADORI"
           },
           {
               "title": "Hunger Games",
               "author": "Suzanne Collins",
               "genre": "Fantasy",
               "year": 2008,
               "publisher_id": "OBJECT_ID_MONDADORI"
           },
           {
               "title": "La ragazza del treno",
               "author": "Paula Hawkins",
               "genre": "Giallo",
               "year": 2015,
               "publisher_id": "OBJECT_ID_MONDADORI"
           },
           {
               "title": "Harry Potter e il prigioniero di Azkaban",
               "author": "J.K. Rowling",
               "genre": "Fantasy",
               "year": 1999,
               "publisher_id": "OBJECT_ID_HARPERCOLLINS"
           },
           {
               "title": "Il piccolo principe",
               "author": "Antoine de Saint-Exupéry",
               "genre": "Romanzo",
               "year": 1943,
               "publisher_id": "OBJECT_ID_HARPERCOLLINS"
           },
           {
               "title": "Il vecchio e il mare",
               "author": "Ernest Hemingway",
               "genre": "Romanzo",
               "year": 1952,
               "publisher_id": "OBJECT_ID_HARPERCOLLINS"
           },
           {
               "title": "Sostiene Pereira",
               "author": "Antonio Tabucchi",
               "genre": "Romanzo",
               "year": 1994,
               "publisher_id": "OBJECT_ID_FELTRINELLI"
           },
           {
               "title": "La ragazza del treno",
               "author": "Paula Hawkins",
               "genre": "Giallo",
               "year": 2015,
               "publisher_id": "OBJECT_ID_FELTRINELLI"
           },
           {
               "title": "Cecità",
               "author": "José Saramago",
               "genre": "Romanzo",
               "year": 1995,
               "publisher_id": "OBJECT_ID_FELTRINELLI"
           }
       ])
async def insert_publishers():
   await publishers.insert_many([
       {
           "name": "Einaudi",
           "founded_year": 1933,
           "country": "Italia"
       },
       {
           "name": "Penguin Random House",
           "founded_year": 2013,
           "country": "USA"
       },
       {
           "name": "Mondadori",
           "founded_year": 1907,
           "country": "Italia"
       },
       {
           "name": "HarperCollins",
           "founded_year": 1989,
           "country": "USA"
       },
       {
           "name": "Feltrinelli",
           "founded_year": 1954,
           "country": "Italia"
       }
   ])

#Classe derivata del Request Handelr di tornado
class PublishersHandler(tornado.web.RequestHandler):
    #Gestione delle richioeste http di tipo get
    async def get(self, pb_id = None):
        #Se non viene inserite nell url un publisher_id(pd_id) stampo tutti quelli presenti
        if not pb_id:
            dict = {}
            publisher = publishers.find()
            cont = 0
            async for pb in publisher:
                pb["_id"] = str(pb["_id"])
                cont = cont + 1
                dict[cont] = pb
            self.set_status(201)
            self.write(dict)
        #Codice che viene eseguto se c'è un id
        else:
            try:
            #Provo a ricercare il publisher con id dato e se lo trovo lo invio
                publisher = await publishers.find_one({"_id":ObjectId(pb_id)})
                publisher["_id"] = str(publisher["_id"])
                self.set_status(201)
                self.write(publisher)
            #Se l'id non è presente nel datbase gestisco l'errore sollevto da mongo
            except bson.errors.InvalidId:
                self.set_status(404)
                self.write("Id not found")

    #Gestione delle richioeste http di tipo post (Inserimento di un nuovo publisher)
    async def post(self):
        #Dichiaro che il server risponderà con un application/json
        self.set_header("Content-Type", "application/json")
        #Ricavo i dati che si trovavano nel body della request
        data = tornado.escape.json_decode(self.request.body)
        #Provo a inserire il contenuto nel database
        try:
            await publishers.insert_one(data)
            self.set_status(203)
        #Se si genera un qualsiasi errore fermo l'inserimento mando un mesaggio di "error" al client
        except Exception:
            self.set_status(400)
            self.write("Error")

    #Gestione delle richioeste http di tipo put (Aggiornamento dati)
    async def put(self, pb_id):
        # Dichiaro che il server risponderà con un application/json
        self.set_header("Content-Type", "application/json")
        # Ricavo i dati che si trovavano nel body della request
        data = tornado.escape.json_decode(self.request.body)
        #Verifico che il id sia coretto se no gestisco l'eccezione
        try:
            publisher = await publishers.find_one({"_id":ObjectId(pb_id)})
        except bson.errors.InvalidId:
            self.set_status(400)
            self.write("id not found")
            return
        #Quando sono stati fatti tutti i controlli inserico il nuovo publisher nel database
        await publishers.update_one({"_id": ObjectId(pb_id)}, { "$set" :data})
        self.set_status(203)

    # Gestione delle richioeste http di tipo delete (Eliminare dati)
    async def delete(self, pb_id):
        #Provo ad eliminaere il publisher e se non lo trova mando un errore
        ris = await publishers.delete_one({"_id":ObjectId(pb_id)})
        if ris["n"] == 1:
            self.set_status(203)
        else:
            self.set_status(404)
            self.write("id not found")

#Classe derivata del Request Handelr di tornado
class BooksHandler(tornado.web.RequestHandler):
    #Gestione delle richioeste http di tipo get
    async def get(self, pb_id, bo_id = None):
        if not pb_id:
            self.set_status(400)
            self.write("Bad Request")
        #Controllo che il publisher esiste se no gestisco l'eccezione sollevata
        try:
            publisher = await publishers.find_one({"_id" : ObjectId(pb_id)})
            name = "OBJECT_ID_" + publisher["name"].upper()
        except bson.errors.InvalidId:
            self.set_status(401)
            self.write("Id publisher errato")
            return
        if not bo_id:
            #Cerco tutti i libri di quel publisher
            dizz_libri = {}
            cont = 0
            libri = books.find({"publisher_id":name})
            async for lib in libri:
                cont += 1
                lib["_id"] = str(lib["_id"])
                dizz_libri[cont] = lib
                self.write(dizz_libri)
        else:
            try:
            #Provo a ricercare il publisher con id dato e se lo trovo lo invio
                book = await books.find_one({"_id":ObjectId(bo_id)})
                book["_id"] = str(book["_id"])
                self.set_status(201)
                self.write(book)
            #Se l'id non è presente nel datbase gestisco l'errore sollevto da mongo
            except bson.errors.InvalidId:
                self.set_status(404)
                self.write("Id not found")


    async def post(self,pb_id):
        # Dichiaro che il server risponderà con un application/json
        self.set_header("Content-Type", "application/json")
        # Ricavo i dati che si trovavano nel body della request
        data = tornado.escape.json_decode(self.request.body)
        if not pb_id:
            self.set_status(400)
            self.write("Bad Request")
        #Controllo che esista il publisher
        try:
            publisher = await publishers.find_one({"_id": ObjectId(pb_id)})
            name = "OBJECT_ID_" + publisher["name"].upper()
        except bson.errors.InvalidId:
            self.set_status(401)
            self.write("Id publisher errato")
            return
        data["publisher_id"] = name
        await books.insert_one(data)
        self.set_status(203)

    async def put(self, pb_id ,bo_id):
        # Dichiaro che il server risponderà con un application/json
        self.set_header("Content-Type", "application/json")
        # Ricavo i dati che si trovavano nel body della request
        data = tornado.escape.json_decode(self.request.body)
        if not pb_id:
            self.set_status(400)
            self.write("Bad Request")
        # Controllo che esista il publisher e il libro
        try:
            await books.find_one({"_id":ObjectId(bo_id)})
            publisher = await publishers.find_one({"_id": ObjectId(pb_id)})
            name = "OBJECT_ID_" + publisher["name"].upper()
            data["publisher_id"] = name
        except bson.errors.InvalidId:
            self.set_status(401)
            self.write("Id book errato")
            return
        #Aggiorno il libro nel database
        await books.update_one({"_id":ObjectId(bo_id)},{"&set":data})
        self.set_status(203)

    async def delete(self,pb_id,bo_id):
        if not pb_id:
            self.set_status(400)
            self.write("Bad Request")
        # Controllo che esista il publisher e il libro
        try:
            await books.find_one({"_id":ObjectId(bo_id)})
            await publishers.find_one({"_id": ObjectId(pb_id)})
        except bson.errors.InvalidId:
            self.set_status(401)
            self.write("Id book errato")
            return
        #Elimino il libro
        ris = await books.delete_one({"_id": ObjectId(bo_id)})
        if ris["n"] == 1:
            self.set_status(203)
        else:
            self.set_status(404)
            self.write("id not found")

def make_app():
  return tornado.web.Application([
      #I primi due url fanno capo alla classe PublishersHandler
      (r"/publishers",PublishersHandler),
      (r"/publishers/([a-f0-9]+)",PublishersHandler),
      #Gli altri due url fanno capo alla classe BooksHandler
      (r"/publishers/([a-f0-9]+)/books",BooksHandler),
      (r"/publishers/([a-f0-9]+)/books/([a-f0-9]+)",BooksHandler),

  ])
async def main(shutdown_event):
    app = make_app()
    app.listen(8888)
    #Comandi da inserire solo al primo avvio
    #await insert_book()
    #await insert_publishers()
    print("Server in ascolto su http://localhost:8888/publishers")
    await shutdown_event.wait()
    print("Shutdown ricevuto, chiusura server...")

if __name__ == "__main__":
   shutdown_event = asyncio.Event()
   try:
       asyncio.run(main(shutdown_event))
   except KeyboardInterrupt:
       shutdown_event.set()
