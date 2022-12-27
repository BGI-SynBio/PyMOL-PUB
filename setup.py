from setuptools import setup

setup(
    name="storeall",
    version="0.0",
    description="PyMOL-advance: high-level interfaces from structure data to manuscript-level figures",
    author="Haoling ZHANG",
    author_email="zhanghaoling@genomics.cn",
    url="https://github.com/BGI-SynBio/PyMOL-advance",
    packages=["PyMOL-advance.mola", "PyMOL-advance.tests"],
    install_requires=["numpy"],
    classifiers=["Programming Language :: Python :: 3",
                 "Operating System :: OS Independent"],
    keywords="PyMOL, batch visualization",
)
