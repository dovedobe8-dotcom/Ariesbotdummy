Quick Start Guide
=================

This guide will help you get started with fbchat-muqit.

Prerequisites
-------------

- Python 3.9 or higher
- A Facebook account to use as Client. (Safer to use old unused account or new)
- Basic knowledge of async/await in Python

Installation
------------

.. code-block:: bash

   pip install fbchat-muqit



Account Login
_____________

fbchat-muqit library uses cookies for authentication. Since due to recent changes in Facebook login via email and password has become very complex. 

We use the already logged in browser cookies and trick the Facebook server thinking we are accessing the account normally from our browser. Learn more about :ref:`how Facebook cookies work <facebook-cookies>`.


To get your Facebook account cookies. First login in your Facebook account and then add `c3c fbstate extension <https://github.com/c3cbot/c3c-ufc-utility>`_ in your browser. Open a your Facebook account in a browser tab and use this extension to get your account cookies. Copy the cookies and save them in a json file. We will use the cookies for authentication instead of email and password. We will call this account ``Client`` account.

Your First Bot
--------------

Let's create a simple echo bot that replies to messages or send image files.:

.. code-block:: python

  from fbchat_muqit import Client, Message, EventType

  client = Client(cookies_file_path="cookies.json")

  # @client.event(EventType.LISTENING) you can also do this if you want a different name for the function instead of `on_listening`
  @client.event 
  async def on_listening():
      print(f"I'm online. Account name: {client.name} and uid: {client.uid}")
      # fetch all users clinet is chatting with. 
      all_users = await client.fetch_all_users()

      for user_id, user_data in all_users.items():
          print(f"User Id: {user_id} and user name {user_data.name}")


  @client.event
  async def on_message(message: Message):
          
      # To avoid spam check if sender_id is client's id or not
      if message.sender_id != client.uid:
          if message.text.startswith("/send image"):
              await client.send_message("sending please wait...", message.thread_id)

              await client.send_files_from_path(
                      file_paths=["/sdcard/my_picture.png", "/Download/hello.jpg"],
                      thread_id=message.thread_id
                      )
          else:
              # otherwise echo the message
              await client.send_message(message.text, message.thread_id)


  client.run()


.. _facebook-cookies:

Understanding Facebook Cookies
_________________________________

Facebook uses cookies small pieces of data stored in your browser to keep you logged in and identify your account.
When you log in to Facebook through a web browser, it creates several cookies (like c_user, xs, datr, fr, etc.) that contain information about your session and authentication state.

The fbchat-muqit library uses these cookies to authenticate with Facebook on your behalf, instead of asking for your email and password directly.
This allows the library to act as your logged-in account, send and receive messages, and interact with Messenger features securely.

You can think of cookies as a temporary access token if they expire or become invalid (for example, if you log out or change your password), you’ll need to provide new cookies to reconnect.

.. important:: Always keep your cookies private. Anyone with access to them can potentially log into your account.


Next Steps
----------

- Learn about :doc:`authentication`
- Explore :doc:`guides/sending-messages`
- Check out :doc:`examples/basic-bot`
