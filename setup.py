from setuptools import setup

setup(
    name="PyMOL-advance",
    version="0.1",
    description="PyMOL-advance: high-level interfaces from structure data to publication-standard figures",
    long_description="With the rapid progress of fields like protein structure prediction, "
                     "an increasing number of researchers from different backgrounds require the use of PyMOL for "
                     "molecular visualization. To be used in publications, the default visualization output of PyMOL "
                     "typically requires the spatial adjustments, such as rotating and/or zooming the structures, "
                     "and purposeful emphasis including highlighting important parts and hiding the unimportant parts. "
                     "Meanwhile, the need for batch visualization has been demonstrated by recent publications "
                     "in high-impact journals. However, these adjustments and batch protocols require the involvement "
                     "of many skilled personnel, are expensive, and operate at human speeds, all of which make them "
                     "worthy of automation. Based on the original design of PyMOL and as an important supplement, "
                     "we develop a high-level interface in order to generate figures capable of reaching "
                     "the publication standard. By using our tool, the manual operations can be greatly reduced, "
                     "and the desired image output can be obtained with a few lines of code or only configuration.",
    author="Haoling Zhang",
    author_email="zhanghaoling@genomics.cn",
    url="https://github.com/BGI-SynBio/PyMOL-PUB",
    packages=["molpub", "cases"],
    install_requires=["numpy", "pymol", "pillow", "biopython", "matplotlib"],
    license="GPL",
    classifiers=["License :: OSI Approved :: GNU General Public License (GPL)",
                 "Programming Language :: Python :: 3",
                 "Operating System :: OS Independent"],
    keywords="PyMOL, batch visualization",
)
