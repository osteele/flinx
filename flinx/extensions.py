# Allow these names as shortcuts for sphinx.ext.*.
sphinx_builtin_extensions = ['autodoc', 'autosectionlabel', 'autosummary', 'coverage',
                             'doctest', 'extlinks', 'githubpages', 'graphviz',
                             'ifconfig', 'imgconverter',
                             'imgmath', 'mathjax', 'jsmith', 'inheritance_diagram',
                             'intersphinx', 'linkcode', 'napoleon', 'todo', 'viewcode']

# Configuration variables that start with image_ imply the imgconverter (not image)
# extension, etc.
config_var_ext_prefixes = {
    'autoclass': 'autodoc',
    'image': 'imgconverter',
    'inheritance': 'inheritance_diagram',
}

# Use this, if the user doesn't specify extensions.
default_extensions = ['autodoc']


def get_extensions(config_vars):
    """Infer the extensions from the Sphinx configuration variables."""
    # expand shortcut names
    extensions = ['sphinx.ext.' + ext
                  if ext in sphinx_builtin_extensions else ext
                  for ext in config_vars.get('extensions', default_extensions)]
    # add extensions implied by configuration value names
    prefixes = {k.split('_', 1)[0] for k in config_vars.keys() if '_' in k}
    detected_exts = (config_var_ext_prefixes.get(prefix, prefix)
                     for prefix in prefixes)
    auto_exts = sorted('sphinx.ext.' + ext
                       for ext in detected_exts
                       if ext in sphinx_builtin_extensions)
    for ext in auto_exts:
        if ext not in extensions:
            extensions.append(ext)
    return extensions
