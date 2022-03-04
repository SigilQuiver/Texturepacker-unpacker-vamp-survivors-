########## made by SigilQuiver, use as you please ##########
# please note:
# this was made for the game Vampire Survivors, so it may not work with other games
# this script also only works with .json files generated with texturepacker and no other formats

######################
# todos:
# make an importer

from os import listdir, getcwd, makedirs
import os
import json
import pygame
import re
import validPath
from pygame import image as imagee

cwd = getcwd()  # cwd = Current Working Directory
jsonContent = {}
jsonImages = {}
jsonImageSizes = {}

# find the json files
for item in listdir(cwd):
    if item[-5:] == ".json" and item[-5:] + ".png":

        # import the json file as a dictionary, put into another dictionary
        with open(cwd + "/" + item, "r") as f:
            data = json.load(f)
        try:
            jsonContent[str(item)] = data["textures"][0]["frames"]
            jsonImages[str(item)] = data["textures"][0]["image"]
            jsonImageSizes[str(item)] = data["textures"][0]["size"]
        except:
            print("Couldn't properly parse", str(item), "!(if there isn't a matching image file, ignore this error)")

canPack = True
if jsonContent == {}:
    canPack = False
    print("No json files found :(\n(place me into a folder with images and json files packed by texturepacker)")


# counts number of digits at the end of a string
def countDigits(string):
    digits1 = 1
    digits2 = None
    while string[-digits1:digits2].isdigit():
        digits1 += 1
        if not digits2:
            digits2 = -1
        else:
            digits2 -= 1
    return digits1 - 1


def setDigits(string, digits, num, addon=True):
    numstring = str(num)
    if addon:
        while len(numstring) < digits:
            numstring = "0" + numstring
    return string[:-digits] + numstring

def importFiles(exportFolder=cwd+"\\export_sheets\\",importFolder=cwd+"\\import\\",align="center"):

    # stop pygame window from popping up >:(
    os.putenv('SDL_VIDEODRIVER', 'fbcon')
    os.environ["SDL_VIDEODRIVER"] = "dummy"

    pygame.init()
    screen = pygame.display.set_mode()

    makedirs(exportFolder, 0o777, True)

    for i, (file, frames) in enumerate(jsonContent.items()):

        frameDict = {}
        for frame in frames:
            frameDict[frame["filename"]] = frame

        bigImage = pygame.Surface((jsonImageSizes[file]["w"],jsonImageSizes[file]["h"]),pygame.SRCALPHA)
        searchPath = importFolder+file[:-5]+"\\"
        for img in listdir(searchPath[:-1]):
            if img[-4:] == ".png" and (img in frameDict or img[:-15]+".png" in frameDict):
                default = False
                if len(img)<15:
                    default = True
                else:
                    if img[-15:-4] != "spritesheet":
                        default = True

                if default:
                    imgDims = frameDict[img]["frame"]
                    frameRect = pygame.Rect(imgDims["x"], imgDims["y"], imgDims["w"], imgDims["h"])

                    toBlit = pygame.image.load(searchPath+img)
                    bigImage.blit(toBlit,frameRect)

                    
                else:
                    baseName = img[:-15]
                    digits = countDigits(baseName)
                    if digits > 0:
                        # look forwards for incrementing name

                        ahead = []
                        
                        num = int(baseName[-digits:]) + 1
                        nextName = setDigits(baseName, digits, num)
                        if not(nextName + ".png" in frameDict.keys()):
                            nextName = setDigits(baseName, digits, num, False)
                        while nextName + ".png" in frameDict.keys():
                            ahead.append(nextName)
                            num += 1
                            nextName = setDigits(baseName, digits, num)
                            if not(nextName + ".png" in frameDict.keys()):
                                nextName = setDigits(baseName, digits, num, False)

                        behind = []
                        
                        # look backwards for incrementing name
                        num = int(baseName[-digits:]) - 1
                        previousName = setDigits(baseName, digits, num)
                        if not(previousName + ".png" in frameDict.keys()):
                            previousName = setDigits(baseName, digits, num, False)
                        while previousName + ".png" in frameDict.keys():
                            behind.append(previousName)
                            num -= 1
                            previousName = setDigits(baseName, digits, num)
                            if not(previousName + ".png" in frameDict.keys()):
                                previousName = setDigits(baseName, digits, num, False)

                        behind.reverse()
                        spriteSheetNames = behind+[baseName]+ahead

                        if len(spriteSheetNames) <= 1:
                            print("Error: not enough sprites in spritesheet",img)
                        else:
                            
                            # get the largest sprite dimensions in the grouped frames
                            bigw = 0
                            bigh = 0

                            for name1 in spriteSheetNames:
                                frameDims = frameDict[name1 + ".png"]["sourceSize"]

                                if frameDims["w"] > bigw:
                                    bigw = frameDims["w"]

                                if frameDims["h"] > bigh:
                                    bigh = frameDims["h"]

                            # create transparent image with width to fit all the frames
                            gap = 0
                            width = (bigw + gap) * len(spriteSheetNames)
                            #spritesheetImage = pygame.Surface((width, bigh), pygame.SRCALPHA)
                            spritesheetRect = pygame.Rect(0,0,width,bigh)
                            bigRect = pygame.Rect(0, 0, bigw + gap, bigh)
                            
                            image = pygame.image.load(searchPath+img)
                            targetRect = image.get_rect()
                            if targetRect != spritesheetRect:
                                print(img)
                            
                            for name1 in spriteSheetNames:
                                imgDims = frameDict[name1 + ".png"]["frame"]

                                # get image for a single frame
                                frameRect = pygame.Rect(imgDims["x"], imgDims["y"], imgDims["w"], imgDims["h"])
                                

                                # center smaller images onto the bigger spritesheet size
                                smallRect = pygame.Rect(0,0,imgDims["w"], imgDims["h"])

                                if align == "center":
                                    smallRect.center = bigRect.center
                                elif align == "bottom":
                                    smallRect.bottom = bigRect.bottom
                                    smallRect.centerx = bigRect.centerx
                                else:
                                    smallRect.center = bigRect.center
                                    

                                smallImage = image.subsurface(smallRect)
                                smallImage.set_colorkey((255,2,0))
                                bigImage.blit(smallImage,frameRect)
                                
                                #spritesheetImage.blit(smallImage, smallRect)
                                

                                # move the spritesheet position for the next frame
                                bigRect.x += bigw + gap

            
            pygame.image.save(bigImage,exportFolder+file[:-5]+".png")
                
        

    
    
def exportFiles(exportFolder=cwd + "\\export_vanilla\\",spriteSheet=True, align="center"):  # align can be either bottom or center
    # creates export folder + folder for all the json files if not present
    for key in jsonContent:
        makedirs(exportFolder + key[:-5], 0o777, True)

    # stop pygame window from popping up >:(
    os.putenv('SDL_VIDEODRIVER', 'fbcon')
    os.environ["SDL_VIDEODRIVER"] = "dummy"

    pygame.init()
    screen = pygame.display.set_mode()

    nameSkip = []  # keeps track of already covered sprites if spritesheets are generated

    # loop through the dict of dicts of frames (not gonna word that anyway different)
    for i, (file, frames) in enumerate(jsonContent.items()):
        imagePath = cwd + "\\" + jsonImages[file]
        savePath = exportFolder + file[:-5] + "\\"

        # gets the image for that json file
        image = pygame.image.load(imagePath).convert_alpha()

        frameDict = {}
        for frame in frames:
            frameDict[frame["filename"]] = frame

        # loop through individual frames
        for j, (name, frame) in enumerate(frameDict.items()):

            default = False
            if spriteSheet and name not in nameSkip:

                baseName = name[:-4]
                spriteSheetNames = []

                # if there are numbers in the name
                digits = countDigits(baseName)
                if digits > 0:
                    # look forwards for incrementing name

                    ahead = []
                    
                    num = int(baseName[-digits:]) + 1
                    nextName = setDigits(baseName, digits, num)
                    
                    if nextName + ".png" not in frameDict.keys():
                        nextName = setDigits(baseName, digits, num, False)
                    
                    while nextName + ".png" in frameDict.keys():
                        ahead.append(nextName)
                        num += 1
                        nextName = setDigits(baseName, digits, num)
                        if nextName + ".png" not in frameDict.keys():
                            nextName = setDigits(baseName, digits, num, False)

                    behind = []
                    
                    # look backwards for incrementing name
                    num = int(baseName[-digits:]) - 1
                    previousName = setDigits(baseName, digits, num)
                    if previousName + ".png" not in frameDict.keys():
                        previousName = setDigits(baseName, digits, num, False)
                    while previousName + ".png" in frameDict.keys():
                        behind.append(previousName)
                        num -= 1
                        previousName = setDigits(baseName, digits, num)
                        if previousName + ".png" not in frameDict.keys():
                            previousName = setDigits(baseName, digits, num, False)

                    behind.reverse()
                    spriteSheetNames = behind+[baseName]+ahead

                    # if incremented names were found before/after
                    if len(spriteSheetNames) > 1:
                        # print(spriteSheetNames)

                        for used in spriteSheetNames:
                            nameSkip.append(used + ".png")

                        """
                        for frameName in list(spriteSheetNames):
                            frameDims = frameDict[frameName + ".png"]["sourceSize"]
                            if frameDims["w"] <= 3 and frameDims["h"] <= 3:
                                spriteSheetNames.remove(frameName)
                        """

                        # get the largest sprite dimensions in the grouped frames
                        bigw = 0
                        bigh = 0

                        for name1 in spriteSheetNames:
                            frameDims = frameDict[name1 + ".png"]["sourceSize"]

                            if frameDims["w"] > bigw:
                                bigw = frameDims["w"]

                            if frameDims["h"] > bigh:
                                bigh = frameDims["h"]

                        # create transparent image with width to fit all the frames
                        gap = 0
                        width = (bigw + gap) * len(spriteSheetNames)
                        spritesheetImage = pygame.Surface((width, bigh), pygame.SRCALPHA)
                        bigRect = pygame.Rect(0, 0, bigw + gap, bigh)
                        for name1 in spriteSheetNames:
                            imgDims = frameDict[name1 + ".png"]["frame"]

                            # get image for a single frame
                            frameRect = pygame.Rect(imgDims["x"], imgDims["y"], imgDims["w"], imgDims["h"])
                            smallImage = image.subsurface(frameRect)

                            # center smaller images onto the bigger spritesheet size
                            smallRect = smallImage.get_rect()

                            if align == "center":
                                smallRect.center = bigRect.center
                            elif align == "bottom":
                                smallRect.bottom = bigRect.bottom
                                smallRect.centerx = bigRect.centerx

                            spritesheetImage.fill((255,3,0,255),bigRect)
                            spritesheetImage.fill((0,0,0,0),smallRect)
                            spritesheetImage.blit(smallImage, smallRect)

                            # put box around the smaller images to show their border
                            

                            # move the spritesheet position for the next frame
                            bigRect.x += bigw + gap

                        # save generated spritesheet to path, using the suffix of spritesheet instead of a number
                        string = savePath + baseName+ "spritesheet.png"
                        pygame.image.save(spritesheetImage, string)

                    else:
                        default = True
                else:
                    default = True
            elif name not in nameSkip:
                default = True

            # if not using spritesheet mode or image is not part of a set
            if default:
                # gets smaller image using the "frame" attribute from each frame and applying it to the bigger image
                frameDims = frame["frame"]
                frameRect = pygame.Rect(frameDims["x"], frameDims["y"], frameDims["w"], frameDims["h"])
                smallImage = image.subsurface(frameRect)
                pygame.image.save(smallImage, savePath + name)

    pygame.quit()

def quickCheckInput(text,optionList):
    result = None
    while result not in optionList:
        if result is not None:
            print("Option not provided in list given (look in the brackets next to the prompt)")
        result = input(text).lower()
    return result

def enterDirectoryInput(text,defaultDir):
    valid = False
    while not valid:
        result = input(text)
        if result == "":
            result = defaultDir

        if validPath.is_pathname_valid(result):
            valid = True
        else:
            print("invalid path/folder name")

        
        if len(result) < 2 or result[1] != ":":
            if result[0] != "\\":
                result = "\\"+result
            if result[-1] != "\\":
                result = result + "\\"
            result = cwd + result
        print("going to directory:",result,"\n")
    return result

if canPack:
    print("Found json files!")
    print("----Texturepacker unpacker/repacker, made for Vampire Survivors----")
    result = quickCheckInput("Will you unpack or repack images?\n(unpack,repack):",["unpack","repack"])

    if result == "unpack":
        text = "Enter directory to export images to, leave blank for default directory (/export_vanilla) ,will create path if not present\n:"
        exportDirectory = enterDirectoryInput(text,cwd + "\\export_vanilla\\")
        spriteSheetString = quickCheckInput("For incremented number images do you want spritesheets?(i.e. spritesheets for animations)\n(y,n)",["yes","no","y","n"])
        spriteSheet = {"yes":True,"y":True,"n":False,"no":False}[spriteSheetString]
        if spriteSheet:
            align = quickCheckInput("Not all images to be put into spritesheets are the same dimensions, align/anchor center or bottom?\n(center,bottom):",["center","bottom"])
            print("\nDoing the stuff...")
            exportFiles(exportDirectory,True,align)
        else:
            print("\nDoing the stuff...")
            exportFiles(exportDirectory,False)
        print("\nComplete!")
    elif result == "repack":
        text = "Enter directory to export images to, leave blank to save packed images to current directory (be careful since doing this will overwrite existing images)\n:"
        exportDirectory = enterDirectoryInput(text,cwd)

        text = "Enter directory to import images from, leave blank for default directory (/import), will create path if not present,\
                \n if textures don't have the correct name, they will just be ommitted from the spritesheet packing (e.g.: after an update)\n:"
        importDirectory = enterDirectoryInput(text,cwd + "\\import\\")

        align = quickCheckInput("If you enabled spritesheets, did you align bottom or center (If you didn't you can leave this blank)\n(bottom,center, ):",["","bottom","center"])

        print("\nDoing the stuff...")
        importFiles(exportDirectory,importDirectory,align)
        print("\nComplete!")
        
                
input("\nPress enter to quit")
        
    
    
    
    
