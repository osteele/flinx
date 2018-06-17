from flinx.extensions import get_extensions


def test_get_extensions():
    # default extensions
    assert set(get_extensions({})) == {'sphinx.ext.autodoc'}

    # copy long names
    assert 'test.ext' in get_extensions({'extensions': ['test.ext']})

    # expand shortcuts
    assert 'sphinx.ext.inheritance_diagram' in get_extensions({'extensions': ['inheritance_diagram']})

    # infer extensions
    assert 'sphinx.ext.autodoc' in get_extensions({'autoclass_content': 'class'})
    assert 'sphinx.ext.autodoc' in get_extensions({'autodoc_member_order': 'bysource'})
    assert 'sphinx.ext.autosectionlabel' in get_extensions({'autosectionlabel_prefix_document': True})
    assert 'sphinx.ext.autosummary' in get_extensions({'autosummary_generate': True})
    assert 'sphinx.ext.autosectionlabel' in get_extensions({'autosectionlabel_prefix_document': True})
    assert 'sphinx.ext.coverage' in get_extensions({'coverage_ignore_modules': []})
    assert 'sphinx.ext.doctest' in get_extensions({'doctest_path': '.'})
    assert 'sphinx.ext.graphviz' in get_extensions({'graphviz_dot': 'dot'})
    assert 'sphinx.ext.imgconverter' in get_extensions({'image_converter': '.'})
    assert 'sphinx.ext.inheritance_diagram' in get_extensions({'inheritance_graph_attrs': {}})
    assert 'sphinx.ext.intersphinx' in get_extensions({'intersphinx_mapping': {}})
    assert 'sphinx.ext.linkcode' in get_extensions({'linkcode_resolve': True})
    assert 'sphinx.ext.mathjax' in get_extensions({'mathjax_options': {}})
    assert 'sphinx.ext.napoleon' in get_extensions({'napoleon_google_docstring': True})
    assert 'sphinx.ext.todo' in get_extensions({'todo_include_todos': {}})
    assert 'sphinx.ext.viewcode' in get_extensions({'viewcode_follow_imported_members': True})

    # TODO:
    # assert 'sphinx.ext.extlinks' in get_extensions({'extlinks': {}})
    # assert 'sphinx.ext.mathjax' in get_extensions({'math_number_all': True})
    # assert 'sphinx.ext.mathjax' in get_extensions({'imgmath_image_format': True})
