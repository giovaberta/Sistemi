import time
import tornado, asyncio, json
from pymongo import AsyncMongoClient




client  = AsyncMongoClient("localhost",27017)
db = client["publisher_db"]
publishers = db["publishers"]
books = db["books"]


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


class PublishersHandler(tornado.web.RequestHandler):
   async def get(self, pb_id = None):
       if not pb_id:
           dict = {}
           publisher = publishers.find()
           cont = 0
           async for pb in publisher:
               print(pb)
               pb["_id"] = str(pb["_id"])
               cont = cont + 1
               dict[cont]=pb
           self.write(dict)
       else:
           publisher = await publishers.find_one({"_id":pb_id})

def make_app():
  return tornado.web.Application([
      (r"/publishers",PublishersHandler),
      (r"/publishers/(.+)",PublishersHandler)

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
