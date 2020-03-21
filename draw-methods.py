
'''
	DRAWING METHODS
'''

class Drawing:

	def __init__(self, startx, starty, _D):
		self.startx = startx
		self.starty = starty
		self.motorDistance = _D
		self.stepsPerMM = [
			10,10
		]

	def moveTo(self, x, y, callback, penDir):
		newx = x + self.startx
		newy = y + self.starty

		newx_2 = newx * newx
		newy_2 = newy * newy

		DsubX = self.motorDistance - newx
		DsubX2 = DsubX * DsubX

		string_length_right = math.sqrt( newx_2 + newy_2 )
		string_length_left = math.sqrt( DsubX2 + newy_2 )

		steps_1 = round(string_length_right * self.stepsPerMM[0])
		steps_2 = round(string_length_left * self.stepsPerMM[1])

		sd1 = steps_1 - self.currentSteps[0]
		sd2 = steps_2 - self.currentSteps[1]
		print('sd:',sd1,sd2)

		sdir1 = 0 if (sd1>0) else 1
		sdir2 = 1 if (sd2>0) else 0
		print('sdir:',sdir1,sdir2)

		# // get steps with absolute value of steps difference
		ssteps1 = math.abs(sd1)
		ssteps2 = math.abs(sd2)
		print('ssteps:',ssteps1,ssteps2)


		def doRotation():
			# // do the rotation!
			rotateBoth(ssteps1,ssteps2,sdir1,sdir2,callback)

			# // store new current steps
			currentSteps[0] = s1
			currentSteps[1] = s2

			# // store new pos
			pos.x = x
			pos.y = y
	

		if(penDir != 0):
			# // MOVETO (default)
			# // pen up, then
			penThen(1, doRotation)
		else:
			# // LINETO
			doRotation()
	

	

	def lineTo( self,x,y,callback):
		penThen( 0, moveTo( float(x),  float(y), callback, 0) )


	def addPath( self, pathString):
		print('addPath')
		paths.push(pathString)
		print('pathcount: ',paths.length)
		if(paths.length==1 and drawingPath==False):
			drawNextPath()
	
	def pause( self ):
		paused = true

	def drawNextPath(self):
		if(paths.length>0):
			drawPath(paths.shift()) #// return/remove first path from array
		else:
			print("Done drawing all the paths. :)")

	def drawPath(self,pathString):
		drawingPath = true
		print('drawing path...')
		commands = svgParse(pathString)
		# // var commands = pathString.split(/(?=[MmLlHhVvZz])/)
		cmdCount = commands.length
		print(cmdCount)
		cmdIndex = 0
		prevCmd

		def doCommand():
			if(cmdIndex<cmdCount):
				cmd = commands[cmdIndex]
				cmdCode = cmd.code
				tox = pos.x
				toy = pos.y
				cmdIndex += 1
				percentage = round((cmdIndex/cmdCount)*100)
				print(cmd, percentage + '%')
				if(client):
					client.emit('progressUpdate',{
						botID: _BOT_ID,
						percentage: percentage
					}
					)
				if(localio):
					localio.emit('progressUpdate',{
						percentage: percentage
					}
					)


				if cmdCode == 'M': case_1()
				if cmdCode == 'L': case_2()
				if cmdCode == 'm': case_3()
				if cmdCode == 'l': case_4()
				if cmdCode == 'H': case_5()
				if cmdCode == 'h': case_6()
				if cmdCode == 'V': case_7()
				if cmdCode == 'v': case_8()
				if cmdCode == 'C': case_9()
				if cmdCode == 'c': case_10()
				if cmdCode == 'S': case_11()
				if cmdCode == 's': case_12()
				if cmdCode == 'Q': case_13()
				if cmdCode == 'q': case_14()
				if cmdCode == 'T': case_15()
				if cmdCode == 't': case_16()
				if cmdCode == 'A': case_17()
				if cmdCode == 'a': case_18()
				if cmdCode == 'Z': case_19()
				if cmdCode == 'z': case_19()

				def case_1():
					#// absolute move
					tox =  float(cmd.x)
					toy =  float(cmd.y)
					moveTo( float(tox),  float(toy), doCommand)
					
				def case_2():
					#// absolute line
					tox =  float(cmd.x)
					toy =  float(cmd.y)
					lineTo( float(tox),  float(toy), doCommand)
					
				def case_3():
					# // relative move
					tox +=  float(cmd.x)
					toy +=  float(cmd.y)
					moveTo( float(tox),  float(toy), doCommand)
					
				def case_4():
					#// relative line
					tox +=  float(cmd.x)
					toy +=  float(cmd.y)
					lineTo( float(tox),  float(toy), doCommand)
					
				def case_5():
					#// absolute horizontal line
					tox =  float(cmd.x)
					lineTo( float(tox),  float(toy), doCommand)
					
				def case_6():
					#// relative horizontal line
					tox +=  float(cmd.x)
					lineTo( float(tox),  float(toy), doCommand)
					
				def case_7():
					#// absolute vertical line
					toy =  float(cmd.y)
					lineTo( float(tox),  float(toy), doCommand)
					
				def case_8():
					#// relative vertical line
					toy +=  float(cmd.y)
					lineTo( float(tox),  float(toy), doCommand)
					
				def case_9():
					#// absolute cubic bezier curve
					drawCubicBezier(
						# // [{x:tox,y:toy}, {x:cmd.x1,y:cmd.y1}, {x:cmd.x2,y:cmd.y2}, {x:cmd.x,y:cmd.y}],
						# // 0.01,
						[ [tox,toy], [cmd.x1,cmd.y1], [cmd.x2,cmd.y2], [cmd.x,cmd.y] ],
						1,
						doCommand
					)
					
				def case_10():
					#// relative cubic bezier curve
					drawCubicBezier(
						# // [{x:tox,y:toy}, {x:tox+cmd.x1,y:toy+cmd.y1}, {x:tox+cmd.x2,y:toy+cmd.y2}, {x:tox+cmd.x,y:toy+cmd.y}],
						# // 0.01,
						[ [tox,toy], [tox+cmd.x1,toy+cmd.y1], [tox+cmd.x2,toy+cmd.y2], [tox+cmd.x,toy+cmd.y] ],
						1,
						doCommand
					)
					
				def case_11():
					#// absolute smooth cubic bezier curve
					
					#// check to see if previous command was a C or S
					#// if not, the inferred control point is assumed to be equal to the start curve's start point
					inf
					if (prevCmd.command.indexOf('curveto')<0):
						inf = {
							x:tox,
							y:toy
						}
					
					else:
						#// get absolute x2 and y2 values from previous command if previous command was relative
						if(prevCmd.relative):
							prevCmd.x2 = pos.x - prevCmd.x + prevCmd.x2
							prevCmd.y2 = pos.y - prevCmd.y + prevCmd.y2
					
						#// calculate inferred control point from previous commands
						#// reflection of x2,y2 of previous commands
						inf = {
							x: tox+(tox-prevCmd.x2), #// make prevCmd.x2 and y2 values absolute, not relative for calculation
							y: toy+(toy-prevCmd.y2)
						}
				

					#// draw it!
					pts = [ [tox,toy], [inf.x,inf.y], [cmd.x2,cmd.y2], [cmd.x,cmd.y] ]
					print('calculated points:',pts)
					drawCubicBezier(
						pts,
						1,
						doCommand
					)
					
					
				def case_12():
					#// relative smooth cubic bezier curve

					#// check to see if previous command was a C or S
					#// if not, the inferred control point is assumed to be equal to the start curve's start point
					inf
					if (prevCmd.command.indexOf('curveto')<0):
						inf = {
							x:tox,
							y:toy
						}
					
					else:
						# // get absolute x2 and y2 values from previous command if previous command was relative
						if(prevCmd.relative):
							prevCmd.x2 = pos.x - prevCmd.x + prevCmd.x2
							prevCmd.y2 = pos.y - prevCmd.y + prevCmd.y2
					
						#// calculate inferred control point from previous commands
						#// reflection of x2,y2 of previous commands
						inf = {
							x: tox+(tox-prevCmd.x2),
							y: toy+(toy-prevCmd.y2)
						}
					
				

					#// draw it!
					drawCubicBezier(
						[ [tox,toy], [inf.x,inf.y], [tox+cmd.x2,toy+cmd.y2], [tox+cmd.x,toy+cmd.y] ],
						1,
						doCommand
					)
					
				def case_13():
					#// absolute quadratic bezier curve
					drawQuadraticBezier(
						[ [tox,toy], [cmd.x1,cmd.y1], [cmd.x,cmd.y] ],
						1,
						doCommand
					)
					
				def case_14():
					#// relative quadratic bezier curve
					drawQuadraticBezier(
						[ [tox,toy], [tox+cmd.x1,toy+cmd.y1], [tox+cmd.x,toy+cmd.y] ],
						1,
						doCommand
					)
					
				
				def case_15():
					#// absolute smooth quadratic bezier curve
					
					#// check to see if previous command was a C or S
					#// if not, the inferred control point is assumed to be equal to the start curve's start point
					inf
					if (prevCmd.command.indexOf('curveto')<0):
						inf = {
							x:tox,
							y:toy
						}
					else:
						#// get absolute x1 and y1 values from previous command if previous command was relative
						if(prevCmd.relative):
							prevCmd.x1 = pos.x - prevCmd.x + prevCmd.x1
							prevCmd.y1 = pos.y - prevCmd.y + prevCmd.y1
					
						#// calculate inferred control point from previous commands
						#// reflection of x1,y1 of previous commands
						inf = {
							x: tox+(tox-prevCmd.x1),
							y: toy+(toy-prevCmd.y1)
						}	
				

					#// draw it!
					drawQuadraticBezier(
						[ [tox,toy], [inf.x,inf.y], [cmd.x,cmd.y] ],
						1,
						doCommand
					)
					
					
				def case_16():
					#// relative smooth quadratic bezier curve

					#// check to see if previous command was a C or S
					#// if not, the inferred control point is assumed to be equal to the start curve's start point
					inf
					if (prevCmd.command.indexOf('curveto')<0):
						inf = {
							x:tox,
							y:toy
						}
					
					else:
						#// get absolute x1 and y1 values from previous command if previous command was relative
						if(prevCmd.relative):
							prevCmd.x1 = pos.x - prevCmd.x + prevCmd.x1
							prevCmd.y1 = pos.y - prevCmd.y + prevCmd.y1
					
						#// calculate inferred control point from previous commands
						#// reflection of x2,y2 of previous commands
						inf = {
							x: tox+(tox-prevCmd.x1),
							y: toy+(toy-prevCmd.y1)
						}
				

					#// draw it!
					drawQuadraticBezier(
						[ [tox,toy], [inf.x,inf.y], [tox+cmd.x,toy+cmd.y] ],
						1,
						doCommand
					)
					

				def case_17():
					#// absolute arc

					#// convert arc to cubic bezier curves
					curves = arcToBezier({
						px: tox,
						py: toy,
						cx: cmd.x,
						cy: cmd.y,
						rx: cmd.rx,
						ry: cmd.ry,
						xAxisRotation: cmd.xAxisRotation,
						largeArcFlag: cmd.largeArc,
						sweepFlag: cmd.sweep
					}
				)
					print(curves)

					# // draw the arc
					drawArc(curves,doCommand)
					
					
				
				def case_18():
					# // relative arc TODO: CHECK THIS!

					# // convert arc to cubic bezier curves
					curves = arcToBezier({
						px: tox,
						py: toy,
						cx: tox+cmd.x,#// relative
						cy: toy+cmd.y,#// relative
						rx: cmd.rx,
						ry: cmd.ry,
						xAxisRotation: cmd.xAxisRotation,
						largeArcFlag: cmd.largeArc,
						sweepFlag: cmd.sweep
					}
				)
					print(curves)

					#// draw the arc
					drawArc(curves,doCommand)
					
					

				def case_19():
					doCommand()
						
			

				prevCmd = cmd
				
			else:
				cmdCount = 0
				cmdIndex = 0
				print('path done!')
				drawingPath = False
				drawNextPath()
		
	
		doCommand()


	def drawArc(self, curves, callback):
		n=0
		cCount = curves.length
		def doCommand():
			if(n<cCount):
				crv = curves[n]
				# // draw the cubic bezier curve created from arc input
				drawCubicBezier(
					[ [pos.x, pos.y], [crv.x1, crv.y1], [crv.x2, crv.y2], [crv.x, crv.y] ],
					1,
					doCommand
				)
				n += 1

			else:
				if ( callback!= None ):
					callback()
		
	
		doCommand()


	# /// NEW WAY (adaptive, per https://www.npmjs.com/package/adaptive-bezier-curve)
	# // TODO: combine cubic/quadratic versions into one with a parameter
	def drawCubicBezier (self, points, scale, callback):
		n = 0 # // curret bezier step in iteration
		pts = cBezier(points[0], points[1], points[2], points[3], scale)
		ptCount = pts.length
		def doCommand():
			if(n<ptCount):
				pt = pts[n]
				lineTo( float(pt[0]),  float(pt[1]), doCommand)
				n += 1
			else:
				# // print('bezier done!')
				if (callback!= None ):
					callback()
		
	
		doCommand()



	def drawQuadraticBezier(self, points, scale, callback):
		n = 0 # // curret bezier step in iteration
		pts = qBezier(points[0], points[1], points[2], scale)
		ptCount = pts.length
		def doCommand():
			if(n<ptCount):
				pt = pts[n]
				lineTo( float(pt[0]),  float(pt[1]), doCommand)
				n += 1
			else:
				# // print('bezier done!')
				if (callback!= None ):
					 callback()
			
		
		doCommand()
	

	def drawCircle(self, x, y, r, callback):
		None
		# // http://jsfiddle.net/heygrady/X5fw4/
		# // Calculate a point on a circle
		def circle(t, radius) :
			r = radius or 100
			arc = math.PI * 2

			# // calculate current angle
			alpha = t * arc

			# // calculate current coords
			x = math.sin(alpha) * r
			y = math.cos(alpha) * r

			# // return coords
			return [x, y * -1]
		

		n = 0 #//current step
		pi = 3.1415926
		C = 2*pi*r
		seg = C

		def doCommand():
			if(n<=seg):
				t = n/seg
				p = circle(t, r)
				if( n == 0 ):
					moveTo(x+p[0], y+p[1], doCommand)
				else:
					lineTo(x+p[0], y+p[1], doCommand)
				
				n += 1
			else:
				if (callback!= None ):
					 callback()
			
		doCommand()

	def drawCircles(self, o):
		print(o.count)
		count = o.count
		n = 0

		def doCommand():
			if(n<count):
				drawCircle(o.x[n], o.y[n], o.r[n], doCommand)
				print(n/count)
				n += 1
			else:
				print('done with circles!')

		doCommand()
