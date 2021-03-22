# STC-for-python

A simple way to use Syndrome Trellis Codes Steganography.
Support linux system and windows system.


Contents
---

>* [Where can use](#Environment)
>* [What is required](#Required)
>* [How to use](#Usage)
>* [What will get](#Output)
>* [Reference](#Reference)

Environment
---

>* Ubuntu or Win10
>* Python = 3.8 or newer


Required
---

If you're using anaconda:

    $ sh ./require_conda

If you're using pip:

    $ pip install opencv
    $ pip install Pillow
    $ pip install scipy
    $ pip install pycryptodome

If you're using other ways to manage your package:

    Please ensure that the above packages are installed correctly
    
If there are other missing packages, please complete the installation.

Usage
---

### Embed
1. Check all parameters are defined correctly in
    ```
    global_var.py
    ```
2. Put all images want to embed by STC in
    ```
    /files/cover/
    ```
3. Then you can start embedding
    ```
    $ python embed_interface.py
    ```
4. You can also embed a single picture
    ```
    $ python embed.py
    ```
   (Make sure that the information in the main function is correct.)


### Extract


### The complete testing


Output
---

### Embed


### Extract


### The complete testing


Reference
---
>* [Minimizing Embedding Impact in Steganography usingTrellis-Coded Quantization](http://dde.binghamton.edu/filler/pdf/Fill10spie-syndrome-trellis-codes.pdf)
>* [Syndrome-Trellis Codes Toolbox](http://dde.binghamton.edu/download/syndrome/)
>* [daniellerch/pySTC](https://github.com/daniellerch/pySTC)
