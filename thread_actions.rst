Thread Actions
==============

Classes for representing thread-related events and actions.

Overview
--------

Thread actions represent various events that occur in conversations, such as participants joining/leaving,
settings changes, admin actions, and more. These are typically received when listening to events.

.. code-block:: python

   from fbchat_muqit import Client, EventType
   from fbchat_muqit import ParticipantsAdded, ThreadName, ThreadTheme
   
   client = Client(cookies_file_path="cookies.json")
   
   @client.event(EventType.PARTICIPANTS_ADDED)
   async def on_participant_added(event: ParticipantsAdded):
       print(f"New members: {[p.name for p in event.added_participants]}")
   
   @client.event(EventType.THREAD_NAME_CHANGE)
   async def on_name_change(event: ThreadName):
       print(f"Group renamed to: {event.name}")

Participant Events
------------------

Participants Added
~~~~~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.ParticipantsAdded
   :members:
   :undoc-members:
   :show-inheritance:

Participant Left
~~~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.ParticipantLeft
   :members:
   :undoc-members:
   :show-inheritance:

Added Participant Info
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.addedParticipant
   :members:
   :undoc-members:
   :show-inheritance:

Admin Management Events
-----------------------

Admin Added
~~~~~~~~~~~

.. autoclass:: fbchat_muqit.AdminAdded
   :members:
   :undoc-members:
   :show-inheritance:

Admin Removed
~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.AdminRemoved
   :members:
   :undoc-members:
   :show-inheritance:

Thread Settings Events
----------------------

Thread Name
~~~~~~~~~~~

.. autoclass:: fbchat_muqit.ThreadName
   :members:
   :undoc-members:
   :show-inheritance:

Thread Theme
~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.ThreadTheme
   :members:
   :undoc-members:
   :show-inheritance:

Thread Emoji
~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.ThreadEmoji
   :members:
   :undoc-members:
   :show-inheritance:

Thread Nickname
~~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.ThreadNickname
   :members:
   :undoc-members:
   :show-inheritance:

Thread Magic Word
~~~~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.ThreadMagicWord
   :members:
   :undoc-members:
   :show-inheritance:

Approval and Privacy Events
----------------------------

Approval Mode
~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.ApprovalMode
   :members:
   :undoc-members:
   :show-inheritance:

Approval Queue
~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.ApprovalQueue
   :members:
   :undoc-members:
   :show-inheritance:

Approved User
~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.ApprovedUser
   :members:
   :undoc-members:
   :show-inheritance:

Joinable Mode
~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.JoinableMode
   :members:
   :undoc-members:
   :show-inheritance:

Message Actions
---------------

Thread Message Pin
~~~~~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.ThreadMessagePin
   :members:
   :undoc-members:
   :show-inheritance:

Thread Message UnPin
~~~~~~~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.ThreadMessageUnPin
   :members:
   :undoc-members:
   :show-inheritance:

Thread Message Sharing
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.ThreadMessageSharing
   :members:
   :undoc-members:
   :show-inheritance:

Thread Management Events
------------------------

Thread Action
~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.ThreadAction
   :members:
   :undoc-members:
   :show-inheritance:

Thread Folder Move
~~~~~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.ThreadFolderMove
   :members:
   :undoc-members:
   :show-inheritance:

Thread Delete
~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.ThreadDelete
   :members:
   :undoc-members:
   :show-inheritance:

Mute Settings
-------------

Mute Thread
~~~~~~~~~~~

.. autoclass:: fbchat_muqit.MuteThread
   :members:
   :undoc-members:
   :show-inheritance:

Thread Mute Settings
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.ThreadMuteSettings
   :members:
   :undoc-members:
   :show-inheritance:

User Status Events
------------------

Change Viewer Status
~~~~~~~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.ChangeViwerStatus
   :members:
   :undoc-members:
   :show-inheritance:

Other Events
------------

Forced Fetch
~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.ForcedFetch
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
--------------

Handling Participant Events
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Client, EventType
   from fbchat_muqit import ParticipantsAdded, ParticipantLeft
   
   client = Client(cookies_file_path="cookies.json")
   
   @client.event(EventType.PARTICIPANTS_ADDED)
   async def on_members_added(event: ParticipantsAdded):
       """Handle when new members are added to a group."""
       author = event.messageMetadata.actorFbId
       thread_id = event.messageMetadata.threadKey.threadFbId
       
       for participant in event.added_participants:
           print(f"👋 {participant.name} was added to the group")
           print(f"   Added by: {author}")
       
       # Welcome new members
       names = ", ".join(p.name for p in event.added_participants)
       await client.send_message(
           f"Welcome {names}! 🎉",
           thread_id=thread_id
       )
   
   @client.event(EventType.PARTICIPANT_LEFT)
   async def on_member_left(event: ParticipantLeft):
       """Handle when a member leaves the group."""
       thread_id = event.messageMetadata.threadKey.threadFbId
       left_user_id = event.left_participant
       
       print(f"👋 User {left_user_id} left the group")
       
       # Fetch remaining participants
       print(f"Remaining members: {len(event.participants)}")

Handling Thread Settings Changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import ThreadName, ThreadTheme, ThreadEmoji
   
   @client.event(EventType.THREAD_NAME_CHANGE)
   async def on_name_change(event: ThreadName):
       """Handle group name changes."""
       thread_id = event.messageMetadata.threadKey.threadFbId
       author = event.messageMetadata.actorFbId
       
       print(f"📝 Group renamed to: {event.name}")
       print(f"   Changed by: {author}")
   
   @client.event(EventType.THREAD_THEME_CHANGE)
   async def on_theme_change(event: ThreadTheme):
       """Handle theme changes."""
       print(f"🎨 New theme: {event.theme_name}")
       print(f"   Color: {event.theme_color}")
       print(f"   Emoji: {event.theme_emoji}")
   
   @client.event(EventType.THREAD_EMOJI_CHANGE)
   async def on_emoji_change(event: ThreadEmoji):
       """Handle quick reaction emoji changes."""
       print(f"😊 New quick reaction: {event.emoji}")

Handling Admin Actions
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import AdminAdded, AdminRemoved
   
   @client.event(EventType.ADMIN_ADDED)
   async def on_admin_added(event: AdminAdded):
       """Handle when someone becomes an admin."""
       print(f"👑 New admin: {event.aded_admin}")
       
       thread_id = event.messageMetadata.threadKey.threadFbId
       await client.send_message(
           "Congratulations on becoming an admin! 👑",
           thread_id=thread_id
       )
   
   @client.event(EventType.ADMIN_REMOVED)
   async def on_admin_removed(event: AdminRemoved):
       """Handle when admin privileges are revoked."""
       for admin_id in event.removed_admins:
           print(f"👑 Admin removed: {admin_id}")

Handling Approval Mode
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import ApprovalMode, ApprovalQueue, ApprovedUser
   
   @client.event(EventType.APPROVAL_MODE_CHANGE)
   async def on_approval_mode(event: ApprovalMode):
       """Handle approval mode toggle."""
       if event.mode == "APPROVALS":
           print("🔒 Approval mode enabled - join requests need approval")
       else:
           print("🔓 Approval mode disabled - anyone can join")
   
   @client.event(EventType.APPROVAL_QUEUE)
   async def on_join_request(event: ApprovalQueue):
       """Handle join requests."""
       if event.action == "REQUESTED":
           print(f"📥 New join request from: {event.requester_id}")
           
           # Auto-approve (if you're an admin)
           # Note: You'll need to implement the approval logic
       elif event.action == "REMOVED":
           print(f"❌ Join request removed: {event.requester_id}")
   
   @client.event(EventType.USER_APPROVED)
   async def on_user_approved(event: ApprovedUser):
       """Handle when a user is approved."""
       thread_id = event.thread_id.threadFbId
       approved_id = event.approved_user_id
       
       await client.send_message(
           f"Welcome! Your join request was approved 🎉",
           thread_id=thread_id
       )

Handling Message Actions
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import ThreadMessagePin, ThreadMessageUnPin
   
   @client.event(EventType.MESSAGE_PINNED)
   async def on_message_pinned(event: ThreadMessagePin):
       """Handle when a message is pinned."""
       print(f"📌 Message pinned: {event.message_id}")
       
       # Fetch the pinned message details
       thread_id = event.messageMetadata.threadKey.threadFbId
       message = await client.fetch_message_info(
           event.message_id, 
           thread_id
       )
       print(f"   Content: {message.text}")
   
   @client.event(EventType.MESSAGE_UNPINNED)
   async def on_message_unpinned(event: ThreadMessageUnPin):
       """Handle when a message is unpinned."""
       print(f"📍 Message unpinned: {event.message_id}")

Handling Mute Events
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import MuteThread, ThreadMuteSettings
   
   @client.event(EventType.THREAD_MUTED)
   async def on_thread_muted(event: MuteThread):
       """Handle when a thread is muted."""
       thread_id = event.thread_id.threadFbId
       
       if event.mute_until == -1:
           print(f"🔇 Thread {thread_id} muted forever")
       else:
           print(f"🔇 Thread {thread_id} muted until {event.mute_until}")
   
   @client.event(EventType.MUTE_SETTINGS_CHANGE)
   async def on_mute_settings(event: ThreadMuteSettings):
       """Handle mute settings changes."""
       thread_id = event.thread_id.threadFbId
       user_id = event.user_id
       
       print(f"🔕 User {user_id} changed mute settings")
       print(f"   Expires: {event.expire_time}")

See Also
--------

- :doc:`thread` - Thread models
- :doc:`message` - Message models  
- :doc:`../client` - Client methods for thread management
- :doc:`/guides/event-handling` - Guide on handling events
