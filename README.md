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
   (Make sure that the information in the main function is correct.)
    ```


### Extract
1. Check all parameters are defined correctly in
    ```
    global_var.py
    ```
2. Put all images want to extract message in
    ```
    /files/stego/
    ```
3. Then you can start extracting
    ```
    $ python extract_interface.py
    ```
4. You can also extract a single picture
    ```
    $ python extract.py
   (Make sure that the information in the main function is correct.)
    ```

Output
---

### Embed
According to the picture format and channel selection,

```
stego picture will be placed in one or all of the following folder:
files/stego/R/
files/stego/G/
files/stego/B/
files/stego/RGB/
```
```
the embedded message used will be placed in the following folder:
files/message_embed/R/
files/message_embed/G/
files/message_embed/B/
files/message_embed/RGB/
```
```
In addition, if enabled, a log file will be generated to record the process
log_embed.log
```


### Extract
According to the picture format and channel selection,
```
the extracted secret message will be placed in the following folder:
files/message_extract/R/
files/message_extract/G/
files/message_extract/B/
files/message_extract/RGB/
```
```
In addition, if enabled, a log file will be generated to record the process
log_extract
```


Comparison of results
---
In addition to the output of the above two parts, there will be a comparative result information in this part. Compare whether the embedded and extracted secret messages are the same.

Use the following,
```
$ python compare_message.py
```
In addition to the output record files, statistical results will also be displayed on the screen.
```
log_compare_message
```


The complete testing
---
1. Check all parameters are defined correctly in
    ```
    global_var.py
    ```
2. Put all images want to embed by STC in
    ```
    /files/cover/
    ```
3. Then you can start continuous testing
    ```
    $ python STC_interface.py
    ```


Reference
---
>* [Minimizing Embedding Impact in Steganography usingTrellis-Coded Quantization](http://dde.binghamton.edu/filler/pdf/Fill10spie-syndrome-trellis-codes.pdf)
>* [Syndrome-Trellis Codes Toolbox](http://dde.binghamton.edu/download/syndrome/)
>* [daniellerch/pySTC](https://github.com/daniellerch/pySTC)
