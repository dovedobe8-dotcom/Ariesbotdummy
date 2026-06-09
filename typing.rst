Typing Models
=============

Classes for representing typing indicator events.

Overview
--------

Typing models track when users are typing in threads. These events help create
a more interactive chat experience by showing real-time typing indicators.

.. code-block:: python

   from fbchat_muqit import Client, EventType
   from fbchat_muqit import Typing
   
   client = Client(cookies_file_path="cookies.json")
   
   @client.event(EventType.TYPING)
   async def on_typing(typing: Typing):
       if typing.is_typing:
           print(f"✍️  User {typing.user_id} is typing in thread {typing.thread_id}")
       else:
           print(f"⏸️  User {typing.user_id} stopped typing")

Typing Class
------------

.. autoclass:: fbchat_muqit.Typing
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
--------------

Monitoring Typing Activity
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Client, EventType
   from fbchat_muqit import Typing
   
   client = Client(cookies_file_path="cookies.json")
   
   # Track who is typing
   currently_typing = {}
   
   @client.event(EventType.TYPING)
   async def on_typing(typing: Typing):
       """Monitor typing indicators."""
       user_id = typing.user_id
       thread_id = typing.thread_id
       is_typing = typing.is_typing
       
       # Fetch user info
       users = await client.fetch_user_info(user_id)
       user_name = users[user_id].name if user_id in users else user_id
       
       if is_typing:
           currently_typing[thread_id] = user_name
           print(f"✍️  {user_name} is typing in thread {thread_id}...")
       else:
           if thread_id in currently_typing:
               print(f"⏸️  {user_name} stopped typing")
               del currently_typing[thread_id]

Sending Typing Indicators
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Client, ThreadType
   import asyncio
   
   async with Client(cookies_file_path="cookies.json") as client:
       thread_id = "123456789"
       
       # Show typing indicator
       await client.typing(
           thread_id=thread_id,
           is_typing=True,
           thread_type=ThreadType.USER
       )
       
       # Simulate composing a message
       await asyncio.sleep(3)
       
       # Send the message
       await client.send_message(
           "Hello! I was just typing this message 😊",
           thread_id=thread_id
       )
       
       # Stop typing indicator
       await client.typing(
           thread_id=thread_id,
           is_typing=False,
           thread_type=ThreadType.USER
       )

Auto Typing Indicator
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Client, EventType, Message, ThreadType
   import asyncio
   
   class AutoTypingBot:
       """Automatically show typing indicator before replying."""
       
       def __init__(self, client: Client, typing_duration: float = 2.0):
           self.client = client
           self.typing_duration = typing_duration
           
           self.client.event(EventType.MESSAGE)(self.on_message)
       
       async def on_message(self, message: Message):
           """Show typing indicator before replying."""
           # Skip own messages
           if message.sender_id == self.client.uid:
               return
           
           # Check if message needs a reply (simple keyword check)
           text = message.text.lower()
           if any(word in text for word in ['hello', 'hi', 'hey']):
               # Show typing indicator
               await self.client.typing(
                   thread_id=message.thread_id,
                   is_typing=True,
                   thread_type=message.thread_type
               )
               
               # Wait a bit (simulate thinking/typing)
               await asyncio.sleep(self.typing_duration)
               
               # Send reply
               await self.client.send_message(
                   "Hello! How can I help you? 😊",
                   thread_id=message.thread_id
               )
               
               # Stop typing indicator
               await self.client.typing(
                   thread_id=message.thread_id,
                   is_typing=False,
                   thread_type=message.thread_type
               )
   
   # Usage
   async with Client(cookies_file_path="cookies.json") as client:
       bot = AutoTypingBot(client, typing_duration=2.0)
       await client.listen()


Smart Typing Simulation
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Client, ThreadType
   import asyncio
   import random
   
   class SmartTypingSimulator:
       """Simulate realistic typing patterns."""
       
       def __init__(self, client: Client):
           self.client = client
       
       async def simulate_typing_for_message(
           self,
           message: str,
           thread_id: str,
           thread_type: ThreadType = ThreadType.USER,
           wpm: int = 40  # Words per minute
       ):
           """Simulate typing based on message length."""
           # Calculate typing duration based on message length and WPM
           word_count = len(message.split())
           typing_duration = (word_count / wpm) * 60  # Convert to seconds
           
           # Add some randomness (±20%)
           typing_duration *= random.uniform(0.8, 1.2)
           
           # Cap at reasonable limits
           typing_duration = max(1.0, min(typing_duration, 10.0))
           
           print(f"✍️  Simulating typing for {typing_duration:.1f}s...")
           
           # Start typing
           await self.client.typing(
               thread_id=thread_id,
               is_typing=True,
               thread_type=thread_type
           )
           
           # Wait
           await asyncio.sleep(typing_duration)
           
           # Send message
           await self.client.send_message(message, thread_id=thread_id)
           
           # Stop typing
           await self.client.typing(
               thread_id=thread_id,
               is_typing=False,
               thread_type=thread_type
           )
       
       async def simulate_typing_with_pauses(
           self,
           message: str,
           thread_id: str,
           thread_type: ThreadType = ThreadType.USER
       ):
           """Simulate realistic typing with pauses."""
           # Start typing
           await self.client.typing(
               thread_id=thread_id,
               is_typing=True,
               thread_type=thread_type
           )
           
           # Simulate typing with random pauses
           words = message.split()
           for i, word in enumerate(words):
               # Random pause between words (0.1-0.5s)
               await asyncio.sleep(random.uniform(0.1, 0.5))
               
               # Occasionally pause longer (thinking)
               if random.random() < 0.2:  # 20% chance
                   print("   💭 (thinking pause)")
                   await asyncio.sleep(random.uniform(1.0, 2.0))
           
           # Final pause before sending
           await asyncio.sleep(0.5)
           
           # Send message
           await self.client.send_message(message, thread_id=thread_id)
           
           # Stop typing
           await self.client.typing(
               thread_id=thread_id,
               is_typing=False,
               thread_type=thread_type
           )
   
   # Usage
   async with Client(cookies_file_path="cookies.json") as client:
       simulator = SmartTypingSimulator(client)
       
       # Simulate realistic typing
       await simulator.simulate_typing_for_message(
           message="Hello! How are you doing today?",
           thread_id="123456789",
           wpm=45  # Typing speed
       )
       
       # Or with natural pauses
       await simulator.simulate_typing_with_pauses(
           message="This message has natural pauses between words",
           thread_id="123456789"
       )

Typing Notification System
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Client, EventType, Typing
   import asyncio
   
   class TypingNotificationSystem:
       """Advanced typing notification system."""
       
       def __init__(self, client: Client):
           self.client = client
           self.typing_timers = {}  # thread_id -> asyncio.Task
           
           self.client.event(EventType.TYPING)(self.on_typing)
       
       async def on_typing(self, typing: Typing):
           """Handle typing with timeout."""
           thread_id = typing.thread_id
           user_id = typing.user_id
           is_typing = typing.is_typing
           
           # Fetch user info
           users = await self.client.fetch_user_info(user_id)
           user_name = users[user_id].name if user_id in users else user_id
           
           if is_typing:
               # Cancel existing timer
               if thread_id in self.typing_timers:
                   self.typing_timers[thread_id].cancel()
               
               # Show notification
               print(f"✍️  {user_name} is typing...")
               
               # Set timeout (auto-hide after 5 seconds)
               self.typing_timers[thread_id] = asyncio.create_task(
                   self.typing_timeout(thread_id, user_name)
               )
           else:
               # Cancel timer
               if thread_id in self.typing_timers:
                   self.typing_timers[thread_id].cancel()
                   del self.typing_timers[thread_id]
               
               print(f"⏸️  {user_name} stopped typing")
       
       async def typing_timeout(self, thread_id: str, user_name: str):
           """Auto-hide typing indicator after timeout."""
           try:
               await asyncio.sleep(5)
               print(f"⏱️  Typing indicator for {user_name} timed out")
               if thread_id in self.typing_timers:
                   del self.typing_timers[thread_id]
           except asyncio.CancelledError:
               pass  # Timer was cancelled
   
   # Usage
   async with Client(cookies_file_path="cookies.json") as client:
       notification_system = TypingNotificationSystem(client)
       await client.listen()

See Also
--------

- :doc:`message` - Message models
- :doc:`thread` - Thread models
- :doc:`../client` - Client methods for typing indicators
- :doc:`/guides/real-time-features` - Guide on real-time features
