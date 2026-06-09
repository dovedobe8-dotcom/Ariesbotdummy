Installation
============

Requirements
------------

- Python 3.8 or higher
- pip package manager

Installing fbchat-muqit
-----------------------

Using pip
~~~~~~~~~

The easiest way to install fbchat-muqit:

.. code-block:: bash

   pip install fbchat-muqit

For the latest development version:

.. code-block:: bash

   pip install git+https://github.com/togashigreat/fbchat-muqit.git

Using uv
~~~~~~~~

If you're using uv for package management:

.. code-block:: bash

   uv pip install fbchat-muqit

Virtual Environment
-------------------

It's recommended to use a virtual environment:

.. code-block:: bash

   # Create virtual environment
   python -m venv venv
   
   # Activate it
   # On Linux/Mac:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   
   # Install fbchat-muqit
   pip install fbchat-muqit

Verifying Installation
----------------------

.. code-block:: python

   import fbchat_muqit
   print(fbchat_muqit.__version__)
