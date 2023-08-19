from django.test import TestCase
from channels.testing import WebsocketCommunicator
from whiteboard.consumer import BoardConsumer


class WhiteboardConsumerTests(TestCase):
    async def test_whiteboard_consumer(self):
        communicator = WebsocketCommunicator(BoardConsumer.as_asgi(), "")

        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)

        try:
            # Send a drawing instruction
            await communicator.send_json_to(
                {
                    "startX": 100,
                    "startY": 100,
                    "endX": 200,
                    "endY": 200,
                    "color": "#000000",
                    "thickness": 2,
                }
            )

            # Receive the response from the consumer
            response = await communicator.receive_json_from()

            # Assert the response matches the sent instruction
            expected_response = {
                "startX": 100,
                "startY": 100,
                "endX": 200,
                "endY": 200,
                "color": "#000000",
                "thickness": 2,
            }
            # import pdb
            # pdb.set_trace()

            self.assertEqual(response, expected_response)
        finally:
            # Disconnect the communicator
            await communicator.disconnect()
