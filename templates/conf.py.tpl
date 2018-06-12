{%- if generated_text -%}
# {{ generated_text }}
#
# Make changes to ``project.toml``, and run ``flinx generate``, instead.
{% else %}
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config
{%- endif %}

import sys
{% if '.md' in source_suffix %}
from recommonmark.parser import CommonMarkParser
{% endif %}

sys.path.insert(0, '{{ module_path }}')

project = '{{ project }}'
copyright = {{ copyright | repr }}
author = '{{ author }}'
version = '{{ version }}'
release = '{{ version }}'

master_doc = '{{ master_basename }}'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
extensions = {{ extensions | repr }}
source_suffix = {{ source_suffix }}

{% if '.md' in source_suffix %}
source_parsers = { '.md': CommonMarkParser }
{% endif %}

{%- if 'sphinx.ext.intersphinx' in extensions %}
intersphinx_mapping = {'https://docs.python.org/': None}
{%- endif %}

{%- if 'sphinx.ext.todo' in extensions %}
todo_include_todos = True
{%- endif %}

{% for k, v in config_vars %}
{{ k }} = {{ v | repr }}
{% endfor %}
