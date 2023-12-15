Modules
=======

.. image:: _static/logo.svg

**PyMOL-PUB** package consists of 3 modules:

- handle module (`handles.py <https://github.com/BGI-SynBio/PyMOL-PUB/blob/main/molpub/handles.py>`_): provides a comprehensive set of operations for working with structured data, performing loading and saving operations, splicing and property assignment operations, and alignment-related calculations.

- layout module (`layouts.py <https://github.com/BGI-SynBio/PyMOL-PUB/blob/main/molpub/layouts.py>`_): is responsible for figure processing and rendering operations.

- config module (`windows.py <https://github.com/BGI-SynBio/PyMOL-PUB/blob/main/molpub/windows.py>`_): provides a Graphical User Interface protocol, allowing users without programming experience to complete the production of publication-quality figures.

.. toctree::
   :maxdepth: 2

Handle Module
------------------------------------------
.. autoclass:: molpub.handles.Monitor
  :members:
  :undoc-members:
  :show-inheritance:

.. autoclass:: molpub.handles.Score
  :members:
  :undoc-members:
  :show-inheritance:

.. autofunction:: molpub.handles.similar
.. autofunction:: molpub.handles.cluster
.. autofunction:: molpub.handles.align
.. autofunction:: molpub.handles.set_properties
.. autofunction:: molpub.handles.set_difference
.. autofunction:: molpub.handles.kmer
.. autofunction:: molpub.handles.load_structure_from_file
.. autofunction:: molpub.handles.save_structure_to_file

Layout Module
------------------------------------------
.. autoclass:: molpub.layouts.Figure
  :members:
  :undoc-members:
  :show-inheritance:

.. autoclass:: molpub.layouts.DefaultStructureImage
  :members:
  :undoc-members:
  :show-inheritance:

.. autoclass:: molpub.layouts.HighlightStructureImage
  :members:
  :undoc-members:
  :show-inheritance:

.. autoclass:: molpub.layouts.PropertyStructureImage
  :members:
  :undoc-members:
  :show-inheritance:

.. autofunction:: molpub.layouts.obtain_widget_icon
