# Configuration file for the Sphinx documentation builder.
import os
import sys

sys.path.insert(0, os.path.abspath('../../'))

from fbchat_muqit import __version__

project = 'fbchat-muqit'
copyright = '2025, Muhammad MuQiT'
author = 'Muhammad MuQiT'
release = __version__
version = release

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc.typehints',
    'sphinx.ext.intersphinx',
    # "sphinx.ext.extlinks",
]

# Napoleon settings
napoleon_google_docstring = True 
napoleon_include_init_with_doc = True
napoleon_use_param = True
napoleon_use_rtype = True

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'groupwise',
    'undoc-members': False,
    'show-inheritance': True,
    'inherited-members': True,
    'private-members': False,
    'special-members': False,
}

autodoc_member_order = "bysource"
autodoc_class_signature = "separated"


# Skip submodules that should be excluded from documentation
def skip_submodules(app, what, name, obj, skip, options):
    """Skip members from excluded modules."""

    excluded_modules = [
        'fbchat_muqit.models.deltas',
        'fbchat_muqit.models.mqtt_response',
        'fbchat_muqit.exception',
        'fbchat_muqit.logging',
    ]
    
    if hasattr(obj, '__module__'):
        for excluded in excluded_modules:
            if obj.__module__ and obj.__module__.startswith(excluded):
                return True
    return skip

def setup(app):
    """Sphinx setup hook."""
    app.connect('autodoc-skip-member', skip_submodules)

templates_path = ['_templates']
exclude_patterns = []  # This only affects .rst files, not Python modules

# -- Options for HTML output -------------------------------------------------

html_theme = 'furo'
html_static_path = ['_static']
html_show_sphinx = False
html_show_sourcelink = False

html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/fontawesome.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/solid.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/brands.min.css",
]


html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "blue",
        "color-brand-content": "#CC3333",
    },
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/togashigreat/fbchat-muqit",
            "html": "",
            "class": "fa-brands fa-solid fa-github fa-2x",
        },
    ],
    "sidebar_hide_name": True,
    "navigation_with_keys": True,
}


