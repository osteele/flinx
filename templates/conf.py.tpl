# THIS FILE IS GENERATED AUTOMATICALLY BY FLINX. MANUAL CHANGES WILL BE LOST.
# Make changes to project.toml, and run ``flinx generate``, instead.

import os
import sys
sys.path.insert(0, '{{ module_path }}')

project = '{{ project }}'
copyright = {{ copyright | repr }}
author = '{{ author }}'

version = '{{ version }}'
release = '{{ version }}'

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.napoleon',
              'sphinx.ext.viewcode',
              'sphinx.ext.intersphinx']

templates_path = ['_templates']

# source_suffix = ['.rst', '.md']
source_suffix = '.rst'
master_doc = '{{ master_basename }}'
language = {{ language | repr }}
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'

## HTML output options
html_theme = 'alabaster'
# html_theme_options = {}
#html_static_path = ['_static']

# HTMLHelp output options
#htmlhelp_basename = '{{ project_fn }}doc'

## LaTeX output options
latex_elements = {
    # 'papersize': 'letterpaper',
    # 'pointsize': '10pt',
    # 'preamble': '',
    # 'figure_align': 'htbp',
}

#latex_documents = [
#    (master_doc, '{{ project_fn }}.tex', u'{{ project_doc_texescaped_str }}',
#     u'{{ author_texescaped_str }}', 'manual'),
#]

## Manual page output options
#man_pages = [
#    (master_doc, '{{ project_manpage }}', u'{{ project_doc_str }}',
#     [author], 1)
#]

## Texinfo output options
#texinfo_documents = [
#    (master_doc, '{{ project_fn }}', u'{{ project_doc_str }}',
#     author, '{{ project_fn }}', 'One line description of project.',
#     'Miscellaneous'),
#]

## Epub output options

# Bibliographic Dublin Core info.
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']

{%- if 'sphinx.ext.intersphinx' in extensions %}
intersphinx_mapping = {'https://docs.python.org/': None}
{%- endif %}

{%- if 'sphinx.ext.todo' in extensions %}
todo_include_todos = True
{%- endif %}
