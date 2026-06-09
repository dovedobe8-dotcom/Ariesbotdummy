Theme Models
============

Classes for representing Messenger thread themes and their styling properties.

Overview
--------

Theme models contain information about the visual appearance of Messenger threads,
including colors, gradients, assets, and alternative theme variants (like dark mode).

.. code-block:: python

   from fbchat_muqit import Client
   
   async with Client(cookies_file_path="cookies.json") as client:
       # Fetch available themes
       themes = await client.fetch_thread_themes()
       
       for theme in themes:
           print(f"🎨 {theme.accessibility_label}")
           print(f"   ID: {theme.id}")
           print(f"   Colors: {', '.join(theme.gradient_colors)}")
       
       # Change thread theme
       # call it after starting event listening
       await client.change_thread_theme(
           thread_id="123456789",
           theme_id=themes[0].id
       )

Theme Classes
-------------

Theme
~~~~~

.. autoclass:: fbchat_muqit.Theme
   :members:
   :undoc-members:
   :show-inheritance:

Alternative Theme
~~~~~~~~~~~~~~~~~

.. autoclass:: fbchat_muqit.AlternativeTheme
   :members:
   :undoc-members:
   :show-inheritance:

Asset
~~~~~

.. autoclass:: fbchat_muqit.Asset
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
--------------

Fetching Available Themes
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Client
   
   async with Client(cookies_file_path="cookies.json") as client:
       # Fetch all available themes
       themes = await client.fetch_thread_themes()
       
       print(f"📚 Available Themes: {len(themes)}")
       print()
       
       for i, theme in enumerate(themes, 1):
           print(f"{i}. {theme.accessibility_label}")
           print(f"   Theme ID: {theme.id}")
           print(f"   Description: {theme.description or 'No description'}")
           print(f"   Color Mode: {theme.app_color_mode}")
           print(f"   Gradient Colors: {len(theme.gradient_colors)} colors")
           
           if theme.gradient_colors:
               print(f"   Colors: {', '.join(theme.gradient_colors[:3])}")
           
           if theme.icon_asset:
               print(f"   Has Icon: ✅")
           
           if theme.background_asset:
               print(f"   Has Background: ✅")
           
           print()

Changing Thread Theme
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Client
   
   async with Client(cookies_file_path="cookies.json") as client:
       thread_id = "123456789"
       
       # Fetch available themes
       themes = await client.fetch_thread_themes()
       
       # Display theme options
       print("Available Themes:")
       for i, theme in enumerate(themes, 1):
           print(f"{i}. {theme.accessibility_label}")
       
       # Change to a specific theme
       selected_theme = themes[0]  # Select first theme
       
       await client.change_thread_theme(
           thread_id=thread_id,
           theme_id=selected_theme.id
       )
       
       print(f"✅ Changed theme to: {selected_theme.accessibility_label}")

Building a Theme Browser
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Client, Theme
   from typing import List, Optional
   
   class ThemeBrowser:
       """Browse and search themes."""
       
       def __init__(self):
           self.themes: List[Theme] = []
       
       async def load_themes(self, client: Client):
           """Load all available themes."""
           self.themes = await client.fetch_thread_themes()
           print(f"📚 Loaded {len(self.themes)} themes")
       
       def search_by_name(self, query: str) -> List[Theme]:
           """Search themes by name."""
           query = query.lower()
           return [
               theme for theme in self.themes
               if query in theme.accessibility_label.lower() or
                  (theme.description and query in theme.description.lower())
           ]
       
       def get_by_color(self, color: str) -> List[Theme]:
           """Find themes containing a specific color."""
           color = color.lower().replace('#', '')
           return [
               theme for theme in self.themes
               if any(color in c.lower().replace('#', '') 
                      for c in theme.gradient_colors)
           ]
       
       def get_by_mode(self, mode: str) -> List[Theme]:
           """Get themes by color mode (LIGHT/DARK)."""
           return [
               theme for theme in self.themes
               if theme.app_color_mode.upper() == mode.upper()
           ]
       
       def get_with_backgrounds(self) -> List[Theme]:
           """Get themes with background assets."""
           return [
               theme for theme in self.themes
               if theme.background_asset is not None
           ]
       
       def get_deprecated(self) -> List[Theme]:
           """Get deprecated themes."""
           return [
               theme for theme in self.themes
               if theme.is_deprecated
           ]
       
       def display_theme_details(self, theme: Theme):
           """Display detailed theme information."""
           print("=" * 70)
           print(f"THEME: {theme.accessibility_label}".center(70))
           print("=" * 70)
           print()
           print(f"🆔 Theme ID: {theme.id}")
           
           if theme.description:
               print(f"📝 Description: {theme.description}")
           
           print(f"🌓 Color Mode: {theme.app_color_mode}")
           print(f"🎨 Gradient Colors: {len(theme.gradient_colors)}")
           
           for i, color in enumerate(theme.gradient_colors, 1):
               print(f"   {i}. {color}")
           
           print()
           print("Colors:")
           if theme.composer_background_color:
               print(f"  📝 Composer Background: {theme.composer_background_color}")
           if theme.title_bar_background_color:
               print(f"  📱 Title Bar: {theme.title_bar_background_color}")
           if theme.message_text_color:
               print(f"  💬 Message Text: {theme.message_text_color}")
           if theme.hot_like_color:
               print(f"  ❤️  Hot Like: {theme.hot_like_color}")
           
           print()
           print("Assets:")
           if theme.icon_asset:
               print(f"  🎨 Icon: {theme.icon_asset.image}")
           if theme.background_asset:
               print(f"  🖼️  Background: {theme.background_asset.image}")
           
           print()
           print(f"Alternative Themes: {len(theme.alternative_themes)}")
           for alt in theme.alternative_themes:
               print(f"  • {alt.accessibility_label} ({alt.app_color_mode})")
           
           print()
           print(f"Status: {'⚠️  Deprecated' if theme.is_deprecated else '✅ Active'}")
           print("=" * 70)
   
   # Usage
   async with Client(cookies_file_path="cookies.json") as client:
       browser = ThemeBrowser()
       await browser.load_themes(client)
       
       # Search for blue themes
       blue_themes = browser.search_by_name("blue")
       print(f"Found {len(blue_themes)} blue themes:")
       for theme in blue_themes:
           print(f"  - {theme.accessibility_label}")
       
       # Get dark mode themes
       dark_themes = browser.get_by_mode("DARK")
       print(f"\n🌙 Dark themes: {len(dark_themes)}")
       
       # Get themes with backgrounds
       bg_themes = browser.get_with_backgrounds()
       print(f"🖼️  Themes with backgrounds: {len(bg_themes)}")
       
       # Display detailed info
       if blue_themes:
           print("\nDetailed view of first blue theme:")
           browser.display_theme_details(blue_themes[0])


Random Theme Changer
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Client
   import random
   import asyncio
   
   class RandomThemeChanger:
       """Automatically change thread theme randomly."""
       
       def __init__(self, client: Client, thread_id: str):
           self.client = client
           self.thread_id = thread_id
           self.themes = []
           self.current_theme_index = 0
       
       async def load_themes(self):
           """Load available themes."""
           self.themes = await self.client.fetch_thread_themes()
           # Filter out deprecated themes
           self.themes = [t for t in self.themes if not t.is_deprecated]
           print(f"📚 Loaded {len(self.themes)} active themes")
       
       async def change_random_theme(self):
           """Change to a random theme."""
           if not self.themes:
               await self.load_themes()
           
           theme = random.choice(self.themes)
           await self.client.change_thread_theme(
               thread_id=self.thread_id,
               theme_id=theme.id
           )
           
           print(f"🎨 Changed theme to: {theme.accessibility_label}")
           return theme
       
       async def cycle_themes(self, interval: int = 300):
           """Cycle through themes automatically."""
           if not self.themes:
               await self.load_themes()
           
           print(f"🔄 Starting theme cycling (every {interval}s)")
           
           while True:
               theme = self.themes[self.current_theme_index]
               
               await self.client.change_thread_theme(
                   thread_id=self.thread_id,
                   theme_id=theme.id
               )
               
               print(f"🎨 [{self.current_theme_index + 1}/{len(self.themes)}] "
                     f"{theme.accessibility_label}")
               
               self.current_theme_index = (self.current_theme_index + 1) % len(self.themes)
               await asyncio.sleep(interval)
   
   # Usage
   async with Client(cookies_file_path="cookies.json") as client:
       changer = RandomThemeChanger(client, thread_id="123456789")
       
       # Change to random theme once
       await changer.change_random_theme()
       
       # Or cycle through all themes (run in background)
       # await changer.cycle_themes(interval=300)

Theme Recommendation
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Client, Theme
   from typing import List
   
   class ThemeRecommender:
       """Recommend themes based on preferences."""
       
       def __init__(self, themes: List[Theme]):
           self.themes = themes
       
       def recommend_by_mood(self, mood: str) -> List[Theme]:
           """Recommend themes based on mood."""
           mood_keywords = {
               'happy': ['love', 'rainbow', 'colorful', 'bright'],
               'calm': ['ocean', 'blue', 'peaceful', 'serene'],
               'energetic': ['red', 'orange', 'fire', 'vibrant'],
               'dark': ['dark', 'night', 'midnight', 'black'],
               'nature': ['green', 'forest', 'nature', 'earth']
           }
           
           keywords = mood_keywords.get(mood.lower(), [])
           recommendations = []
           
           for theme in self.themes:
               label_lower = theme.accessibility_label.lower()
               desc_lower = (theme.description or '').lower()
               
               if any(kw in label_lower or kw in desc_lower for kw in keywords):
                   recommendations.append(theme)
           
           return recommendations
       
       def recommend_for_time_of_day(self, hour: int) -> List[Theme]:
           """Recommend themes based on time of day."""
           if 6 <= hour < 12:
               # Morning - bright themes
               return [t for t in self.themes if t.app_color_mode == 'LIGHT']
           elif 12 <= hour < 18:
               # Afternoon - any theme
               return self.themes
           else:
               # Evening/Night - dark themes
               return [t for t in self.themes if t.app_color_mode == 'DARK']
   
   # Usage
   async with Client(cookies_file_path="cookies.json") as client:
       themes = await client.fetch_thread_themes()
       recommender = ThemeRecommender(themes)
       
       # Get recommendations by mood
       happy_themes = recommender.recommend_by_mood('happy')
       print(f"😊 Themes for happy mood: {len(happy_themes)}")
       for theme in happy_themes[:3]:
           print(f"  - {theme.accessibility_label}")
       
       # Get recommendations by time
       from datetime import datetime
       current_hour = datetime.now().hour
       time_themes = recommender.recommend_for_time_of_day(current_hour)
       print(f"\n🕐 Themes for current time ({current_hour}:00): {len(time_themes)}")

Exporting Theme Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Client, Theme
   import json
   
   async def export_themes_to_json(client: Client, output_file: str = "themes.json"):
       """Export all themes to a JSON file."""
       themes = await client.fetch_thread_themes()
       
       themes_data = []
       for theme in themes:
           theme_dict = {
               'id': theme.id,
               'name': theme.accessibility_label,
               'description': theme.description,
               'color_mode': theme.app_color_mode,
               'gradient_colors': theme.gradient_colors,
               'background_gradient_colors': theme.background_gradient_colors,
               'composer_background': theme.composer_background_color,
               'title_bar_background': theme.title_bar_background_color,
               'message_text_color': theme.message_text_color,
               'hot_like_color': theme.hot_like_color,
               'is_deprecated': theme.is_deprecated,
               'has_icon': theme.icon_asset is not None,
               'has_background': theme.background_asset is not None,
               'alternative_themes_count': len(theme.alternative_themes)
           }
           
           themes_data.append(theme_dict)
       
       with open(output_file, 'w') as f:
           json.dump(themes_data, f, indent=2)
       
       print(f"💾 Exported {len(themes_data)} themes to {output_file}")
   
   # Usage
   async with Client(cookies_file_path="cookies.json") as client:
       await export_themes_to_json(client)

Working with Alternative Themes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Client, Theme, AlternativeTheme
   
   async def explore_theme_variants(client: Client, theme_name: str):
       """Explore a theme and its alternative variants."""
       themes = await client.fetch_thread_themes()
       
       # Find the theme
       theme = next((t for t in themes if theme_name.lower() in t.accessibility_label.lower()), None)
       
       if not theme:
           print(f"❌ Theme '{theme_name}' not found")
           return
       
       print(f"🎨 Theme: {theme.accessibility_label}")
       print(f"   Main Color Mode: {theme.app_color_mode}")
       print(f"   Main Colors: {', '.join(theme.gradient_colors[:3])}")
       print()
       
       if theme.alternative_themes:
           print(f"Alternative Variants: {len(theme.alternative_themes)}")
           print()
           
           for i, alt_theme in enumerate(theme.alternative_themes, 1):
               print(f"{i}. {alt_theme.accessibility_label}")
               print(f"   Color Mode: {alt_theme.app_color_mode}")
               print(f"   Colors: {', '.join(alt_theme.gradient_colors[:3])}")
               
               if alt_theme.description:
                   print(f"   Description: {alt_theme.description}")
               
               print(f"   Status: {'⚠️  Deprecated' if alt_theme.is_deprecated else '✅ Active'}")
               print()
       else:
           print("No alternative variants available")
   
   # Usage
   async with Client(cookies_file_path="cookies.json") as client:
       await explore_theme_variants(client, "love")

Creating a Theme Preview
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from fbchat_muqit import Theme
   
   def generate_theme_preview_html(theme: Theme, output_file: str = "theme_preview.html"):
       """Generate an HTML preview of a theme."""
       gradient = ', '.join(theme.gradient_colors)
       
       html = f"""
       <!DOCTYPE html>
       <html>
       <head>
           <title>{theme.accessibility_label} - Theme Preview</title>
           <style>
               body {{
                   font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                   margin: 0;
                   padding: 20px;
                   background: linear-gradient(135deg, {gradient});
                   min-height: 100vh;
               }}
               .container {{
                   max-width: 800px;
                   margin: 0 auto;
                   background: white;
                   border-radius: 20px;
                   padding: 30px;
                   box-shadow: 0 10px 40px rgba(0,0,0,0.2);
               }}
               h1 {{
                   color: {theme.title_bar_background_color or '#000'};
                   margin-top: 0;
               }}
               .message {{
                   background: linear-gradient(135deg, {', '.join(theme.inbound_message_gradient_colors)});
                   color: {theme.inbound_message_text_color or '#fff'};
                   padding: 15px 20px;
                   border-radius: 20px;
                   margin: 10px 0;
                   max-width: 70%;
               }}
               .composer {{
                   background: {theme.composer_background_color or '#f0f0f0'};
                   padding: 15px;
                   border-radius: 25px;
                   margin-top: 20px;
               }}
               .color-palette {{
                   display: flex;
                   gap: 10px;
                   margin: 20px 0;
                   flex-wrap: wrap;
               }}
               .color-swatch {{
                   width: 50px;
                   height: 50px;
                   border-radius: 10px;
                   border: 2px solid #ddd;
               }}
               .info {{
                   color: #666;
                   margin: 10px 0;
               }}
           </style>
       </head>
       <body>
           <div class="container">
               <h1>{theme.accessibility_label}</h1>
               <p class="info">{theme.description or 'No description'}</p>
               
               <h2>Color Palette</h2>
               <div class="color-palette">
       """
       
       for color in theme.gradient_colors:
           html += f'<div class="color-swatch" style="background: {color};" title="{color}"></div>\n'
       
       html += """
               </div>
               
               <h2>Message Preview</h2>
               <div class="message">
                   This is how messages look with this theme! 💬
               </div>
               
               <div class="composer">
                   Type a message...
               </div>
               
               <h2>Theme Details</h2>
               <ul class="info">
       """
       
       html += f"<li>Theme ID: {theme.id}</li>\n"
       html += f"<li>Color Mode: {theme.app_color_mode}</li>\n"
       html += f"<li>Deprecated: {'Yes ⚠️' if theme.is_deprecated else 'No ✅'}</li>\n"
       html += f"<li>Alternative Themes: {len(theme.alternative_themes)}</li>\n"
       
       html += """
               </ul>
           </div>
       </body>
       </html>
       """
       
       with open(output_file, 'w') as f:
           f.write(html)
       
       print(f"📄 Generated preview: {output_file}")
   
   # Usage
   async with Client(cookies_file_path="cookies.json") as client:
       themes = await client.fetch_thread_themes()
       
       # Generate preview for first theme
       if themes:
           generate_theme_preview_html(themes[0])

See Also
--------

- :doc:`thread` - Thread models
- :doc:`thread_actions` - Thread action events
- :doc:`../client` - Client methods for theme management
- :doc:`/guides/customization` - Guide on customizing threads
