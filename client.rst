
Client
======

The main client class for interacting with Facebook and Messenger.

.. autoclass:: fbchat_muqit.Client
   :members: __init__, uid, name
   :undoc-members:
   :show-inheritance:

Overview
--------

The ``Client`` class is the main entry point for fbchat-muqit. It combines Facebook operations, 
Messenger operations, and event handling into a single interface.

.. code-block:: python

  import asyncio
  from fbchat_muqit import Client, Message

  # Enter correct cookie file path
  client = Client(cookies_file_path="cookies.json")

  @client.event
  async def on_message(message: Message):
          
      # To avoid spam check if sender_id is client's id or not
      if message.sender_id != client.uid:
          # show typing indicator
          await client.typing(message.thread_id, True, message.thread_type)

          # typing for 0.5s
          await asyncio.sleep(0.5)
          
          # stop typing indicator 
          await client.typing(message.thread_id, False, message.thread_type)

          # send a message
          await client.send_message("Hello!", thread_id=message.thread_id)

  client.run()
        

Initialization
--------------

.. automethod:: fbchat_muqit.Client.__init__

Session Management
------------------

.. automethod:: fbchat_muqit.Client.start
.. automethod:: fbchat_muqit.Client.close
.. automethod:: fbchat_muqit.Client.run

Event Listening
---------------

.. automethod:: fbchat_muqit.Client.listen
.. automethod:: fbchat_muqit.Client.start_listening
.. automethod:: fbchat_muqit.Client.stop_listening

Messenger Operations
====================

Sending Messages
----------------

.. automethod:: fbchat_muqit.messenger.client.MessengerClient.send_message
.. automethod:: fbchat_muqit.messenger.client.MessengerClient.send_quick_reaction
.. automethod:: fbchat_muqit.messenger.client.MessengerClient.send_files
.. automethod:: fbchat_muqit.messenger.client.MessengerClient.send_files_from_path
.. automethod:: fbchat_muqit.messenger.client.MessengerClient.send_files_from_url
.. automethod:: fbchat_muqit.messenger.client.MessengerClient.forward_message

Message Interactions
--------------------

.. automethod:: fbchat_muqit.messenger.client.MessengerClient.react
.. automethod:: fbchat_muqit.messenger.client.MessengerClient.unsend
.. automethod:: fbchat_muqit.messenger.client.MessengerClient.pin_message

Fetching Data
-------------

.. automethod:: fbchat_muqit.messenger.client.MessengerClient.fetch_thread_list
.. automethod:: fbchat_muqit.messenger.client.MessengerClient.fetch_thread_info
.. automethod:: fbchat_muqit.messenger.client.MessengerClient.fetch_thread_messages
.. automethod:: fbchat_muqit.messenger.client.MessengerClient.fetch_message_info
.. automethod:: fbchat_muqit.messenger.client.MessengerClient.fetch_user_info
.. automethod:: fbchat_muqit.messenger.client.MessengerClient.fetch_all_users
.. automethod:: fbchat_muqit.messenger.client.MessengerClient.fetch_thread_themes

Thread Management
-----------------

.. automethod:: fbchat_muqit.messenger.client.MessengerClient.create_group_thread
.. automethod:: fbchat_muqit.messenger.client.MessengerClient.change_thread_name
.. automethod:: fbchat_muqit.messenger.client.MessengerClient.change_thread_image
.. automethod:: fbchat_muqit.messenger.client.MessengerClient.change_thread_theme
.. automethod:: fbchat_muqit.messenger.client.MessengerClient.change_thread_emoji
.. automethod:: fbchat_muqit.messenger.client.MessengerClient.change_nickname

Thread Settings
---------------

.. automethod:: fbchat_muqit.messenger.client.MessengerClient.change_thread_approval
.. automethod:: fbchat_muqit.messenger.client.MessengerClient.change_thread_message_share
.. automethod:: fbchat_muqit.messenger.client.MessengerClient.change_read_receipts
.. automethod:: fbchat_muqit.messenger.client.MessengerClient.mute_thread

Participant Management
----------------------

.. automethod:: fbchat_muqit.messenger.client.MessengerClient.add_participants
.. automethod:: fbchat_muqit.messenger.client.MessengerClient.remove_participant
.. automethod:: fbchat_muqit.messenger.client.MessengerClient.set_thread_admin

Thread Actions
--------------

.. automethod:: fbchat_muqit.messenger.client.MessengerClient.mark_as_read
.. automethod:: fbchat_muqit.messenger.client.MessengerClient.mark_as_unread
.. automethod:: fbchat_muqit.messenger.client.MessengerClient.typing
.. automethod:: fbchat_muqit.messenger.client.MessengerClient.search_message

File Handling
-------------

.. automethod:: fbchat_muqit.messenger.client.MessengerClient.uploadFiles

User Management
---------------

.. automethod:: fbchat_muqit.messenger.client.MessengerClient.restrict_user
.. automethod:: fbchat_muqit.messenger.client.MessengerClient.accept_friend_request

Facebook Operations
===================

Posts
-----

.. automethod:: fbchat_muqit.facebook.client.FacebookClient.publish_post
.. automethod:: fbchat_muqit.facebook.client.FacebookClient.react_to_post

Media Upload
------------

.. automethod:: fbchat_muqit.facebook.client.FacebookClient.upload_photo
.. automethod:: fbchat_muqit.facebook.client.FacebookClient.upload_photos

Friend Management
-----------------

.. automethod:: fbchat_muqit.facebook.client.FacebookClient.send_friend_request
.. automethod:: fbchat_muqit.facebook.client.FacebookClient.manage_friend_request
.. automethod:: fbchat_muqit.facebook.client.FacebookClient.cancel_friend_request
.. automethod:: fbchat_muqit.facebook.client.FacebookClient.unfriend

Properties
==========

.. autoproperty:: fbchat_muqit.Client.uid
.. autoproperty:: fbchat_muqit.Client.name

See Also
========

- :doc:`/guides/sending-messages` - Guide on sending different types of messages
- :doc:`/guides/event-handling` - Guide on handling events
- :doc:`/api/models/index` - Data models used throughout the library
