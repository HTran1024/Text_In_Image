# Name:     Huy Tran
# Class:    CPSC 353 - 01
# Date:     May 10, 2018

from PIL import Image
import sys

# The MAIN FUNCTION for determining the hidden message.
def decode(img):
    # findLength will not only return a string of binary but also the width and an x & y coordinate for future use.
    strBinary, x, y, width = findLength(img)
    # removing the last bit in the string as its not needed.
    strBinary = strBinary[:-1]
    # take the string of binary and convert it into decimal.
    binaryToDecimal = int(strBinary, 2)
    binaryLength = int(binaryToDecimal)
    # the next line will return what the hidden message is in binary.
    strBinaryMessage = extractLength(img, x, y, width, binaryLength)
    # extractMessage function will translate the hidden message is by taking the message's binary string and its string length
    hiddenMessage = extractMessage(strBinaryMessage[0], binaryLength)
    return hiddenMessage

# findLength function returns length of string in binary as well as width and an x & y coordinate for future use.
def findLength(img):
    # the width and height variable will be needed to access the bottom right pixel.
    width, height = img.size
    # row and col variable will help by allowing extractLength function to start on the bottom right pixel.
    row = height - 1
    col = width - 1
    # lengthInBinary will store the message's binary length while x, y, and width2 will be needed next time extractLength will be used.
    lengthInBinary, x, y, width2 = extractLength(img, col, row, width, 11)
    return lengthInBinary, x, y, width2

# extractLength function returns a string of binary which when converted tells us the length of the hidden message
def extractLength(img, col, row, width, end):
    binary = ''
    # the for loop takes the rgb values of the 11 pixels and stores the least significant bit into a string which will be returned by the end of the function.
    for i in range(end):
        r, g, b = img.getpixel((col, row))
        binary += str(bin(r))[-1]
        binary += str(bin(g))[-1]
        binary += str(bin(b))[-1]
        #if the for loop needs to wrap around the image, this condition will take care of it by changing the its coordinate to the next row up starting on the right.
        if col is 0:
            col = width
            row = row - 1
        col = col - 1
    return binary, col, row, width

#################################################################################################################
# extractMessage function will translate the message by taking first taking the hidden message's binary string, #
# converting each set of 8 bits into a decimal, then converting the decimal into an ascii character. Once the   #
# ascii character is determined, it will be stored into a string and this cycle will continue until the         #
# function reaches the end of the binary string and translates the last set of binary into an ascii character   #
# to be stored. The function will return the resulting message.                                                 #
#################################################################################################################

def extractMessage(str, strlen):
    # msg will be used to store the hidden message.
    msg = ''
    # binaryStr will be used to store binaries.
    binaryStr = ''
    for i in range(strlen + 1):
        # once a set of 8 bits is stored, convert that set into an ascii character and store it into msg
        if (i % 8) == 0 and i != 0:
            binaryToDecimal = int(binaryStr, 2)
            asciiNum = int(binaryToDecimal)
            asciiChar = chr(asciiNum)
            msg += asciiChar
            # reset binaryStr for the next set of binaries
            binaryStr = ''
        binaryStr += str[i]
    return msg

# The MAIN FUNCTION for embedding your message and its length
def embed(img, str, name):
    # msgLenInBin will use getLength function to return the length of the message's in binary (if you ignore the 0 at the end).
    msgLenInBin = getLength(str)
    # similarly in decode function; x, y, and width will be used for a future function as its coordinates are needed. Otherwise it will output the resulting image.
    x, y, width, newImg = embedLength(img, msgLenInBin)
    # The next function will embed your message and output the resulting image and then it will be saved.
    newImg = embedMessage(newImg, str, x, y, width)
    newImg.save(name, "PNG")

def getLength(str):
    # the next two lines will get the message's length and also its binary form char length but it is still a decimal.
    strLen = len(str)
    lenInBin = strLen * 8
    # the next two lines will get its binary form char length into a binary and slice the first two chars in the string as its not needed.
    binary = bin(lenInBin)
    binary = binary[2:]
    # the next line will concatenate as many 0's as needed to the front for comparison purposes in the future.
    binary = concatenateZero(binary, 32)
    # the 0 added at the end will be needed so the program won't crash when it compares the last bit.
    binary = binary + '0'
    return binary

# embedLength function will embed the length of the binary message in the first 11 pixels of the image.
def embedLength(img, binStr):
    # similar procedure as the findLength function except with one additional variable: index.
    width, height = img.size
    row = height - 1
    col = width - 1
    # index will be used to access binStr for comparison purposes.
    index = 0
    for i in range(11):
        r, g, b = img.getpixel((col, row))

        ################################################################################################################
        # The last bit of the rgb values will be compared to where binStr is to determine if the last bit of the rgb   #
        # values need to be changed. This will change the values of rgb and be used in the putpixel function near the  #
        # end.                                                                                                         #
        ################################################################################################################

        if (bin(r))[-1] != binStr[index]:
            r = bin(r)
            # the first two char are '0b' which is not needed and the last bit is removed so it can be replaced.
            r = r[2:-1]
            r = r + binStr[index]
            r = int(r, 2)
        index = index + 1
        if (bin(g))[-1] != binStr[index]:
            g = bin(g)
            g = g[2:-1]
            g = g + binStr[index]
            g = int(g, 2)
        index = index + 1
        if (bin(b))[-1] != binStr[index]:
            b = bin(b)
            b = b[2:-1]
            b = b + binStr[index]
            b = int(b, 2)
        index = index + 1
        img.putpixel((col, row), (r, g, b))
        if col is 0:
            col = width
            row = row - 1
        col = col - 1
    return col, row, width, img

########################################################################################################################
# embedMessage function will embed your message within the image in binary after the 11th pixel by doing the following;#
# First the function will get its entire message in binary using a function called getMsgBinStr and store it in        #
# msgInBin. To help determine whether function is done with its job, it will need two variables: index and msgBinLen.  #
# index will help determine where in msgInBin it should be at for comparison and msgBinLen stores the length of        #
# msgInBin. These two variables will be used in a while loop and in an if statement where the function will break out  #
# of the while loop if needed. embedMessage will function similarly as embedLength where it will compare msgInBin last #
# bits of its rgb values and edit them if needed. At the end of each of these if statements is another if statement to #
# determine whether embedMessage is done with its job and needs to break out. The function will return the resulting   #
# image.                                                                                                               #
########################################################################################################################

def embedMessage(img, msg, col, row, width):
    # msgInBin will get its entire message in binary form.
    msgInBin = getMsgBinStr(msg)
    # index will be used to access msgInBin for comparison and msgBinLen will be used to determine if index is at the end of msgInBin
    index = 0
    msgBinLen = len(msgInBin)
    while (index < msgBinLen):
        r, g, b = img.getpixel((col, row))
        if (bin(r))[-1] != msgInBin[index]:
            r = bin(r)
            r = r[2:-1]
            r = r + msgInBin[index]
            r = int(r, 2)
        index = index + 1
        # at the each of these if statements is this if statement. It is needed to determine if index reached the end of msgInBin and the while loop needs to be broken out.
        if (index == msgBinLen):
            img.putpixel((col, row), (r, g, b))
            break
        if (bin(g))[-1] != msgInBin[index]:
            g = bin(g)
            g = g[2:-1]
            g = g + msgInBin[index]
            g = int(g, 2)
        index = index + 1
        # so is this if statement.
        if (index == msgBinLen):
            img.putpixel((col, row), (r, g, b))
            break
        if (bin(b))[-1] != msgInBin[index]:
            b = bin(b)
            b = b[2:-1]
            b = b + msgInBin[index]
            b = int(b, 2)
        index = index + 1
        # this too.
        if (index == msgBinLen):
            img.putpixel((col, row), (r, g, b))
            break
        img.putpixel((col, row), (r, g, b))
        if col is 0:
            col = width
            row = row - 1
        col = col - 1
    return img

# concatenateZero function will concatenate as many 0's needed to the front.
def concatenateZero(binStr, numOfBits):
    binLen = len(binStr)
    end = numOfBits - binLen
    for i in range(end):
        binStr = '0' + binStr
    return binStr

# getMsgBinStr function will help embedMessage function by getting the message's binary string.
def getMsgBinStr(msg):
    end = len(msg)
    binStr = ''
    for i in range(end):
        asciiNum = ord(msg[i])
        charBin = bin(asciiNum)
        charBin = charBin[2:]
        charBin = concatenateZero(charBin, 8)
        binStr += charBin
    return binStr

def checkName(str):
    end = len(str)
    for i in range(end):
        if str[i] == '.':
            remove = end - i
            str[:-remove]
            str = str + ".png"
    return str

def main():
    if (sys.argv[1] == "-d" and sys.argv[2]):
        img = Image.open(sys.argv[2])
        hiddenMsg = decode(img)
        print("Message:", hiddenMsg)
    elif (sys.argv[1] == "-e" and sys.argv[2] and sys.argv[3] and sys.argv[4]):
        img = Image.open(sys.argv[2])
        msgToEmbed = sys.argv[3]
        newImgName = sys.argv[4]
        newImgName = checkName(newImgName)
        embed(img, msgToEmbed, newImgName)
        print("Message embedding successful!")
    else:
        print("Invalid command!")

if __name__ == "__main__":
    main()