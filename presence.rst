Presence Models
===============

Classes for representing user presence and online status.

Overview
--------

Presence models track the online/offline status and last active time of users. These events are received
when listening for presence updates and help you monitor when users are available.

.. code-block:: python

   from fbchat_muqit import Client, EventType
   from fbchat_muqit import Presence, UserStatus
   
   client = Client(cookies_file_path="cookies.json")
   
   @client.event(EventType.PRESENCE)
   async def on_presence_update(presence: Presence):
       for user in presence.presence_list:
           status = "🟢 Online" if user.isActive > 0 else "⚫ Offline"
           print(f"{status}: User {user.userId}")

Presence Classes
----------------

Presence
~~~~~~~~

.. autoclass:: fbchat_muqit.Presence
   :members:
   :undoc-members:
   :show-inheritance:

User Status
~~~~~~~~~~~

.. autoclass:: fbchat_muqit.UserStatus
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
--------------

Monitoring User Presence
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Client, EventType
   from fbchat_muqit import Presence, UserStatus
   from datetime import datetime
   
   client = Client(cookies_file_path="cookies.json")
   
   # Track online users
   online_users = set()
   
   @client.event(EventType.PRESENCE)
   async def on_presence(presence: Presence):
       """Handle presence updates."""
       print(f"\n📡 Presence Update ({presence.list_type})")
       
       for user_status in presence.presence_list:
           user_id = str(user_status.userId)
           is_online = user_status.isActive > 0
           
           # Fetch user info
           users = await client.fetch_user_info(user_id)
           user_name = users.get(user_id, {}).name if users else user_id
           
           if is_online:
               if user_id not in online_users:
                   print(f"🟢 {user_name} is now online")
                   online_users.add(user_id)
           else:
               if user_id in online_users:
                   print(f"⚫ {user_name} is now offline")
                   online_users.remove(user_id)
               
               # Show last active time
               if user_status.lastActive > 0:
                   last_active = datetime.fromtimestamp(user_status.lastActive / 1000)
                   print(f"   Last active: {last_active.strftime('%Y-%m-%d %H:%M:%S')}")

Building a Presence Tracker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Client, EventType, Presence, UserStatus
   from datetime import datetime, timedelta
   from typing import Dict
   
   class PresenceTracker:
       """Track user online/offline status and activity patterns."""
       
       def __init__(self, client: Client):
           self.client = client
           self.users: Dict[str, dict] = {}
           
           # Register event handler
           self.client.event(EventType.PRESENCE)(self.on_presence)
       
       async def on_presence(self, presence: Presence):
           """Handle presence updates."""
           for user_status in presence.presence_list:
               user_id = str(user_status.userId)
               is_online = user_status.isActive > 0
               
               # Initialize user tracking
               if user_id not in self.users:
                   self.users[user_id] = {
                       'status': 'offline',
                       'last_online': None,
                       'last_offline': None,
                       'online_duration': timedelta(0),
                       'online_sessions': 0
                   }
               
               user_data = self.users[user_id]
               previous_status = user_data['status']
               
               # Handle status change
               if is_online and previous_status == 'offline':
                   # User came online
                   user_data['status'] = 'online'
                   user_data['last_online'] = datetime.now()
                   user_data['online_sessions'] += 1
                   
                   print(f"🟢 User {user_id} came online")
               
               elif not is_online and previous_status == 'online':
                   # User went offline
                   user_data['status'] = 'offline'
                   user_data['last_offline'] = datetime.now()
                   
                   # Calculate session duration
                   if user_data['last_online']:
                       session_duration = user_data['last_offline'] - user_data['last_online']
                       user_data['online_duration'] += session_duration
                       
                       print(f"⚫ User {user_id} went offline")
                       print(f"   Session duration: {session_duration}")
               
               # Update last active time
               if user_status.lastActive > 0:
                   user_data['last_active_timestamp'] = user_status.lastActive
       
       def get_user_stats(self, user_id: str) -> dict:
           """Get statistics for a user."""
           return self.users.get(user_id, {})
       
       def get_online_users(self) -> list:
           """Get list of currently online users."""
           return [
               user_id for user_id, data in self.users.items()
               if data['status'] == 'online'
           ]
       
       def print_stats(self):
           """Print statistics for all tracked users."""
           print("\n📊 Presence Statistics")
           print("=" * 60)
           
           online_count = len(self.get_online_users())
           total_count = len(self.users)
           
           print(f"Online Users: {online_count}/{total_count}")
           print()
           
           for user_id, data in self.users.items():
               status_icon = "🟢" if data['status'] == 'online' else "⚫"
               print(f"{status_icon} User {user_id}")
               print(f"   Status: {data['status']}")
               print(f"   Sessions: {data['online_sessions']}")
               print(f"   Total Online Time: {data['online_duration']}")
               
               if data.get('last_online'):
                   print(f"   Last Online: {data['last_online']}")
               if data.get('last_offline'):
                   print(f"   Last Offline: {data['last_offline']}")
               print()
   
   # Usage
   async with Client(cookies_file_path="cookies.json") as client:
       tracker = PresenceTracker(client)
       
       # Listen for presence updates
       await client.listen()

Detecting User Activity
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Presence, UserStatus
   from datetime import datetime, timedelta
   
   @client.event(EventType.PRESENCE)
   async def detect_activity(presence: Presence):
       """Detect when users become active after being idle."""
       now = datetime.now()
       
       for user_status in presence.presence_list:
           user_id = str(user_status.userId)
           
           if user_status.isActive > 0:
               # User is currently active
               print(f"✅ User {user_id} is active right now")
           
           elif user_status.lastActive > 0:
               # User is offline, check when they were last active
               last_active = datetime.fromtimestamp(user_status.lastActive / 1000)
               idle_time = now - last_active
               
               if idle_time < timedelta(minutes=5):
                   print(f"🟡 User {user_id} was active {idle_time} ago (recently active)")
               elif idle_time < timedelta(hours=1):
                   print(f"🟠 User {user_id} was active {idle_time} ago")
               else:
                   print(f"⚫ User {user_id} was last active {idle_time} ago")

Notification on Friend Online
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Client, EventType, Presence
   
   class OnlineNotifier:
       """Notify when specific friends come online."""
       
       def __init__(self, client: Client, watch_users: list):
           self.client = client
           self.watch_users = set(str(uid) for uid in watch_users)
           self.online_status = {}
           
           self.client.event(EventType.PRESENCE)(self.on_presence)
       
       async def on_presence(self, presence: Presence):
           """Notify when watched users come online."""
           for user_status in presence.presence_list:
               user_id = str(user_status.userId)
               
               # Only track watched users
               if user_id not in self.watch_users:
                   continue
               
               is_online = user_status.isActive > 0
               was_online = self.online_status.get(user_id, False)
               
               # User just came online
               if is_online and not was_online:
                   # Fetch user info
                   users = await self.client.fetch_user_info(user_id)
                   user_name = users[user_id].name if user_id in users else user_id
                   
                   print(f"🔔 {user_name} is now online!")
                   
                   # Optional: Send them a message
                   # await self.client.send_message(
                   #     "Hey! I saw you came online 👋",
                   #     thread_id=user_id
                   # )
               
               # Update status
               self.online_status[user_id] = is_online
   
   # Usage
   async with Client(cookies_file_path="cookies.json") as client:
       # Watch specific friends
       notifier = OnlineNotifier(
           client,
           watch_users=["100001234567890", "100009876543210"]
       )
       
       await client.listen()

Building an Activity Dashboard
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Client, EventType, Presence
   from datetime import datetime
   import time
   
   class ActivityDashboard:
       """Real-time dashboard of user activity."""
       
       def __init__(self, client: Client):
           self.client = client
           self.users = {}
           self.client.event(EventType.PRESENCE)(self.on_presence)
       
       async def on_presence(self, presence: Presence):
           """Update dashboard with presence data."""
           for user_status in presence.presence_list:
               user_id = str(user_status.userId)
               
               # Get user name
               if user_id not in self.users:
                   users_info = await self.client.fetch_user_info(user_id)
                   user_name = users_info[user_id].name if user_id in users_info else user_id
                   
                   self.users[user_id] = {
                       'name': user_name,
                       'status': 'unknown',
                       'last_active': None
                   }
               
               # Update status
               is_online = user_status.isActive > 0
               self.users[user_id]['status'] = 'online' if is_online else 'offline'
               
               if user_status.lastActive > 0:
                   self.users[user_id]['last_active'] = user_status.lastActive
               
               # Refresh display
               self.display_dashboard()
       
       def display_dashboard(self):
           """Display the activity dashboard."""
           # Clear screen (optional)
           print("\033[2J\033[H")  # ANSI escape code
           
           print("=" * 70)
           print("ACTIVITY DASHBOARD".center(70))
           print("=" * 70)
           print(f"Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
           print()
           
           # Separate online and offline users
           online = []
           offline = []
           
           for user_id, data in self.users.items():
               if data['status'] == 'online':
                   online.append((user_id, data))
               else:
                   offline.append((user_id, data))
           
           # Display online users
           print(f"🟢 ONLINE ({len(online)})")
           print("-" * 70)
           for user_id, data in online:
               print(f"  {data['name']:<30} {user_id}")
           print()
           
           # Display offline users with last active time
           print(f"⚫ OFFLINE ({len(offline)})")
           print("-" * 70)
           for user_id, data in offline[:10]:  # Show first 10
               last_active = ""
               if data['last_active']:
                   last_time = datetime.fromtimestamp(data['last_active'] / 1000)
                   last_active = f"Last: {last_time.strftime('%H:%M:%S')}"
               
               print(f"  {data['name']:<30} {last_active}")
           
           if len(offline) > 10:
               print(f"  ... and {len(offline) - 10} more")
           
           print("=" * 70)
   
   # Usage
   async with Client(cookies_file_path="cookies.json") as client:
       dashboard = ActivityDashboard(client)
       await client.listen()

Auto-Response When Online
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Client, EventType, Presence, Message
   
   class SmartAutoResponder:
       """Auto-respond based on your online status."""
       
       def __init__(self, client: Client):
           self.client = client
           self.am_i_online = True  # Assume online initially
           self.away_message = "I'm currently away. I'll respond when I'm back!"
           
           self.client.event(EventType.PRESENCE)(self.on_presence)
           self.client.event(EventType.MESSAGE)(self.on_message)
       
       async def on_presence(self, presence: Presence):
           """Track own online status."""
           my_uid = int(self.client.uid)
           
           for user_status in presence.presence_list:
               if user_status.userId == my_uid:
                   was_online = self.am_i_online
                   self.am_i_online = user_status.isActive > 0
                   
                   if was_online != self.am_i_online:
                       status = "online" if self.am_i_online else "away"
                       print(f"📱 Status changed: {status}")
       
       async def on_message(self, message: Message):
           """Auto-respond when away."""
           # Don't respond to own messages
           if message.sender_id == self.client.uid:
               return
           
           # Only auto-respond when away
           if not self.am_i_online:
               # Send away message
               await self.client.send_message(
                   text=self.away_message,
                   thread_id=message.thread_id
               )
               
               print(f"📤 Sent away message to {message.sender_id}")
   
   # Usage
   async with Client(cookies_file_path="cookies.json") as client:
       responder = SmartAutoResponder(client)
       await client.listen()

Understanding Presence List Types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Presence
   
   @client.event(EventType.PRESENCE)
   async def on_presence(presence: Presence):
       """Handle different presence list types."""
       
       if presence.list_type == "full":
           # Full presence list (received on first listen or reconnection)
           print("📋 Received full presence list")
           print(f"   Total users: {len(presence.presence_list)}")
           
           # Process all users
           online_count = sum(1 for u in presence.presence_list if u.isActive > 0)
           offline_count = len(presence.presence_list) - online_count
           
           print(f"   Online: {online_count}")
           print(f"   Offline: {offline_count}")
       
       elif presence.list_type == "inc":
           # Incremental update (partial list with changes)
           print("🔄 Received presence update")
           
           # Process only changed users
           for user_status in presence.presence_list:
               user_id = user_status.userId
               status = "online" if user_status.isActive > 0 else "offline"
               print(f"   User {user_id}: {status}")

See Also
--------

- :doc:`thread` - Thread models
- :doc:`user` - User models
- :doc:`../client` - Client methods
- :doc:`/guides/event-handling` - Guide on handling events
