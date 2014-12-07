#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
dashlength = 0.3
dotlength = 0.1
flashgap = 0.05
pin=13
chargap = 0.2
wordgap = 0.5
MORSE = {"A":".-","B":"-...","C":"-.-.","D":"-..","E":".","F":"..-.",\
		"G":"--.","H":"....","I":"..","J":".---","K":"-.-","L":".-..",\
		"M":"--","N":".","O":"---","P":".--.","Q":"--.-","R":".-.",\
		"S":"...","T":"-","U":"..-","V":"...-","W":".--","X":"-..-",\
		"Y":"-.--","Z":"--..","1":".----","2":"..---","3":"...--",\
		"5":".....","6":"-....","7":"--...","8":"---..","9":"----.",\
		"0":"-----"," ":",",}
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin,GPIO.OUT)
def engToMorse(string):
	end = ""
	for char in string:
		if char in MORSE:
			end += MORSE[char]+" "
		else:
			print(char, "cannot be translated into morse code.")
	return end

def codePlayer(morsein):
	for tone in morsein:
		if tone == "-":
			GPIO.output(pin,GPIO.HIGH)
			time.sleep(dashlength)
			GPIO.output(pin,GPIO.LOW)
			time.sleep(flashgap)
		elif tone == ".":
			GPIO.output(pin,GPIO.HIGH)
			time.sleep(dotlength)
			GPIO.output(pin,GPIO.LOW)
			time.sleep(flashgap)
		elif tone == " ":
			time.sleep(chargap)
		elif tone == ",":
			time.sleep(wordgap)
		else:
			print("unrecodnised character",tone)	
	
print("Input the sentence to translate:")
sentence = input()
x = engToMorse(sentence.upper())
print(x)
codePlayer(x)
