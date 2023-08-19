# from channels.consumer import AsyncConsumer
# import json

# class BoardConsumer(AsyncConsumer):

#     async def websocket_connect(self, event):
#         board_room = "boardroom"
#         self.borad_room = board_room

#         # Add the consumer to the group
#         await self.channel_layer.group_add(
#             board_room, self.channel_name
#         )

#         await self.send({
#             "type": "websocket.accept",
#         })

#     async def websocket_receive(self, event):
#         initial_data = event.get("text", None)

#         # Send the message to the group
#         await self.channel_layer.group_send(
#             self.borad_room, {
#                 "type": "board_message",
#                 "text": initial_data
#             }
#         )

#     async def board_message(self, event):
#         data = event['initial_data']
#         # Send the message to the WebSocket
#         await self.send(text_data=json.dumps(data))

#     async def websocket_disconnect(self, event):
#         print("Disconnect", event)

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Whiteboard, Drawing, Action


class BoardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.whiteboard_group_name = "whiteboard_group"
        self.whiteboard_id = self.scope['url_route']['kwargs']['whiteboard_id']

        await self.channel_layer.group_add(
            self.whiteboard_group_name, self.channel_name
        )

        await self.send(
            {
                "type": "websocket.accept",
            }
        )


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.whiteboard_group_name, self.channel_name
        )


    async def receive(self, text_data):

        data = json.loads(text_data)

        # Broadcast the drawing instruction to all clients
        await self.channel_layer.group_send(
            self.whiteboard_group_name, {"type": "draw_message", "data": data}
        )
        

    async def draw_message(self, event):
        data = event["data"]

        action_type = data.get('action_type')

        # Save the action to the database
        whiteboard_id = self.whiteboard_id
        drawing_obj , created = Drawing.objects.get_or_create(whiteboard_id=whiteboard_id)

        user = self.scope['user']  # Assuming authentication is enabled

        # Ensure action_type is valid
        if action_type in dict(Action.ActionType.choices):
                
                #we need to write pydantic validation here for type line and shape and text
                
                # Calculate the new index_number based on the last action
                last_action = Action.objects.filter(drawing=drawing_obj).last()
                new_index_number = (last_action.index_number + 1) if last_action else 1

                action_obj = Action.objects.create(
                drawing=drawing_obj,
                user=user,
                action_type=action_type,
                data=data,
                index_number = new_index_number
                
            )


        # Send the drawing instruction to the client
        await self.send(text_data=json.dumps(data))



    async def handle_websocket_message(self, event):
        message = json.loads(event["text"])

        if message["type"] == "undo":
            await self.handle_undo_action()

        if message["type"] == "redo":
            await self.handle_redo_action()
