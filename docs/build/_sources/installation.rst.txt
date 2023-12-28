.. _installation:

============
Installation
============

.. note::

   If GlabTop2-py is NOT installed using the :ref:`Anaconda <installation_anaconda>` package manager, then a
   manual installation of the PCRaster dynamic modelling framework is required. This can be downloaded from:
   
   http://pcraster.geo.uu.nl/downloads/latest-release/

   Installation through Anaconda is therefore strongly recommended.


This page describes how you can install GlabTop2-py. There are three ways of installing GlabTop2-py:
   
   1. Install via :ref:`Anaconda <installation_anaconda>`::
   
       conda install -c WilcoTerink GlabTop2-py
   
   2. Install via :ref:`pip <installation_pip>`::
   
       pip install GlabTop2-py
   
   3. Downloading the source code from the `GlabTop2-py GitHub repository <https://github.com/WilcoTerink/GlabTop2-py>`_
   
Each of these installation methods is described in detail in the sections below. The recommended installation is the
**Anaconda** method.


.. _anaconda:

Anaconda
--------

About Anaconda
^^^^^^^^^^^^^^

Anaconda is the world's most popular Python/R data science platform. The open-source Anaconda distribution is the easiest way
to perform Python/R data science and machine learning on Linux, Windows, and Mac OS X. With over 11 million users worldwide, it
is the industry standard for developing, testing, and training on a single machine, enabling individual data scientists to:

    + Quickly download 1,500+ Python/R data science packages
    + Manage libraries, dependencies, and environments with Conda
    + Develop and train machine learning and deep learning models with scikit-learn, TensorFlow, and Theano
    + Analyze data with scalability and performance with Dask, NumPy, pandas, and Numba
    + Visualize results with Matplotlib, Bokeh, Datashader, and Holoviews
    
More information about the Anaconda distribution can be found `here <https://www.anaconda.com/distribution/>`_.

Download Anaconda
^^^^^^^^^^^^^^^^^

It is strongly recommended to use the Anaconda Python distribution to install and manage all your Python packages. The reason for
this is because Anaconda checks for dependencies, installs missing dependencies or updates old depencies if required. Use the link below to
download Anaconda Python:

    + `Python <https://repo.anaconda.com/archive/Anaconda3-2019.03-Windows-x86_64.exe>`_
    
.. _installation_anaconda:

Install GlabTop2-py using Anaconda
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you have PCRaster and Anaconda installed you can easily install GlabTop2-py via the command prompt::

    conda install -c WilcoTerink GlabTop2-py
    
The command above will always install the most recent GlabTop2-py release. Upgrading an already installed GlabTop2-py distribution
to the most recent release can be achieved by::

    conda update -c WilcoTerink GlabTop2-py

After you have installed GlabTop2-py, the package resides under::

    PATH-TO-YOUR-ANACONDA-INSTALLATION\Lib\site-packages\GlabTop2


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

Installation by this method, however, is not recommended because it does not check for the dependencies that are required to run GlabTop2-py, whereas the :ref:`Anaconda <anaconda>`
installation method does.









