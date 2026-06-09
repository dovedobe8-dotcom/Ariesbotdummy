Message Models
==============

Classes for representing messages and message-related events.

Overview
--------

Message models represent the core communication data in fbchat-muqit. Messages can contain text,
mentions, attachments, reactions, and can be replies to other messages.

.. code-block:: python

   from fbchat_muqit import Client, Message, MessageType
   
   async with Client(cookies_file_path="cookies.json") as client:
       # Fetch messages
       messages = await client.fetch_thread_messages(
           thread_id="123456789",
           message_limit=10
       )
       
       for message in messages:
           print(f"{message.sender_id}: {message.text}")
           
           if message.attachments:
               print(f"  Has {len(message.attachments)} attachments")

Message Classes
---------------

Message
~~~~~~~

.. autoclass:: fbchat_muqit.Message
   :members:
   :undoc-members:
   :show-inheritance:

Message Types
~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.MessageType
   :members:
   :undoc-members:

Emoji Size
~~~~~~~~~~

.. autoclass:: fbchat_muqit.EmojiSize
   :members:
   :undoc-members:

Mentions
--------

Mention
~~~~~~~

.. autoclass:: fbchat_muqit.Mention
   :members:
   :undoc-members:

Mentions
~~~~~~~~

.. autoclass:: fbchat_muqit.Mentions
   :members:
   :undoc-members:

Message Events
--------------

Message Reaction
~~~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.MessageReaction
   :members:
   :undoc-members:
   :show-inheritance:

Message Remove
~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.MessageRemove
   :members:
   :undoc-members:
   :show-inheritance:

Message Unsend
~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.MessageUnsend
   :members:
   :undoc-members:
   :show-inheritance:

Reaction Enum
~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.Reaction
   :members:
   :undoc-members:

Usage Examples
--------------

Sending Messages with Mentions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Client, Mention
   
   async with Client(cookies_file_path="cookies.json") as client:
       # Method 1: Manual mention with offset and length
       text = "Hey @John, check this out!"
       mention = Mention(
           user_id="100001234567890",
           offset=4,  # Position where "@John" starts
           length=5   # Length of "@John"
       )
       
       await client.send_message(
           text=text,
           thread_id="123456789",
           mentions=[mention]
       )
       
       # Method 2: Using Mentions.from_text (automatically finds positions)
       from fbchat_muqit import Mentions
       
       text = "Hello Alice and Bob!"
       mentions = Mentions.from_text(
           text=text,
           users=[
               ("100001111111111", "Alice"),
               ("100002222222222", "Bob")
           ]
       )
       
       await client.send_message(
           text=text,
           thread_id="123456789",
           mentions=mentions.users
       )

Working with Message Types
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Message, MessageType
   from fbchat_muqit import ImageAttachment, VideoAttachment, StickerAttachment
   
   async def handle_message(message: Message):
       """Handle different types of messages."""
       
       # Check message type
       if message.message_type == MessageType.TEXT:
           print(f"📝 Text: {message.text}")
       
       elif message.message_type == MessageType.IMAGE:
           print(f"📷 Image message")
           for attachment in message.attachments:
               if isinstance(attachment, ImageAttachment):
                   print(f"   URL: {attachment.preview.url}")
       
       elif message.message_type == MessageType.VIDEO:
           print(f"🎥 Video message")
           for attachment in message.attachments:
               if isinstance(attachment, VideoAttachment):
                   print(f"   Duration: {attachment.playable_duration}ms")
       
       elif message.message_type == MessageType.STICKER:
           print(f"😊 Sticker message")
           for attachment in message.attachments:
               if isinstance(attachment, StickerAttachment):
                   print(f"   Label: {attachment.label}")
       
       elif message.message_type == MessageType.EMOJI:
           print(f"😀 Emoji: {message.text}")
       
       # Check for mentions
       if message.mentions:
           mentioned_users = [m.user_id for m in message.mentions]
           print(f"👥 Mentions: {mentioned_users}")
       
       # Check for reactions
       if message.reaction:
           print(f"❤️ Reactions: {len(message.reaction)}")
       
       # Check if it's a reply
       if message.replied_to_message_id:
           print(f"↩️ Reply to: {message.replied_to_message_id}")

Handling Message Reactions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Client, EventType
   from fbchat_muqit import MessageReaction, Reaction
   
   client = Client(cookies_file_path="cookies.json")
   
   @client.event(EventType.MESSAGE_REACTION)
   async def on_reaction(event: MessageReaction):
       """Handle message reactions."""
       message_id = event.id
       thread_id = event.thread_id.threadFbId
       reactor_id = event.reactor
       reaction = event.reaction
       
       if event.reaction_type == Reaction.ADDED:
           print(f"➕ User {reactor_id} reacted {reaction} to message {message_id}")
           
           # Fetch user info
           users = await client.fetch_user_info(str(reactor_id))
           if str(reactor_id) in users:
               user_name = users[str(reactor_id)].name
               print(f"   Reactor: {user_name}")
           
           # Auto-react back
           await client.react(
               reaction="❤️",
               message_id=message_id,
               thread_id=thread_id
           )
       
       elif event.reaction_type == Reaction.REMOVED:
           print(f"➖ User {reactor_id} removed {reaction} from message {message_id}")

Handling Message Unsend
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import MessageUnsend
   
   @client.event(EventType.MESSAGE_UNSENT)
   async def on_message_unsent(event: MessageUnsend):
       """Handle when someone unsends a message."""
       message_id = event.id
       sender_id = event.sender_id
       thread_id = event.thread_id.threadFbId
       
       print(f"🗑️ Message {message_id} was unsent by {sender_id}")
       
       # Fetch sender info
       users = await client.fetch_user_info(str(sender_id))
       if str(sender_id) in users:
           sender_name = users[str(sender_id)].name
           print(f"   Sender: {sender_name}")
       
       # Log for moderation purposes
       await log_unsent_message(message_id, sender_id, thread_id)

Building a Message Logger
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Client, EventType, Message
   from datetime import datetime
   import json
   
   class MessageLogger:
       """Log all messages to a file."""
       
       def __init__(self, client: Client, log_file: str = "messages.json"):
           self.client = client
           self.log_file = log_file
           self.messages = []
           
           # Register event handler
           self.client.event(EventType.MESSAGE)(self.on_message)
       
       async def on_message(self, message: Message):
           """Log incoming messages."""
           log_entry = {
               'message_id': message.id,
               'thread_id': message.thread_id,
               'sender_id': message.sender_id,
               'text': message.text,
               'timestamp': message.timestamp,
               'message_type': message.message_type.value,
               'has_attachments': bool(message.attachments),
               'attachment_count': len(message.attachments) if message.attachments else 0,
               'has_mentions': bool(message.mentions),
               'mention_count': len(message.mentions) if message.mentions else 0,
               'reaction_count': len(message.reaction) if message.reaction else 0,
               'is_reply': bool(message.replied_to_message_id),
               'logged_at': datetime.now().isoformat()
           }
           
           # Fetch sender name
           users = await self.client.fetch_user_info(message.sender_id)
           if message.sender_id in users:
               log_entry['sender_name'] = users[message.sender_id].name
           
           self.messages.append(log_entry)
           
           # Print summary
           sender = log_entry.get('sender_name', message.sender_id)
           print(f"📝 [{sender}]: {message.text[:50]}")
           
           # Save periodically
           if len(self.messages) % 10 == 0:
               await self.save_logs()
       
       async def save_logs(self):
           """Save logs to file."""
           with open(self.log_file, 'w') as f:
               json.dump(self.messages, f, indent=2)
           print(f"💾 Saved {len(self.messages)} messages to {self.log_file}")
   
   # Usage
   async with Client(cookies_file_path="cookies.json") as client:
       logger = MessageLogger(client)
       await client.listen()

Advanced: Auto-Reply Bot
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Client, EventType, Message
   import re
   
   class AutoReplyBot:
       """Auto-reply bot with keyword detection."""
       
       def __init__(self, client: Client):
           self.client = client
           self.keywords = {
               r'\b(hello|hi|hey)\b': "Hello! How can I help you?",
               r'\b(help|support)\b': "For support, please visit our help center.",
               r'\b(thanks|thank you)\b': "You're welcome! 😊",
               r'\b(bye|goodbye)\b': "Goodbye! Have a great day!"
           }
           
           self.client.event(EventType.MESSAGE)(self.on_message)
       
       async def on_message(self, message: Message):
           """Auto-reply to messages with keywords."""
           # Skip own messages
           if message.sender_id == self.client.uid:
               return
           
           text = message.text.lower()
           
           # Check for keywords
           for pattern, reply in self.keywords.items():
               if re.search(pattern, text, re.IGNORECASE):
                   # Send auto-reply
                   await self.client.send_message(
                       text=reply,
                       thread_id=message.thread_id
                   )
                   
                   print(f"🤖 Auto-replied to {message.sender_id}")
                   break
   
   # Usage
   async with Client(cookies_file_path="cookies.json") as client:
       bot = AutoReplyBot(client)
       await client.listen()

Working with Message Chains
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Message
   
   async def get_conversation_thread(
       client: Client,
       message: Message,
       max_depth: int = 10
   ) -> list[Message]:
       """Get the full conversation thread for a message."""
       thread = [message]
       current = message
       depth = 0
       
       # Follow reply chain backwards
       while current.replied_to_message_id and depth < max_depth:
           replied_msg = await client.fetch_message_info(
               current.replied_to_message_id,
               current.thread_id
           )
           
           if replied_msg:
               thread.insert(0, replied_msg)
               current = replied_msg
               depth += 1
           else:
               break
       
       return thread
   
   # Usage
   message = await client.fetch_message_info(msg_id, thread_id)
   conversation = await get_conversation_thread(client, message)
   
   print("Conversation thread:")
   for i, msg in enumerate(conversation, 1):
       print(f"{i}. {msg.sender_id}: {msg.text}")

See Also
--------

- :doc:`attachment` - Attachment models
- :doc:`thread` - Thread models
- :doc:`timestamps` - Timestamp events
- :doc:`../client` - Client methods for sending messages
- :doc:`/guides/sending-messages` - Guide on sending messages
