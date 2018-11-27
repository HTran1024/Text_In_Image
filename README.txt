Name: Huy Tran

This program will decode a message hidden in an image by using the first 11 pixels to determine its length and use it to find the hidden message after the 11th pixel and embed
a message inside an image as well. Two main functions are used to accomplish this which is decode and embed; the rest is done through its sub functions. These two tasks can
only be done through commands.

The program will take 2 arguments after the file name to decode, 3 to embed. Use -d to decode or -e to embed.

To decode a message, the command syntax are as followed (This is done in Windows Command Prompt):
python Steganography.py -d nameOfImage.png

To embed a message, the command syntax are as followed (Also done in Windows Command Prompt):
python Steganography.py -e nameOfImage.png messageYouWantToPut

To put in multiple words, you will have to use quotes so something like "message you want to put." otherwise it will only take in the first word.
So if you want to put in multiple words, you will have to input the following:
python Steganography.py -e nameOfImage.png "Insert your message here"

Remember! The image must exist in the folder of the program for the program to use!