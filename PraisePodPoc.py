import cv2.cv as cv

# --Todo--
# Record Interface Button
# Debug info

def StartCam():
	#cv.NamedWindow("PraisePod (Proof Of Concept)", 1)
	recording = False
	
	capture = cv.CaptureFromCAM(0)
	frame = cv.RetrieveFrame(capture)
	frame_size = cv.GetSize(frame)
	fps = 10.0																			# FPS Set low to reduce output video speed.
	
	font = cv.InitFont(cv.CV_FONT_HERSHEY_COMPLEX_SMALL, 1, 1, 0, 1, 1)
	fontTitle = cv.InitFont(cv.CV_FONT_HERSHEY_COMPLEX_SMALL, 0.8, 0.8, 0, 1, 1)
	
	writer = cv.CreateVideoWriter("out.avi", cv.CV_FOURCC('D', 'I', 'V', 'X'), 
						  fps, frame_size, True)
	
	while True:
		img = cv.QueryFrame(capture)
		cv.PutText(frame,"PraisePod - Proof Of Concept", (frame_size[0] / 2,30), fontTitle, (0,0,255))
		if recording == False:
			cv.PutText(frame,"Press space to start recording.", (10,frame_size[1] - 10), font, (0,0,255))			# To be replaced with interface button.
		else:
			cv.PutText(frame,"Recording...", (10,frame_size[1] - 10), font, (0,0,255))
		cv.ShowImage("camera", img)
		
		# Write Frames once recording is enabled.
		if recording == True:
			frame = cv.RetrieveFrame(capture)
			cv.WriteFrame(writer, frame)
		if cv.WaitKey(10) == 32:
			if recording == False:
				recording = True;
			else:
				recording = False;
		if cv.WaitKey(10) == 27:
			break
			

if __name__ == '__main__':
	print("PraisePod (Proof Of Concept)")
	raw_input("Press Enter to start...")
	StartCam()
