import asyncio
import json
import websockets
import os


# Tous les joueurs connectés
clients = set()


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

        async for message in websocket:

            print("Message reçu :", message)

            data = json.loads(message)

            # -------------------------
            # CHAT
            # -------------------------

            if data["type"] == "chat":

                await broadcast(data)

            # -------------------------
            # COMMANDES
            # -------------------------

            elif data["type"] == "command":

                command = data["command"]

                print("Commande :", command)

                # EVENT TEST
                if command == "event":

                    await broadcast({

                        "type": "chat",

                        "user": "SERVER",

                        "message": "Meteor shower started!"

                    })

                # TEST NUIT
                elif command == "night":

                    await broadcast({

                        "type": "chat",

                        "user": "SERVER",

                        "message": "Night has started."

                    })

                # TEST BOSS
                elif command == "boss":

                    await broadcast({

                        "type": "chat",

                        "user": "SERVER",

                        "message": "Boss spawned."

                    })


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