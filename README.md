# PyMOL-advance: high-level interface from structure data to publication-standard figures

With the rapid progress of fields like protein structure prediction, 
an increasing number of researchers from different backgrounds require the use of 
[PyMOL](https://pymol.org/2/) for molecular visualization.
To be used in publications, the default visualization output of PyMOL typically requires 
the spatial adjustments, such as rotating and/or zooming the structures, and 
purposeful emphasis including highlighting important parts and hiding the unimportant parts.
Meanwhile, the need for batch visualization has been demonstrated by recent publications in high-impact journals.
However, these adjustments and batch protocols require the involvement of many skilled personnel, are expensive, 
and operate at human speeds, all of which make them worthy of automation.
Based on the original design of PyMOL and as an important supplement, 
we develop a high-level interface in order to generate figures capable of reaching the 
publication standard with configuration or a few codes.
By using our tool, the manual operations can be greatly reduced, 
and the desired image output can be obtained with a few lines of code or only configuration.

<p align="center">
    <img src="https://github.com/BGI-SynBio/PyMOL-advance/blob/main/docs/source/_static/overview.png"/>
</p>

## Case presentation
Based on three structures with default visualization output 

<table width="100%" align="center", table-layout:fixed>
    <tr>
        <td bgcolor="#FFFFFF" bgcolor="#FFFFFF" align="center">1AY7</td>
        <td bgcolor="#FFFFFF" bgcolor="#FFFFFF" align="center">1F34</td>
        <td bgcolor="#FFFFFF" bgcolor="#FFFFFF" align="center">1YCR</td>
    </tr>
    <tr>
        <td bgcolor="#FFFFFF">
            <img width="100%" src="https://github.com/BGI-SynBio/PyMOL-advance/blob/main/cases/baseline/1.1AY7.png"/>
        </td>
        <td bgcolor="#FFFFFF">
            <img width="100%" src="https://github.com/BGI-SynBio/PyMOL-advance/blob/main/cases/baseline/1.1F34.png"/>
        </td>
        <td bgcolor="#FFFFFF">
            <img width="100%" src="https://github.com/BGI-SynBio/PyMOL-advance/blob/main/cases/baseline/1.1YCR.png"/>
        </td>
    </tr>
</table>

an ideal publication-standard figure 

<p align="center">
    <img width="40%" src="https://github.com/BGI-SynBio/PyMOL-advance/blob/main/cases/designed/1.png"/>
</p>

can be [created](https://github.com/BGI-SynBio/PyMOL-advance/blob/main/cases/case_1.py) 
using 55 lines of code, which is similar to Figure 1 of 
[Carles Corbi-Verge et al. work](https://biosignaling.biomedcentral.com/articles/10.1186/s12964-016-0131-4).

Furthermore, we provide some high-level visualization usage 
for displaying physicochemical properties and alignment comparison results (e.g. RMSD) of target structure(s).
For example, the following left panel describes the difference 
between the expected structure and the predicted structure, 
reported in Figure 1 of [Zeming Lin et al. work](https://www.science.org/doi/abs/10.1126/science.ade2574).
Here, to avoid a cluttered information in the structure overlapping parts, 
we depict solely the predicted structure (center panel), and illustrate the difference 
between the predicted and anticipated structures by 
varying the thickness and gradient color of the cartoon representation (see the following right panel).


<table width="100%" align="center", table-layout:fixed>
    <tr>
        <td bgcolor="#FFFFFF" bgcolor="#FFFFFF" align="center">expected</td>
        <td bgcolor="#FFFFFF" bgcolor="#FFFFFF" align="center">designed (equal)</td>
        <td bgcolor="#FFFFFF" bgcolor="#FFFFFF" align="center">designed (improve)</td>
    </tr>
    <tr>
        <td bgcolor="#FFFFFF">
            <img width="33%" src="https://github.com/BGI-SynBio/PyMOL-advance/blob/main/cases/expected/3.png"/>
        </td>
        <td bgcolor="#FFFFFF">
            <img width="33%" src="https://github.com/BGI-SynBio/PyMOL-advance/blob/main/cases/designed/3.png"/>
        </td>
        <td bgcolor="#FFFFFF">
            <img width="33%" src="https://github.com/BGI-SynBio/PyMOL-advance/blob/main/cases/designed/3(clearer).png"/>
        </td>
    </tr>
</table>

## Installation
You can install it using pip:

```sh
pip install PyMOL-advance
```

Or you can also install it from source after installing [git](https://git-scm.com/):

```sh
git clone https://github.com/BGI-SynBio/PyMOL-advance.git
cd PyMOL-advance
pip install -r requirements.txt
python setup.py install develop --user
```

The tool requires 
[Python >= 3.7.3](https://www.python.org/downloads/release/python-373/).
As the foundation of this tool, we require version of PyMOL to be greater than or equal to 2.5.0.
Please refer to the [official website](https://pymol.org/2/#download) for installation protocol details.
 
Moreover, some well-established libraries: 
[biopython >= 1.78](https://pypi.org/project/biopython/1.78/), 
[matplotlib >= 3.1.1](https://pypi.org/project/matplotlib/3.1.1/), 
[numpy >= 1.21.2](https://pypi.org/project/numpy/1.21.2/), 
[pillow >= 8.2.0](https://pypi.org/project/Pillow/8.2.0/) and 
[scipy >= 1.4.1](https://pypi.org/project/scipy/1.4.1/).


## Customizations and protocols
### Scalable string expression for part selection
We present a string expression to describe two types of selection scheme, 
one is "all" and another is "type:target,target,...,target",
which avoids users from needing to input extensive selection information based on the original PyMOL design.

Here, "type" is selection class, including (1) "position", (2) "range", (3) "residue", (4) "segment", 
(5) "chain" and (6) "model".
"target" represents the selection range under the corresponding "type".

Some examples are shown below:
```python
# select the model called "predicted".
a = "model:predicted"
# select A-chain.
b = "chain:A"
# select segment "NPGP" in all chains.
c = "segment:NPGP"
# select residue "HOH" in all chains.
d = "residue:HOH"
# select range from 10 to 20 and from 50 to 60 in all chains.
e = "range:10-20,50-60"
# select 10-th position in all chains.
f = "position:10"
```
For types below the chain scale, i.e. type (1) - (4), 
we provide a built-in chain description mechanism for more accurate selection.
For example:

```python
# select range from 10 to 20 in all chains.
a = "range:10-20"
# select range from 10 to 20 in A-chain.
b = "range:A+10-200"
```

### Structure image creation
For the structure image, two types of rendering objectives have been offered: 
the first aims to accentuate specific region(s), 
and the second intends to showcase element (deoxyribonucleic acid, ribonucleic acid and amino acid) 
property information in the structure.
The [HighlightStructureImage](https://github.com/BGI-SynBio/PyMOL-advance/blob/main/mola/layouts.py#L303) class 
can offer adequate services for the former, 
whereas the 
[PropertyStructureImage](https://github.com/BGI-SynBio/PyMOL-advance/blob/main/mola/layouts.py#L418) class 
is developed for the latter.

Irrespective of the structure visualisation method, 
as applicable in all cases, 
the recommended function calling order (not mandatory) is to 
(1) omit unnecessary parts by 
["set_cache"](https://github.com/BGI-SynBio/PyMOL-advance/blob/main/mola/layouts.py#L29) function, 
(2) adjust the structure's spatial orientation by
["set_state"](https://github.com/BGI-SynBio/PyMOL-advance/blob/main/mola/layouts.py#L127) function, 
(3) modify the structure or its parts representation by
["set_shape"](https://github.com/BGI-SynBio/PyMOL-advance/blob/main/mola/layouts.py#L174) function, 
(4) complete coloring of the structure or its parts 
by highlight [coloring](https://github.com/BGI-SynBio/PyMOL-advance/blob/main/mola/layouts.py#L305) 
or property driven [coloring](https://github.com/BGI-SynBio/PyMOL-advance/blob/main/mola/layouts.py#L420),
both called "set_color" function in the corresponding class,
and (5) save the image by ["save"](https://github.com/BGI-SynBio/PyMOL-advance/blob/main/mola/layouts.py#L283) function.

A highlight structure image example can be:
```python
from mola.layouts import HighlightStructureImage

# create a structure image based on a structure file "structure.pdb".
image = HighlightStructureImage(structure_paths=["structure.pdb"])
# hide all water molecules.
image.set_cache(cache_contents=["residue:HOH"])
# rotate the structure according to the x-axis 240 degrees, y-axis 340 degrees, and z-axis 90 degrees.
image.set_state(rotate=[240, 340, 90])
# set A-chain to surface representation and B-chain to cartoon representation.
image.set_shape(representation_plan=[("chain:A", "surface"), ("chain:B", "cartoon")])
# set A-chain to "0xF2F2F2" color and B-chain to "0x2D2F82" color.
image.set_color(coloring_plan=[("chain:A", "0xF2F2F2"), ("chain:B", "0x2D2F82")])
# save the structure with the width 1280 and the height 1280 * 0.8 = 1024.
image.save(save_path="structure.png", width=1280, ratio=0.8)
```

Besides, a property driven structure image example can be:

```python
from mola.layouts import PropertyStructureImage

# create a structure image based on two structure files "expected.pdb" and "predicted.pdb".
image = PropertyStructureImage(structure_paths=["expected.pdb", "predicted.pdb"])
# rotate the structure according to the x-axis 0 degrees, y-axis 60 degrees, and z-axis 255 degrees.
# and align two structures based on the PyMOL built-in method using the expected structure as a template.
image.set_state(rotate=[0, 60, 255], inner_align=True, target="expected")
# set two structures to cartoon representation.
image.set_shape(representation_plan=[("model:predicted", "cartoon"), ("model:expected", "cartoon")])
# set the color of predicted structure is the rainbow spectrum, starting in red and ending in purple.
image.set_color(target="model:predicted", color_map="rainbow", edge_color="0x000000", gauge_strengthen=True)
# save the structure with the width 1800 and the height 1800 * 0.5 = 900.
image.save(save_path="aligned_structure.png", width=1800, ratio=0.5)
```

More comparable cases are attached in the [cases](https://github.com/BGI-SynBio/PyMOL-advance/tree/main/cases) folder.


### Publication-standard figure creation
At the figure level, we can customize the target publication format during the 
[initialization](https://github.com/BGI-SynBio/PyMOL-advance/blob/main/mola/layouts.py#L493) of the figure.
The supporting figure formats of journal, conference or publisher are:

<table width="100%" align="center", table-layout:fixed>
    <tr>
        <th bgcolor="#FFFFFF" align="center" rowspan="2">target</th>
        <th bgcolor="#FFFFFF" align="center" rowspan="2">font</th>
        <th bgcolor="#FFFFFF" align="center" rowspan="2">math font</th>
        <th bgcolor="#FFFFFF" align="center" rowspan="2">dots per inch (dpi)</th>
        <th bgcolor="#FFFFFF" align="center" rowspan="2">max columns</th>
        <th colspan="3">width under column occupy (inches)</th>
    </tr>
    <tr>
        <th bgcolor="#FFFFFF" align="center">1</th>
        <th bgcolor="#FFFFFF" align="center">2</th>
        <th bgcolor="#FFFFFF" align="center">3</th>
    </tr>
    <tr>
        <td bgcolor="#FFFFFF" align="center"><a href="https://www.nature.com/nature/for-authors/formatting-guide">Nature</a></td>
        <td bgcolor="#FFFFFF" align="center">Arial</td>
        <td bgcolor="#FFFFFF" align="center" rowspan="9">Linux Libertine<br/>&<br/>Lucida Calligraphy</th>
        <td bgcolor="#FFFFFF" align="center">300</td>
        <td bgcolor="#FFFFFF" align="center">2</td>
        <td bgcolor="#FFFFFF" align="center">3.54</td>
        <td bgcolor="#FFFFFF" align="center">7.08</td>
        <td bgcolor="#FFFFFF" align="center">-</td>
    </tr>
    <tr>
        <td bgcolor="#FFFFFF" align="center"><a href="https://www.science.org/content/page/instructions-preparing-initial-manuscript#preparation-of-figures">Science</a></td>
        <td bgcolor="#FFFFFF" align="center">Helvetica</td>
        <td bgcolor="#FFFFFF" align="center">300</td>
        <td bgcolor="#FFFFFF" align="center">3</td>
        <td bgcolor="#FFFFFF" align="center">2.24</td>
        <td bgcolor="#FFFFFF" align="center">4.76</td>
        <td bgcolor="#FFFFFF" align="center">7.24</td>
    </tr>
    <tr>
        <td bgcolor="#FFFFFF" align="center" rowspan="2"><a href="https://www.cell.com/figureguidelines">Cell</a></td>
        <td bgcolor="#FFFFFF" align="center" rowspan="2">Arial</td>
        <td bgcolor="#FFFFFF" align="center" rowspan="2">300</td>
        <td bgcolor="#FFFFFF" align="center">2</td>
        <td bgcolor="#FFFFFF" align="center">3.35</td>
        <td bgcolor="#FFFFFF" align="center">6.85</td>
        <td bgcolor="#FFFFFF" align="center">-</td>
    </tr>
    <tr>
        <td bgcolor="#FFFFFF" align="center">3</td>
        <td bgcolor="#FFFFFF" align="center">2.17</td>
        <td bgcolor="#FFFFFF" align="center">4.49</td>
        <td bgcolor="#FFFFFF" align="center">6.85</td>
    </tr>
    <tr>
        <td bgcolor="#FFFFFF" align="center"><a href="https://www.pnas.org/author-center/submitting-your-manuscript">PNAS</a></td>
        <td bgcolor="#FFFFFF" align="center">Helvetica</td>
        <td bgcolor="#FFFFFF" align="center">600</td>
        <td bgcolor="#FFFFFF" align="center">2</td>
        <td bgcolor="#FFFFFF" align="center">3.42</td>
        <td bgcolor="#FFFFFF" align="center">7.00</td>
        <td bgcolor="#FFFFFF" align="center">-</td>
    </tr>
    <tr>
        <td bgcolor="#FFFFFF" align="center"><a href="https://pubs.acs.org/page/4authors/submission/graphics_prep.html">ACS</a></td>
        <td bgcolor="#FFFFFF" align="center">Arial</td>
        <td bgcolor="#FFFFFF" align="center">600</td>
        <td bgcolor="#FFFFFF" align="center">2</td>
        <td bgcolor="#FFFFFF" align="center">3.25</td>
        <td bgcolor="#FFFFFF" align="center">7.00</td>
        <td bgcolor="#FFFFFF" align="center">-</td>
    </tr>
    <tr>
        <td bgcolor="#FFFFFF" align="center"><a href="https://academic.oup.com/bioinformatics/pages/instructions_for_authors">Oxford</a></td>
        <td bgcolor="#FFFFFF" align="center">Arial</td>
        <td bgcolor="#FFFFFF" align="center">350</td>
        <td bgcolor="#FFFFFF" align="center">2</td>
        <td bgcolor="#FFFFFF" align="center">3.39</td>
        <td bgcolor="#FFFFFF" align="center">7.00</td>
        <td bgcolor="#FFFFFF" align="center">-</td>
    </tr>
    <tr>
        <td bgcolor="#FFFFFF" align="center"><a href="https://journals.plos.org/ploscompbiol/s/figures">PLOS</a></td>
        <td bgcolor="#FFFFFF" align="center">Arial</td>
        <td bgcolor="#FFFFFF" align="center">300</td>
        <td bgcolor="#FFFFFF" align="center">1</td>
        <td bgcolor="#FFFFFF" align="center">5.20</td>
        <td bgcolor="#FFFFFF" align="center">-</td>
        <td bgcolor="#FFFFFF" align="center">-</td>
    </tr>
    <tr>
        <td bgcolor="#FFFFFF" align="center"><a href="https://www.ieee.org/content/dam/ieee-org/ieee/web/org/pubs/format-definition-table-and-glossary.pdf">IEEE</a></td>
        <td bgcolor="#FFFFFF" align="center">Times New Roman</td>
        <td bgcolor="#FFFFFF" align="center">300</td>
        <td bgcolor="#FFFFFF" align="center">2</td>
        <td bgcolor="#FFFFFF" align="center">3.50</td>
        <td bgcolor="#FFFFFF" align="center">7.25</td>
        <td bgcolor="#FFFFFF" align="center">-</td>
    </tr>
</table>

The target figure can be set to the Science format and full width by constructing the subsequent object.

```python
from mola.layouts import Figure
figure = Figure(manuscript_format="Science", occupied_columns=3)
```

Once the figure has been created, 
it is possible to insert the generated structure image(s) into it 
by utilizing the ["set_image"](https://github.com/BGI-SynBio/PyMOL-advance/blob/main/mola/layouts.py#L692) function 
or paint various outcomes, 
like [line chart, bar chart, violin chart, and so on](https://matplotlib.org/stable/gallery/index), 
through the ["set_panel"](https://github.com/BGI-SynBio/PyMOL-advance/blob/main/mola/layouts.py#L663) function.
The [Figure](https://github.com/BGI-SynBio/PyMOL-advance/blob/main/mola/layouts.py#L491) class 
also provides a 
[grid selection](https://github.com/BGI-SynBio/PyMOL-advance/blob/main/mola/layouts.py#L644) function
since publications usually have varying information to display in one figure.

## Configuration-driven figure creation
In preparation

## Acknowledgements
This work is funded by 
[Warren L. DeLano Memorial PyMOL Open-Source Fellowship](http://pymol.org/fellowship). 
We thank Dr. Jarrett Johnson from Schrödinger, Inc. for constructive discussions 
on functional design and implementation mode.