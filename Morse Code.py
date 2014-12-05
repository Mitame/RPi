import RPi.GPIO as GPIO
import time
dashlength = 0.5
dotlength = 0.2
flashgap = 0.1
pin=13
chargap = 0.5
wordgap = 1
MORSE = {"A":".-","B":"-...","C":"-.-.","D":"-..","E":".","F":"..-.",\
		"G":"--.","H":"....","I":"..","J":".---","K":"-.-","L":".-..",\
		"M":"--","N":".","O":"---","P":".--.","Q":"--.-","R":".-.",\
		"S":"...","T":"-","U":"..-","V":"...-","W":".--","X":"-..-",\
		"Y":"-.--","Z":"--..","1":".----","2":"..---","3":"...--",\
		"5":".....","6":"-....","7":"--...","8":"---..","9":"----.",\
		"0":"-----"," ":",",}

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
			GPIO.setup(13,GPIO.output)
	
print("Input the sentence to translate:")
sentance = input()
