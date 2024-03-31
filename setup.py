from setuptools import setup

setup(
    name="PyMOL-PUB",
    version="1.2",
    description="Rapid generation of high-quality structure figures for publication with PyMOL-PUB",
    long_description="The advancement of structural biology has increased the requirements for researchers "
                     "to quickly and efficiently visualize molecular structures in silico. "
                     "Meanwhile, it is also time-consuming for structural biologists "
                     "to create publication-standard figures, as no useful tools can directly generate figures "
                     "from structure data. Although manual editing can ensure that figures meet the standards "
                     "required for publication, it requires a deep understanding of software operations "
                     "and/or program call commands. Therefore, providing interfaces based on established software "
                     "instead of manual editing becomes a significant necessity. "
                     "We developed PyMOL-PUB, based on the original design of PyMOL, "
                     "to effectively create publication-quality figures from molecular structure data. "
                     "It provides functions including structural alignment methods, functional coloring schemes, "
                     "conformation adjustments, and layout plotting strategies. These functions allow users "
                     "to easily generate high-quality figures, demonstrate structural differences, "
                     "illustrate inter-molecular interactions and predict performances of biomacromolecules.",
    author="Haoling Zhang",
    author_email="zhanghaoling@genomics.cn",
    url="https://github.com/BGI-SynBio/PyMOL-PUB",
    packages=["molpub", "cases", "tests"],
    install_requires=["numpy", "pymol", "pillow", "biopython", "matplotlib"],
    license="GPL",
    classifiers=["License :: OSI Approved :: GNU General Public License (GPL)",
                 "Programming Language :: Python :: 3",
                 "Operating System :: OS Independent"],
    keywords="pymol, pymol-pub, matplotlib, structure-cluster, structure-alignment, manuscript-figure",
)
