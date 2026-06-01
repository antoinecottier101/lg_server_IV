import asyncio
import json
import websockets
import os

import time
import random







# Tous les joueurs connectés
clients = set()
player_data = {}



game_on = False
j_limite = 8



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

    global game_on

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


            if data["type"] == "join":

                player_data[websocket]["username"] = data["user"]

                data = {"type" : "chat",
                        "user" : "NARRATOR",
                        "message" : f"{len(clients)} /8 players in the game."}
                await broadcast(data)            
                

                
                if len(clients) >= j_limite and not game_on:

                    game_on = True

                    await broadcast({
                        "type": "chat",
                        "user": "NARRATOR",
                        "message": "La partie commence dans 10 secondes."
                    })

                    await asyncio.sleep(10)

                    await broadcast({
                        "type": "chat",
                        "user": "NARRATOR",
                        "message": "Partie lancée."
                    })



            elif data["type"] == "chat":
                await broadcast(data)

                        




    except:

        print("Déconnexion joueur")

    finally:
                
                clients.discard(websocket)

                await broadcast({"type" : "chat",
                        "user" : "NARRATOR",
                        "message" : f"{player_data[websocket]['username']} s'est déconnecté. \n {len(clients)} / 8 joueurs restants.",})




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
