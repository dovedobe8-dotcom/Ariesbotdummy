Attachment Models
=================

Classes for representing message attachments and media content.

Overview
--------

Attachments represent various types of media and content that can be sent or received in messages.
fbchat-muqit supports a wide variety of attachment types including images, videos, files, stickers,
and Facebook-specific content like posts, reels, and profiles.

.. code-block:: python

   from fbchat_muqit import ImageAttachment, VideoAttachment, PostAttachment
   
   # Attachments are automatically parsed from messages

   # inside on_message()
   message = await client.fetch_message_info(message_id, thread_id)
   
   for attachment in message.attachments:
       if isinstance(attachment, ImageAttachment):
           print(f"Image: {attachment.preview.url}")
       elif isinstance(attachment, VideoAttachment):
           print(f"Video: {attachment.playable_url}")

Attachment Types
----------------

.. autoclass:: fbchat_muqit.AttachmentType
   :members:
   :undoc-members:

Media Attachments
-----------------

Image Attachment
~~~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.ImageAttachment
   :members:
   :undoc-members:
   :show-inheritance:

Video Attachment
~~~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.VideoAttachment
   :members:
   :undoc-members:
   :show-inheritance:

GIF Attachment
~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.GifAttachment
   :members:
   :undoc-members:
   :show-inheritance:

Sticker Attachment
~~~~~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.StickerAttachment
   :members:
   :undoc-members:
   :show-inheritance:

Audio Attachment
~~~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.AudioAttachment
   :members:
   :undoc-members:
   :show-inheritance:

File Attachment
~~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.FileAttachment
   :members:
   :undoc-members:
   :show-inheritance:

Facebook Content Attachments
-----------------------------

Post Attachment
~~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.PostAttachment
   :members:
   :undoc-members:
   :show-inheritance:

Reel Attachment
~~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.ReelAttachment
   :members:
   :undoc-members:
   :show-inheritance:

Profile Attachment
~~~~~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.ProfileAttachment
   :members:
   :undoc-members:
   :show-inheritance:

Product Attachment
~~~~~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.ProductAttachment
   :members:
   :undoc-members:
   :show-inheritance:

Other Attachments
-----------------

Location Attachment
~~~~~~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.LocationAttachment
   :members:
   :undoc-members:
   :show-inheritance:

External Attachment
~~~~~~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.ExternalAttachment
   :members:
   :undoc-members:
   :show-inheritance:

Shared Attachment
~~~~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.SharedAttachment
   :members:
   :undoc-members:
   :show-inheritance:

Supporting Classes
------------------

Dimension
~~~~~~~~~

.. autoclass:: fbchat_muqit.Dimension
   :members:
   :undoc-members:

Image
~~~~~

.. autoclass:: fbchat_muqit.Image
   :members:
   :undoc-members:

Media
~~~~~

.. autoclass:: fbchat_muqit.Media
   :members:
   :undoc-members:

Author
~~~~~~

.. autoclass:: fbchat_muqit.Author
   :members:
   :undoc-members:

GroupInfo
~~~~~~~~~

.. autoclass:: fbchat_muqit.GroupInfo
   :members:
   :undoc-members:

Post
~~~~

.. autoclass:: fbchat_muqit.Post
   :members:
   :undoc-members:

Usage Examples
--------------

Checking Attachment Types
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

  import asyncio
  from fbchat_muqit import (
     Client, ImageAttachment, VideoAttachment, 
     StickerAttachment, FileAttachment
  )

  async def main():
      msg_id = "mid.behw.........."
      thread_id = "1000973........."
      async with Client(cookies_file_path="cookies.json") as client:
          message = await client.fetch_message_info(msg_id, thread_id)
    
          if message and message.attachments:
              for attachment in message.attachments:
                  if isinstance(attachment, ImageAttachment):
                     print(f"📷 Image: {attachment.filename}")
                     print(f"   URL: {attachment.preview.url}")
                     print(f"   Size: {attachment.original_dimensions.width}x"
                           f"{attachment.original_dimensions.height}x")
                 
                  elif isinstance(attachment, VideoAttachment):
                     print(f"🎥 Video: {attachment.filename}")
                     print(f"   Duration: {attachment.playable_duration}ms")
                     print(f"   URL: {attachment.playable_url}")
                 
                  elif isinstance(attachment, StickerAttachment):
                     print(f"😊 Sticker: {attachment.label}")
                     print(f"   Animated: {attachment.frame_count > 0}")
                 
                  elif isinstance(attachment, FileAttachment):
                     print(f"📎 File")
                     print(f"   Type: {attachment.mimetype}")
                     print(f"   Download: {attachment.download_url}")

  asyncio.run(main())

Downloading Attachments
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

  from fbchat_muqit import Client
  from fbchat_muqit.models import Message, ImageAttachment


  client = Client("cookies.json")


  # Usage
  @client.event
  async def on_message(message: Message):
      # if the message has a image attachment download the image
      if message.attachments:
          for attachment in message.attachments:
              if isinstance(attachment, ImageAttachment):
                  await client.download(attachment.large_preview.url, attachment.filename)

  client.run()

Working with Facebook Content's Attachment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import PostAttachment, ReelAttachment, ProfileAttachment
   
   for attachment in message.attachments:
       if isinstance(attachment, PostAttachment):
           print(f"📝 Facebook Post")
           print(f"   Title: {attachment.title}")
           print(f"   Author: {attachment.post.author[0].name}")
           print(f"   URL: {attachment.post_url}")
       
       elif isinstance(attachment, ReelAttachment):
           print(f"🎬 Facebook Reel")
           print(f"   Title: {attachment.title}")
           print(f"   Creator: {attachment.source}")
           print(f"   URL: {attachment.url}")
       
       elif isinstance(attachment, ProfileAttachment):
           print(f"👤 Profile Shared")
           print(f"   Name: {attachment.profile_name}")
           print(f"   URL: {attachment.profile_url}")

See Also
--------

- :doc:`message` - Message models that contain attachments
- :doc:`../client` - Client methods for sending attachments
- :doc:`/guides/attachments` - Guide on working with attachments
