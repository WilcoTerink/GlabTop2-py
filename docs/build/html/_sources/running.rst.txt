.. _running:

===================
Running GlabTop2-py
===================

This section describes how you can run GlabTop2-py. How-to run the tool depends on the way you have installed
GlabTop2-py:

    1. Installation via :ref:`pip <installation_pip>`
    
    2. Installation using the download from the :ref:`GitHub repository <installation_github>`
    
See ONE of the sections below for how-to run GlabTop2-py depending on the chosen installation method.

Run via pip installation
------------------------

If you have installed GlabTop2-py via pip, then you can run GlabTop2-py from any location
on your PC; i.e. you do not need to refer to the physical address where the GlabTop2-py source code resides.
This is an advantage, because you do not need to copy all the source code files everytime you start
a new project.

The steps that are needed to run GlabTop2-py are:

  1. Create a folder somewhere on your hard drive, e.g. ``c:\my_folder``
  
  2. After you have installed GlabTop2-py via pip, the ``config.cfg`` configuration template can be found under:
  
     ``PATH-TO-YOUR-PYTHON-INSTALLATION\Lib\site-packages\GlabTop2\config.cfg``
     
     Copy ``config.cfg`` to the folder you created under step 1
     
     
  3. You can edit the ``config.cfg`` and set all the variables in this configuration file
  
  4. After you have edited and saved ``config.cfg``, you can run GlabTop2-py by::

         python -m GlabTop2.main -i c:\my_folder\config.cfg   


Run via the GitHub download installation
----------------------------------------

If you have downloaded the source code from the `GlabTop2-py GitHub repository <https://github.com/WilcoTerink/GlabTop2-py>`_, then you always
need to work from the folder where you have extracted GlabTop2-py's source code files; i.e. every time you start a new project you
have to copy the source code files to the new project folder.

The steps that are needed to run GlabTop2-py are:

  1. Create a folder somewhere on your hard drive, e.g. ``c:\my_folder``
  
  2. Copy all the GlabTop2-py source code files to the folder created under step 1
  
  3. You can edit the ``config.cfg`` and set all the variables in this configuration file
  
  4. Save the ``config.cfg`` file
  
  5. You can now run GlabTop2-py via:: 
  
         python c:\my_folder\main.py -i c:\my_folder\config.cfg
         


    

