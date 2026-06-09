
User Models
===========

Classes for representing Facebook users and their information.

Overview
--------

User models contain information about Facebook users including their profile details,
friendship status, and other metadata.

.. code-block:: python

  from fbchat_muqit import Client
  import asyncio


  async def main():
      async with Client(cookies_file_path="cookies.json") as client:
         # Fetch single user
         users = await client.fetch_user_info("100001234567890")
         user = users["100001234567890"]
         
         print(f"Name: {user.name}")
         print(f"Username: {user.username}")
         print(f"Is Friend: {user.is_friend}")
         
         # Fetch multiple users
         users = await client.fetch_user_info(
             "100001234567890",
             "100009876543210",
             "100005555555555"
         )
         
         for user_id, user in users.items():
             print(f"{user.name} (@{user.username})")

  asyncio.run(main())

User Class
----------

.. autoclass:: fbchat_muqit.User
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
--------------

Fetching User Information
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   
   async with Client(cookies_file_path="cookies.json") as client:
       # Fetch a single user
       user_id = "100001234567890"
       users = await client.fetch_user_info(user_id)
       user = users[user_id]
       
       # Access user properties
       print(f"📝 User Information")
       print(f"   Name: {user.name}")
       print(f"   First Name: {user.first_name}")
       print(f"   Username: @{user.username}")
       print(f"   Gender: {user.gender}")
       print(f"   Profile URL: {user.url}")
       print(f"   Profile Picture: {user.image}")
       
       # Check friendship status
       if user.is_friend:
           print(f"✅ You are friends with {user.name}")
       else:
           print(f"❌ Not friends with {user.name}")
       
       # Check block status
       if user.is_blocked:
           print(f"🚫 You have blocked or been blocked by {user.name}")

Fetching Multiple Users
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   
   async with Client(cookies_file_path="cookies.json") as client:
       # Fetch multiple users at once
       user_ids = [
           "100001234567890",
           "100009876543210",
           "100005555555555"
       ]
       
       users = await client.fetch_user_info(*user_ids)
       
       print(f"Fetched {len(users)} users:")
       for user_id, user in users.items():
           print(f"  👤 {user.name} (ID: {user_id})")
           if user.username:
               print(f"     @{user.username}")

Fetching All Contacts
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Client
   
   async with Client(cookies_file_path="cookies.json") as client:
       # Fetch all users you chat with
       all_users = await client.fetch_all_users()
       
       print(f"Total contacts: {len(all_users)}")
       
       # Filter friends
       friends = {
           uid: user for uid, user in all_users.items()
           if user.is_friend
       }
       print(f"Friends: {len(friends)}")
       
       # Filter by gender
       male_users = {
           uid: user for uid, user in all_users.items()
           if user.gender in ['male', 'male_singular']
       }
       female_users = {
           uid: user for uid, user in all_users.items()
           if user.gender in ['female', 'female_singular']
       }
       
       print(f"Male: {len(male_users)}, Female: {len(female_users)}")

Building a User Cache
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Client, User
   from typing import Dict
   import json
   
   class UserCache:
       """Cache user information to reduce API calls."""
       
       def __init__(self, client: Client, cache_file: str = "user_cache.json"):
           self.client = client
           self.cache_file = cache_file
           self.cache: Dict[str, dict] = {}
           self.load_cache()
       
       def load_cache(self):
           """Load cache from file."""
           try:
               with open(self.cache_file, 'r') as f:
                   self.cache = json.load(f)
               print(f"📂 Loaded {len(self.cache)} users from cache")
           except FileNotFoundError:
               print("📂 No cache file found, starting fresh")
       
       def save_cache(self):
           """Save cache to file."""
           with open(self.cache_file, 'w') as f:
               json.dump(self.cache, f, indent=2)
           print(f"💾 Saved {len(self.cache)} users to cache")
       
       async def get_user(self, user_id: str) -> User:
           """Get user from cache or fetch if not cached."""
           if user_id in self.cache:
               print(f"✅ Found {user_id} in cache")
               # Reconstruct User object from cache
               return User(**self.cache[user_id])
           
           # Fetch from API
           print(f"🔍 Fetching {user_id} from API")
           users = await self.client.fetch_user_info(user_id)
           user = users[user_id]
           
           # Cache the user (convert to dict)
           self.cache[user_id] = {
               'id': user.id,
               'name': user.name,
               'first_name': user.first_name,
               'username': user.username,
               'gender': user.gender,
               'url': user.url,
               'is_friend': user.is_friend,
               'is_blocked': user.is_blocked,
               'image': user.image,
               'alternate_name': user.alternate_name
           }
           
           self.save_cache()
           return user
       
       async def get_users(self, *user_ids: str) -> Dict[str, User]:
           """Get multiple users, fetching only uncached ones."""
           result = {}
           to_fetch = []
           
           # Check cache first
           for user_id in user_ids:
               if user_id in self.cache:
                   result[user_id] = User(**self.cache[user_id])
               else:
                   to_fetch.append(user_id)
           
           # Fetch uncached users
           if to_fetch:
               print(f"🔍 Fetching {len(to_fetch)} users from API")
               fetched = await self.client.fetch_user_info(*to_fetch)
               
               for user_id, user in fetched.items():
                   result[user_id] = user
                   self.cache[user_id] = {
                       'id': user.id,
                       'name': user.name,
                       'first_name': user.first_name,
                       'username': user.username,
                       'gender': user.gender,
                       'url': user.url,
                       'is_friend': user.is_friend,
                       'is_blocked': user.is_blocked,
                       'image': user.image,
                       'alternate_name': user.alternate_name
                   }
               
               self.save_cache()
           
           return result
   
   # Usage
   async with Client(cookies_file_path="cookies.json") as client:
       cache = UserCache(client)
       
       # First call fetches from API
       user = await cache.get_user("100001234567890")
       print(f"Got: {user.name}")
       
       # Second call uses cache
       user = await cache.get_user("100001234567890")
       print(f"Got: {user.name}")

User Search and Filter
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Client, User
   from typing import Dict, List
   
   class UserDirectory:
       """Search and filter users."""
       
       def __init__(self):
           self.users: Dict[str, User] = {}
       
       async def load_all_users(self, client: Client):
           """Load all users from the client."""
           self.users = await client.fetch_all_users()
           print(f"📚 Loaded {len(self.users)} users")
       
       def search_by_name(self, query: str) -> List[User]:
           """Search users by name."""
           query = query.lower()
           return [
               user for user in self.users.values()
               if query in user.name.lower() or 
                  query in user.first_name.lower()
           ]
       
       def search_by_username(self, username: str) -> List[User]:
           """Search users by username."""
           username = username.lower().replace('@', '')
           return [
               user for user in self.users.values()
               if user.username and username in user.username.lower()
           ]
       
       def get_friends(self) -> List[User]:
           """Get all friends."""
           return [
               user for user in self.users.values()
               if user.is_friend
           ]
       
       def get_by_gender(self, gender: str) -> List[User]:
           """Get users by gender."""
           return [
               user for user in self.users.values()
               if gender.lower() in user.gender.lower()
           ]
       
       def get_blocked_users(self) -> List[User]:
           """Get all blocked users."""
           return [
               user for user in self.users.values()
               if user.is_blocked
           ]
   
   # Usage
   async with Client(cookies_file_path="cookies.json") as client:
       directory = UserDirectory()
       await directory.load_all_users(client)
       
       # Search by name
       results = directory.search_by_name("John")
       print(f"Found {len(results)} users named John:")
       for user in results:
           print(f"  - {user.name} (@{user.username})")
       
       # Get all friends
       friends = directory.get_friends()
       print(f"\n👥 You have {len(friends)} friends")
       
       # Filter by gender
       male_friends = [u for u in friends if 'male' in u.gender and 'female' not in u.gender]
       female_friends = [u for u in friends if 'female' in u.gender]
       print(f"   Male: {len(male_friends)}")
       print(f"   Female: {len(female_friends)}")

Displaying User Profile
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Client, User
   
   async def display_user_profile(client: Client, user_id: str):
       """Display a formatted user profile."""
       users = await client.fetch_user_info(user_id)
       user = users[user_id]
       
       print("=" * 60)
       print(f"USER PROFILE".center(60))
       print("=" * 60)
       print()
       print(f"👤 Name: {user.name}")
       
       if user.alternate_name:
           print(f"   Also known as: {user.alternate_name}")
       
       print(f"📝 First Name: {user.first_name}")
       
       if user.username:
           print(f"🔗 Username: @{user.username}")
       
       print(f"🆔 User ID: {user.id}")
       
       if user.gender:
           gender_emoji = {
               'male': '♂️',
               'female': '♀️',
               'male_singular': '♂️',
               'female_singular': '♀️'
           }.get(user.gender, '⚧')
           print(f"{gender_emoji} Gender: {user.gender}")
       
       if user.url:
           print(f"🌐 Profile: {user.url}")
       
       if user.image:
           print(f"🖼️  Picture: {user.image}")
       
       print()
       print("Relationship:")
       print(f"  {'✅' if user.is_friend else '❌'} Friend")
       print(f"  {'🚫' if user.is_blocked else '✅'} {'Blocked' if user.is_blocked else 'Not Blocked'}")
       print()
       print("=" * 60)
   
   # Usage
   async with Client(cookies_file_path="cookies.json") as client:
       await display_user_profile(client, "100001234567890")

Bulk User Operations
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Client
   from typing import List
   
   async def get_thread_participants_info(
       client: Client,
       thread_id: str
   ) -> dict:
       """Get info for all participants in a thread."""
       # Fetch thread info
       threads = await client.fetch_thread_info([thread_id])
       thread = threads[0]
       
       # Get participant IDs
       participant_ids = [str(p) for p in thread.participants]
       
       # Fetch all user info
       users = await client.fetch_user_info(*participant_ids)
       
       return users
   
   async def find_mutual_friends(
       client: Client,
       user_id1: str,
       user_id2: str
   ) -> List[str]:
       """Find mutual friends (simplified version)."""
       # This is a simplified example
       # Facebook doesn't provide direct mutual friends API
       
       # Get all users
       all_users = await client.fetch_all_users()
       
       # Get friends of both users (if available)
       # Note: You can only see your own friends list
       my_friends = {
           uid for uid, user in all_users.items()
           if user.is_friend
       }
       
       print(f"You have {len(my_friends)} friends")
       return list(my_friends)
   
   # Usage
   async with Client(cookies_file_path="cookies.json") as client:
       # Get all participants in a group
       participants = await get_thread_participants_info(
           client,
           thread_id="123456789"
       )
       
       print("Group Members:")
       for user_id, user in participants.items():
           friend_status = "👥 Friend" if user.is_friend else "👤 Not Friend"
           print(f"  {user.name} - {friend_status}")

See Also
--------

- :doc:`thread` - Thread models
- :doc:`message` - Message models
- :doc:`../client` - Client methods for user operations
- :doc:`/guides/user-management` - Guide on managing users
