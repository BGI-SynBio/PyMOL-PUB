from setuptools import setup

setup(
    name="PyMOL-advance",
    version="0.0",
    description="PyMOL-advance: high-level interfaces from structure data to manuscript-level expected_figures",
    author="Haoling Zhang",
    author_email="zhanghaoling@genomics.cn",
    url="https://github.com/BGI-SynBio/PyMOL-advance",
    packages=["PyMOL-advance.mola", "PyMOL-advance.tests", "PyMOL-advance.cases"],
    install_requires=["numpy"],
    license="GPL",
    classifiers=["License :: OSI Approved :: GNU General Public License (GPL)",
                 "Programming Language :: Python :: 3",
                 "Operating System :: OS Independent"],
    keywords="PyMOL, batch visualization",
)
