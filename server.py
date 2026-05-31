import asyncio
import json
import websockets
import os

import time
import random







# Tous les joueurs connectés
clients = set()
player_data = {}



n_players = 0
game_on = False




async def broadcast(packet):

    if len(clients) <= 0:
        return

    message = json.dumps(packet)
    disconnected = set()
    for client in clients:
        try:
            await client.send(message)
        except:
            disconnected.add(client)
    clients.difference_update(disconnected)


async def handler(websocket):
    print("Joueur connecté")
    clients.add(websocket)
    try:


        player_data[websocket] = {
        "username": "Unknown",
        "rating": 0,
        "silver": 0
        }



        async for message in websocket:
            print("Message reçu :", message)
            data = json.loads(message)

            # -------------------------
            # CHAT
            # -------------------------

            if data["type"] == "chat":
                await broadcast(data)



            if data["type"] == "join":
                n_players += 1
                data = {"type" : "chat",
                        "user" : "NARRATOR",
                        "message" : f"{n_players} /8 players in the game."}
                await broadcast(data)            
                if n_players >= 0:
                    await asyncio.sleep(10)
                    if n_players >= 0:
                        data = {"type" : "chat",
                                "user" : "NARRATOR",
                                "message" : "Partie lancée."}
                        await broadcast(data)
                        game_on = True
                        

            

            # -------------------------
            # COMMANDES
            # -------------------------

            # elif data["type"] == "command":

            #     command = data["command"]

            #     print("Commande :", command)

            #     # EVENT TEST
            #     if command == "event":

            #         await broadcast({

            #             "type": "chat",

            #             "user": "SERVER",

            #             "message": "Meteor shower started!"

            #         })



    except:

        print("Déconnexion joueur")

    finally:

        clients.remove(websocket)



PORT = int(os.environ.get("PORT", 8080))


async def main():

    async with websockets.serve(
        handler,
        "0.0.0.0",
        PORT
    ):

        print("Serveur websocket online")
        await asyncio.Future()


asyncio.run(main())
asyncio.run(main())
