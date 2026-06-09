Timestamp Events
================

Classes for representing timestamp-related events such as read receipts, delivery receipts, and message status updates.

Overview
--------

Timestamp events track when messages are delivered, read, or when threads are marked as seen/unseen.
These events help you monitor message status and user engagement.

.. code-block:: python

   from fbchat_muqit import Client, EventType
   from fbchat_muqit import ReadReceipt, DeliveryReceipt
   
   client = Client(cookies_file_path="cookies.json")
   
   @client.event(EventType.READ_RECEIPT)
   async def on_message_read(event: ReadReceipt):
       print(f"User {event.user_id} read messages in thread {event.thread_id}")
   
   @client.event(EventType.DELIVERY_RECEIPT)
   async def on_message_delivered(event: DeliveryReceipt):
       print(f"Messages {event.message_id} were delivered")

Read and Delivery Events
-------------------------

Read Receipt
~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.ReadReceipt
   :members:
   :undoc-members:
   :show-inheritance:

Delivery Receipt
~~~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.DeliveryReceipt
   :members:
   :undoc-members:
   :show-inheritance:

Mark Status Events
------------------

Mark Folder Seen
~~~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.MarkFolderSeen
   :members:
   :undoc-members:
   :show-inheritance:

Mark Read
~~~~~~~~~

.. autoclass:: fbchat_muqit.MarkRead
   :members:
   :undoc-members:
   :show-inheritance:

Mark Unread
~~~~~~~~~~~

.. autoclass:: fbchat_muqit.MarkUnread
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
--------------


Tracking Read Receipts
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

  from fbchat_muqit import ReadReceipt, EventType, Client
  import time

  # Store message read status
  message_reads = {}
  client = Client(cookies_file_path="cookies.json")

  @client.event(EventType.MARK_READ)
  async def on_message_read(event: ReadReceipt):
     """Handle when someone reads your messages."""
     user_id = event.user_id
     thread_id = event.thread_id
     read_time = int(event.watermark_timestamp)
     
     print(f"👁️ User {user_id} read messages in thread {thread_id}")
     print(f"   Read at: {time.ctime(read_time / 1000)}")
     
     # Store read status
     if thread_id not in message_reads:
         message_reads[thread_id] = {}
     
     message_reads[thread_id][user_id] = read_time
     
     # Fetch user info
     users = await client.fetch_user_info(user_id)
     if user_id in users:
         user_name = users[user_id].name
         print(f"   Reader: {user_name}")

Monitoring Thread Status
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from fbchat_muqit import MarkRead, MarkUnread, MarkFolderSeen, Client, EventType

    client = Client(cookies_file_path="cookies.json")


    @client.event(EventType.MARK_READ)
    async def on_mark_read(event: MarkRead):
       """Handle when threads are marked as read."""
       for thread_key in event.thread_ids:
           thread_id = str(thread_key)
           print(f"✉️ Thread {thread_id} marked as read")
           

    @client.event(EventType.MARK_UNREAD)
    async def on_mark_unread(event: MarkUnread):
       """Handle when threads are marked as unread."""
       for thread_key in event.thread_ids:
           thread_id = str(thread_key)
           print(f"📬 Thread {thread_id} marked as unread")
           

    @client.event(EventType.MESSAGE_SEEN)
    async def on_folder_seen(event: MarkFolderSeen):
       """Handle when folders are marked as seen."""
       print(f"👀 Folders seen: {', '.join(event.folders)}")
       print(f"   Timestamp: {event.timestamp}")



See Also
--------

- :doc:`message` - Message models
- :doc:`thread` - Thread models
- :doc:`../client` - Client methods for sending messages
- :doc:`/guides/event-handling` - Guide on handling events
