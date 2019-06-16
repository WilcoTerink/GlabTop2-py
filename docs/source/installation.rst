.. _installation:

============
Installation
============

.. note::

   GlabTop2-py requires the PCRaster dynamic modelling framework, which needs to be downloaded from:
   
   http://pcraster.geo.uu.nl/downloads/latest-release/
   
   GlabTop2-py was developed using PCRaster version 4.2.1 and Python 3.6 (both 64 bits).


This page describes how you can install GlabTop2-py. There are two ways of installing GlabTop2-py:
   
   1. Install via :ref:`pip <installation_pip>`::
   
       pip install GlabTop2-py
   
   2. Downloading the source code from the `GlabTop2-py GitHub repository <https://github.com/WilcoTerink/GlabTop2-py>`_
   
Each of these installation methods is described in detail in the sections below. The recommended installation is the
**pip** method.


.. _pip:

pip
---

About pip
^^^^^^^^^

pip is the package installer for Python. You can use pip to install packages from the `Python Package Index <https://pypi.org/>`_ and other indexes.
In contrast to Anaconda, which comes with a complete Python installation, pip itself does not contain a Python installation. Therefore,
it is required to have a Python distribution already installed before you can use pip. See the link below for more information on how-to install pip:

    https://pip.pypa.io/en/stable/installing/

.. _installation_pip:

Install GlabTop2-py using pip
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you have PCRaster and pip installed you can easily install the GlabTop2-py via the command prompt::

    pip install GlabTop2-py
    
The command above will always install the most recent GlabTop2-py release. Upgrading an already installed GlabTop2-py distribution
to the most recent release can be achieved by::

    pip install GlabTop2-py --upgrade
    
After you have installed GlabTop2-py the package resides under::

    PATH-TO-PYTHON-INSTALLATION\Lib\site-packages\GlabTop2


.. _installation_github:

Download from GitHub repository
-------------------------------

Alternatively, you can download GlabTop2-py from my GitHub repository: 

    https://github.com/WilcoTerink/GlabTop2-py

You can download the release you want, and extract the contents to a folder on your hard drive.
GlabTop2-py can then be run from inside this folder.

Installation by this method, however, is not recommended because it does not check for the dependencies that are required to run GlabTop2-py, whereas the :ref:`pip <pip>`
installation method does.









