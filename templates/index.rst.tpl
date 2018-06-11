{%- if generated_text -%}
# {{ generated_text }}
#
# Make changes to ``project.toml``, and run ``flinx generate``, instead.

{% endif -%}

{% if readme %}
.. include:: {{ readme | project_rel }}
{% endif -%}

.. toctree::
   :maxdepth: 2
   :caption: Contents:


API
---

.. automodule:: {{ module_name }}
    :members:
