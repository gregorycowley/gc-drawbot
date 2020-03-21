import sys
import argparse
import logging
import math
from gpiozero import LED
from gpiozero import Servo
from gpiozero import OutputDevice
from time import sleep
from threading import Thread
from datetime import datetime
import yaml

# from gpiozero.pins.pigpio import PiGPIOFactory
# factory = PiGPIOFactory(host='localhost')

with open("config.yml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


# PIN Constants ::
# pin_left_dir = LED(20, pin_factory=factory)
# pin_left_step = OutputDevice(21, pin_factory=factory)
# pin_right_dir = LED(6, pin_factory=factory)
# pin_right_step = OutputDevice(13, pin_factory=factory)
# pin_pen_servo = Servo(18, pin_factory=factory)


class SetUp:
	'''
	Class Variables
	
	Custom for a single session
	'''

	pin_left_dir = LED(20)
	pin_left_step = OutputDevice(21)
	pin_right_dir = LED(6)
	pin_right_step = OutputDevice(13)
	pin_pen_servo = Servo(18)

	# GPIO Pins for a Raspeberry Pi:
	dir_pins = [
		pin_left_dir,
		pin_right_dir
	]

	step_pins = [
		pin_left_step,
		pin_right_step
	]

	string_lengths = {
		"left": 0,
		"right": 0
	}

	home_position = {
		"x": config["startPos"]["x"],
		"y": config["startPos"]["y"]
	}

	motor_distance = config["_D"]

	# Hardware Setup
	def updateStringLengths(self):
		config.startStringLengths = [
			math.sqrt( (config.startPos.x * config.startPos.x) + (config.startPos.y * config.startPos.y) ),
			math.sqrt( ( (config._D - config.startPos.x) * (config._D - config.startPos.x) ) + (config.startPos.y * config.startPos.y) )
		]
		config.stringLengths = [config.startStringLengths[0],config.startStringLengths[1]]
		config.startSteps = [round(config.stringLengths[0] * config.stepsPerMM[0]), round(config.stringLengths[1] * config.stepsPerMM[1])]
		config.currentSteps = [config.startSteps[0], config.startSteps[1]]
		return config.startStringLengths

	def setStartPos(self,data):
		config.static.startPos.x = config.startPos.x = float(data.x) 
		config.static.startPos.y = config.startPos.y = float(data.y)
		# Writes to config file --> cfg.save()
		updateStringLengths()

	def setD(self,data):
		config.static.d = config._D = float(data) # set value and store in config
		# Writes to config file --> cfg.save() # save to local config.json file
		updateStringLengths()


class Units:
	def __init__(self):
		self.setup = SetUp()
		self.stepsPerMM = 10;

	def convertLengthToRotation(self, length):
		return length * self.stepsPerMM
			
	def convertRotationToLength(self, steps):
		return steps / self.stepsPerMM


class Timer:
	'''
	Off Thread Non-Blocking Timer
	'''
	def __init__(self, duration, callback):
		self.duration = duration
		self.callback = callback
	
	def start(self):
		try:
			self.alt_thread = Thread( target=self.stop )
			self.alt_thread.start()
		except TypeError as e:
			print(e)
		
	def stop(self):
		sleep(self.duration)
		self.cleanup()
		
	def cleanup(self):
		self.callback()	


# Stepper Motor Controls

class Motor:
	'''
	Stepper Motor Control
	'''
	def __init__( self, motor_id ):	
		print(">> Initing Motor %s" % motor_id)
		self.motor_id = motor_id
		self.setup = SetUp()
		self.direction = 0
		self.fullstep = 0
		self.pause_time = .001
		self.duration = 0
		self.current_steps = 0
		self.dir_io = self.setup.dir_pins[self.motor_id]
		self.step_io = self.setup.step_pins[self.motor_id]
		
	def get_current_steps (self):
		return self.current_steps

	def rotate(self, direction, steps, pause):
		if not pause: 
			self.pause_time = .001
		else:
			self.pause_time = pause
		
		self.duration = datetime.now()  
		print('>> Rotaing %s steps in %s direction' % (steps, direction))
		self.direction = direction
		self.steps = steps
		for i in range(1, steps):
			self.increment(i)

		print ("Total Time :: " + str( datetime.now() - self.duration ) )
		print ("Lost Steps : " + str( self.fullstep ))

	def increment( self, cnt ):
		# print("incrementing : " + str(cnt), end="\r")
		self.makeStep(self.direction)

	def makeStep( self, dir ):
		if dir:
			self.dir_io.on() 
			self.current_steps -= 1
		else:
			self.dir_io.off()
			self.current_steps += 1

		self.step_io.on()
		self.fullstep += 1
		if True:
			sleep(float( self.pause_time ))
			self.resetStep()
		else:
			self.timer = Timer(self.pause_time, self.resetStep)
			self.timer.start()
	
	def resetStep(self):
		self.fullstep -= 1
		self.step_io.off()

	def cleanup(self):
		self.callback( self )


class Pen:
	'''
	Pen Servo Control
	'''

	def __init__(self):
		self.setup = SetUp()

	def pen(self, direction):
		if(direction):
			self.up()
		else:
			self.down()

	def up(self):
		self.setup.pin_pen_servo.max()

	def down(self):
		self.setup.pin_pen_servo.min()


class Strings:
	def __init__(self, id):
		self.id = id
		self.setup = SetUp()
		self.motor_distance = config["_D"]
		self.current_length = 0

	def get_current_length(self):
		return self.current_length

	def string_length(self, x, y):
		if self.id == 1:
			# left side, origin offset is 0:
			return self.calcString( x, y, 0 )	
		elif self.id == 2:
			# right side, origin offset is motor_distance:
			return self.calcString( x, y, self.motor_distance )	
		else:
			print( 'String ID is undefined' ) 
		
	def calcString(self, x1, y1, offset):
		x2 = abs( offset - x1 )
		s1 = math.sqrt(( x2 * x2 ) + ( y1 * y1 ))
		return s1

# Drawbot 

class Drawing:
	def __init__(self):
		self.motor_left = Motor(0)
		self.motor_right = Motor(1)
		self.string_left = Strings(0)
		self.string_right = Strings(1)
		
	def move_to(self, dstX, dstY):
		'''
		Move gondola with both motors
		Timing is important. Each motor needs to complete movement 
		at the same time. Motor operation time is controlled indepenent
		of distance.

		greatest change will set movement duration for both strings

		Calc new length
	
		Duration
		
		Current string length
		New string length

		Factor in current length
		Amount of change over time

		pauses = totaltime/steps
		'''

		self.motor_left.rotate( 1, 1000, .001 ) 
		self.motor_right.rotate( 1, 1000, .001 ) 


# Combined Control Functions

class MotorsSynced:
	def __init__(self):
		self.motor_left = Motor(0)
		self.motor_right = Motor(1)
		self.steps = 0
		self.a1 = 0
		self.a2 = 0
		self.stepped = 0
		self.paused = False
		self.baseDelay = .002
		self.callback = None

	def move_it(self, dir):
		for inc in range (1,1000):
			self.motor_left.makeStep(dir)
			self.motor_right.makeStep(dir)
			self.motor_right.makeStep(dir)

	# TODO: This could move to a python script for faster execution (faster than bc.baseDelay=2 miliseconds)
	def rotateBoth ( self, s1, s2, d1, d2, callback ):
		# // console.log('bc.rotateBoth',s1,s2,d1,d2)
		self.s1 = s1
		self.s2 = s2
		self.d1 = d1
		self.d2 = d2
		self.steps = round(max(s1,s2))
		self.a1 = 0
		self.a2 = 0
		self.stepped = 0
		self.paused = False
		self.baseDelay = .0002
		self.callback = None
		self.doStep()

	def timerFunction(self):
		if( self.stepped < self.steps) :
			self.stepped += 1

			# Motor one ::
			self.a1 += self.s1
			if(self.a1 >= self.steps):
				self.a1 -= self.steps
				self.motor_left.makeStep(self.d1)
				# print("**** Moving LEFT steps %s a1 %s a2 %s" % (self.steps, self.a1, self.a2))

			# Motor two:
			self.a2 += self.s2
			if(self.a2 >= self.steps):
				self.a2 -= self.steps
				self.motor_right.makeStep(self.d2)
				# print("++++ Moving RIGHT steps %s a1 %s a2 %s" % (self.steps, self.a1, self.a2))

			self.doStep()

		else:
			if self.callback != None: 
				self.callback()

	def doStep( self ):
		if not self.paused:
			t = Timer(self.baseDelay, self.timerFunction)
			t.start() 
		else:
			print('paused!')
			self.paused = False

		


# Gather our code in a main() function
def main(args, loglevel):

	logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
	
	# TODO Replace this with your actual code.
	print ("Hello there.")
	logging.info("You passed an argument.")
	logging.debug("Your Argument: %s" % args.argument)

	wait()

	# run = RotateBoth( 1000, 1000, 1, 1, "finished" )
	# run.doStep(1000)
	# message = input('==> ')

def wait ():
	message = input('-> ')
	while message != 'q':
		print ('Running :: ' + message )
		message = message.split(' ')
		# drawtools = Drawing()
		# drawtools.move_to( 0, 0 )
		move = MotorsSynced()
		move.rotateBoth(1000,5000,0,0,None)
		# move.rotateBoth.doStep()
		message = 'q'
		print ("")
		wait()
		



# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
	parser = argparse.ArgumentParser( 
						description = "Does a thing to some stuff.",
						epilog = "As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
						fromfile_prefix_chars = '@' )
	# TODO Specify your real parameters here.
	parser.add_argument(
						"argument",
						help = "pass ARG to the program",
						metavar = "ARG")
	parser.add_argument(
						"-v",
						"--verbose",
						help="increase output verbosity",
						action="store_true")
	args = parser.parse_args()
	
	# Setup logging
	if args.verbose:
		loglevel = logging.DEBUG
	else:
		loglevel = logging.INFO
	
	main(args, loglevel)
