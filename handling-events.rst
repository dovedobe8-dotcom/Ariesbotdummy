Handle Events
=============

There are different ways you can handle messenger events such as handling incomimg messages, thread actions, user actions etc. 


Using Decorator
_______________

The most simple way to handle events is to use `event` decorator.

A Quick example of using decorators:

.. code-block:: python

  from fbchat_muqit import Client, EventType
  from fbchat_muqit.models import Message, MessageUnsend


  client = Client("cookies.json")

  @client.event 
  async def on_message(message: Message):
      if message.sender_id != client.uid:
          await client.react("❤️", message.id, message.thread_id)

  @client.event 
  async def on_message_unsent(message: MessageUnsend):
      text = f"User: {message.sender_id} unsent a message in thread: {message.thread_id}"
      print(text)

  client.run()


`@client.event` decorator automatically guesses the event type from function name which may be inaccurate in some cases if the function name is different. So It is better pass the Event Type to the decorator. Like below:

.. code-block:: python

  from fbchat_muqit import Client, EventType
  from fbchat_muqit.models import Message, MessageUnsend


  client = Client("cookies.json")

  @client.event(EventType.MESSAGE)
  async def on_message(message: Message):
      if message.sender_id != client.uid:
          await client.react("❤️", message.id, message.thread_id)

  @client.event(EventType.MESSAGE_UNSENT)
  async def on_message_unsent(message: MessageUnsend):
      text = f"User: {message.sender_id} unsent a message in thread: {message.thread_id}"
      print(text)

  client.run()
     
 
This way the event listener function will be called correctly upon receiving a message. 


Adding Event Listener
_____________________

You can manually add or remove an event listener by passing the ``EventType`` and the defined function to ``add_listener()`` method. 

.. code-block:: python

  from fbchat_muqit import Client, EventType
  from fbchat_muqit.models import Message, MessageUnsend


  client = Client("cookies.json")

  async def on_message(message: Message):
      if message.sender_id != client.uid:
          await client.react("❤️", message.id, message.thread_id)

  async def on_unsent(message: MessageUnsend):
      text = f"User: {message.sender_id} unsent a message in thread: {message.thread_id}"
      print(text)

  # add both function to listener for specific event 
  client.add_listener(EventType.MESSAGE, on_message)
  client.add_listener(EventType.MESSAGE_UNSENT, on_unsent)

  # remove a listener
  client.remove_listener(EventType.MESSAGE, on_message)

  client.run()



Subclassing client
__________________

We can make a subclass of main :class:`~fbchat_muqit.Client` and handle the events. 

.. code-block:: python

  from fbchat_muqit import Client
  from fbchat_muqit.models import Message, ParticipantsAdded


  class myClient(Client):
      async def on_message(self, event_data: Message):
          if event_data.sender_id == client.uid:
              return
          # react to the message
          await self.react(
                  reaction="✅",
                  message_id=event_data.id,
                  thread_id=event_data.thread_id,
                  )
          # echo and reply to the received message
          await self.send_message(
                  text=event_data.text, 
                  thread_id=event_data.thread_id, 
                  reply_to_message=event_data.id
                  )


      async def on_participant_joined(self, event_data: ParticipantsAdded):
          for participant in event_data.added_participants:
              print(f"{participant.name} has been added to thread: {event_data.messageMetadata.thread_id}")


  client = myClient("cookies.json")


  client.run()

