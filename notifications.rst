Notification Models
===================

Classes for representing Facebook notifications and friend request events.

Overview
--------

Notification models track various Facebook events such as friend requests, pokes,
and page notifications. These events are received when listening to the event stream.

.. code-block:: python

  from fbchat_muqit import Client, EventType
  from fbchat_muqit import PokeNotification

  client = Client(cookies_file_path="cookies.json")

  @client.event(EventType.POKE_NOTIFICATION)
  async def on_poke(notification: PokeNotification):
     print(f"👉 You were poked by user {notification.user_poked}")

Notification Classes
--------------------

Friend Request List
~~~~~~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.friendRequestList
   :members:
   :undoc-members:
   :show-inheritance:

Friend Updated
~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.friendUpdated
   :members:
   :undoc-members:
   :show-inheritance:

Friend Request State
~~~~~~~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.FriendRequestState
   :members:
   :undoc-members:
   :show-inheritance:

Poke Notification
~~~~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.PokeNotification
   :members:
   :undoc-members:
   :show-inheritance:

Page Notification
~~~~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.PageNotification
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
--------------

Handling Friend Requests
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

  from fbchat_muqit import Client, EventType
  from fbchat_muqit import friendRequestList, FriendRequestState

  client = Client(cookies_file_path="cookies.json")

  @client.event(EventType.FRIEND_REQUEST_LIST_UPDATE)
  async def on_friend_request_update(notification: friendRequestList):
     """Handle friend request list updates."""
     total = notification.friend_requests
     new = notification.new_friend_request
     
     print(f"📬 Friend Requests Update")
     print(f"   Total pending: {total}")
     print(f"   New requests: {new}")
     
     if new > 0:
         print(f"   You have {new} new friend request(s)!")

  @client.event(EventType.FRIEND_REQUEST_CHANGE)
  async def on_friend_request_action(notification: FriendRequestState):
     """Handle friend request state changes."""
     user_id = str(notification.user_id)
     action = notification.action
     
     # Fetch user info
     users = await client.fetch_user_info(user_id)
     user_name = users[user_id].name if user_id in users else user_id
     
     if action == 'send':
         print(f"📤 You sent a friend request to {user_name}")
     elif action == 'confirm':
         print(f"✅ You accepted {user_name}'s friend request")
         # Send welcome message
         await client.send_message(
             f"Thanks for accepting my friend request! 👋",
             thread_id=user_id
         )
     elif action == 'reject':
         print(f"❌ You rejected {user_name}'s friend request")


Auto-Accept Friend Requests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Client, EventType
   from fbchat_muqit import friendRequestList
   
   class AutoAcceptFriendRequests:
       """Automatically accept all friend requests."""
       
       def __init__(self, client: Client, whitelist: list = None):
           self.client = client
           self.whitelist = whitelist or []  # List of user IDs to auto-accept
           
           self.client.event(EventType.FRIEND_REQUEST_LIST)(self.on_request_update)
       
       async def on_request_update(self, notification: friendRequestList):
           """Handle new friend requests."""
           if notification.new_friend_request > 0:
               print(f"🔔 {notification.new_friend_request} new friend request(s)")
               
               # Note: You would need to implement logic to get pending request IDs
               # This is a simplified example
               print("⏳ Auto-accepting friend requests...")
               
               # If you have specific user IDs in whitelist, accept them
               for user_id in self.whitelist:
                   try:
                       await self.client.manage_friend_request(
                           user_id=user_id,
                           accept_request=True
                       )
                       print(f"✅ Accepted friend request from {user_id}")
                   except Exception as e:
                       print(f"❌ Failed to accept: {e}")
   
   # Usage
   async with Client(cookies_file_path="cookies.json") as client:
       auto_accept = AutoAcceptFriendRequests(
           client,
           whitelist=["100001234567890", "100009876543210"]
       )
       
       await client.listen()


Handling Poke Notifications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Client, EventType
   from fbchat_muqit import PokeNotification
   from datetime import datetime
   
   client = Client(cookies_file_path="cookies.json")
   
   # Track pokes
   poke_history = {}
   
   @client.event(EventType.POKE)
   async def on_poke(notification: PokeNotification):
       """Handle poke notifications."""
       poker_id = str(notification.user_poked)
       poke_time = notification.poke_time
       
       # Fetch user info
       users = await client.fetch_user_info(poker_id)
       poker_name = users[poker_id].name if poker_id in users else poker_id
       
       # Convert timestamp to readable format
       poke_datetime = datetime.fromtimestamp(poke_time / 1000)
       
       print(f"👉 {poker_name} poked you!")
       print(f"   Time: {poke_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
       
       # Track poke history
       if poker_id not in poke_history:
           poke_history[poker_id] = []
       poke_history[poker_id].append(poke_time)
       
       poke_count = len(poke_history[poker_id])
       print(f"   Total pokes from this user: {poke_count}")
       
       # Auto-poke back
       # Function will be added in later updates  
       # Note: You would need to implement poke functionality
       # This is just a placeholder


Handling Page Notifications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Client, EventType
   from fbchat_muqit import PageNotification
   
   client = Client(cookies_file_path="cookies.json")
   
   @client.event(EventType.PAGE_NOTIFICATION)
   async def on_page_notification(notification: PageNotification):
       """Handle notifications from pages."""
       sender_id = notification.sender_id
       page_id = notification.page_id
       page_name = notification.page_name
       message_id = notification.message_id
       title = notification.title
       text = notification.text
       
       print(f"📄 Page Notification from: {page_name}")
       print(f"   Title: {title}")
       print(f"   Message: {text}")
       print(f"   Sender: {sender_id}")
       print(f"   Message ID: {message_id}")
       
       # Auto-reply to page messages
       await client.send_message(
           "Thank you for your message! We'll get back to you soon.",
           thread_id=sender_id
       )

Friend Request Dashboard
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Client, EventType
   from fbchat_muqit import friendRequestList, FriendRequestState, friendUpdated
   
   class FriendRequestDashboard:
       """Track and manage friend requests."""
       
       def __init__(self, client: Client):
           self.client = client
           self.pending_count = 0
           self.new_count = 0
           self.actions = []
           
           # Register event handlers
           self.client.event(EventType.FRIEND_REQUEST_LIST)(self.on_request_list)
           self.client.event(EventType.FRIEND_REQUEST_STATE)(self.on_request_state)
           self.client.event(EventType.FRIEND_UPDATED)(self.on_friend_updated)
       
       async def on_request_list(self, notification: friendRequestList):
           """Update request counts."""
           self.pending_count = notification.friend_requests
           self.new_count = notification.new_friend_request
           
           self.display_dashboard()
       
       async def on_request_state(self, notification: FriendRequestState):
           """Track friend request actions."""
           action_record = {
               'user_id': notification.user_id,
               'action': notification.action,
               'timestamp': datetime.now()
           }
           self.actions.append(action_record)
           
           print(f"\n📝 Action: {notification.action} for user {notification.user_id}")
       
       async def on_friend_updated(self, notification: friendUpdated):
           """Handle removed friend requests."""
           user_id = notification.from_user
           print(f"🔄 Friend request from {user_id} was removed")
       
       def display_dashboard(self):
           """Display the friend request dashboard."""
           print("\n" + "=" * 60)
           print("FRIEND REQUEST DASHBOARD".center(60))
           print("=" * 60)
           print(f"\n📬 Pending Requests: {self.pending_count}")
           print(f"🆕 New Requests: {self.new_count}")
           
           if self.actions:
               print(f"\n📊 Recent Actions: ({len(self.actions)})")
               for action in self.actions[-5:]:  # Show last 5
                   time_str = action['timestamp'].strftime('%H:%M:%S')
                   print(f"  [{time_str}] {action['action']} - User {action['user_id']}")
           
           print("=" * 60 + "\n")
   
   # Usage
   async with Client(cookies_file_path="cookies.json") as client:
       dashboard = FriendRequestDashboard(client)
       await client.listen()

See Also
--------

- :doc:`user` - User models
- :doc:`../client` - Client methods for friend management
- :doc:`/guides/notifications` - Guide on handling notifications
