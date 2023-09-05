# drive/consumers.py
import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import File  # Import your File model
from django.contrib.auth.models import User

class FileShareConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data['type'] == 'share_file':
            file_id = data['file_id']
            target_username = data['target_username']
            try:
                file = File.objects.get(pk=file_id)
                target_user = User.objects.get(username=target_username)

                # Check if the file exists and the target user exists
                if file and target_user:
                    # Check if the file belongs to the sender
                    if file.folder.owner == self.scope['user']:
                        # Implement your file sharing logic here
                        # You can update the database or perform the necessary actions
                        # For simplicity, let's assume the file is shared successfully
                        await self.send(text_data=json.dumps({
                            'type': 'file_shared',
                            'message': f'File shared: {file.filetitle}',
                        }))
                    else:
                        await self.send(text_data=json.dumps({
                            'type': 'error',
                            'message': 'You do not have permission to share this file.',
                        }))
                else:
                    await self.send(text_data=json.dumps({
                        'type': 'error',
                        'message': 'File or target user not found.',
                    }))
            except File.DoesNotExist:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'File not found.',
                }))
            except User.DoesNotExist:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'Target user not found.',
                }))
