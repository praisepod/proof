import cv2.cv as cv
import pyaudio
import wave
import os

# --Todo--
# Debug info

class Camera:
	def __init__(self):
		self.recording = False
		self.capture = cv.CaptureFromCAM(0)
		self.frame = cv.RetrieveFrame(self.capture)
		self.defaultFont = cv.InitFont(cv.CV_FONT_HERSHEY_COMPLEX_SMALL, 1, 1, 0, 1, 1)
		self.titleFont = cv.InitFont(cv.CV_FONT_HERSHEY_COMPLEX_SMALL, 0.8, 0.8, 0, 1, 1)
		
		self.CHUNK = 1024
		self.FORMAT = pyaudio.paInt16
		self.CHANNELS = 2
		self.RATE = 44100
		self.output_filename_base = "temp"
		
		self.pyA = pyaudio.PyAudio()
	
	def StartCam(self):
		if self.frame is not None:			
			self.RecordAV()
		else:
			os.system("echo 'Error: Unable to find a camera. Check the USB connection.'")
				
	def RecordAV(self):
			frame_size = cv.GetSize(self.frame)
			fps = 10.0																			# FPS Set low to reduce output video speed.
			
			writer = cv.CreateVideoWriter("temp/" + self.output_filename_base + ".avi", cv.CV_FOURCC('D', 'I', 'V', 'X'), 
								  fps, frame_size, True)
			
			stream = self.pyA.open(format=self.FORMAT,
					channels=self.CHANNELS,
					rate=self.RATE,
					input=True,
					frames_per_buffer=self.CHUNK)
		
			frames = []
		
			#Main Display/Record Loop
			while True:
				img = cv.QueryFrame(self.capture)
				cv.PutText(self.frame,"PraisePod - Proof Of Concept", (frame_size[0] / 2,30), self.titleFont, (0,0,255))
				if self.recording == False:
					cv.PutText(self.frame,"Press space to start recording.", (10,frame_size[1] - 10), self.defaultFont, (0,0,255))			# To be replaced with interface button.
				else:
					cv.PutText(self.frame,"Recording...", (10,frame_size[1] - 10), self.defaultFont, (0,0,255))
				cv.ShowImage("camera", img)
				
				# Write Frames once recording is enabled.
				if self.recording == True:
					self.frame = cv.RetrieveFrame(self.capture)
					cv.WriteFrame(writer, self.frame)
					data = stream.read(self.CHUNK)
					frames.append(data)
				if cv.WaitKey(10) == 32:
					if self.recording == False:
						self.recording = True;
					else:
						self.recording = False;
						
						stream.stop_stream()
						stream.close()
						self.pyA.terminate()

						wf = wave.open("temp/" + self.output_filename_base + ".wav", 'wb')
						wf.setnchannels(self.CHANNELS)
						wf.setsampwidth(self.pyA.get_sample_size(self.FORMAT))
						wf.setframerate(self.RATE)
						wf.writeframes(b''.join(frames))
						wf.close()
						
						os.system("echo 'Combining Streams'")
						os.system("ffmpeg -i temp/" + self.output_filename_base + ".wav -i temp/" + self.output_filename_base + ".avi -y -acodec copy -vcodec copy output.avi")
						os.system("echo 'Video and Audio Processing Complete!'")
				if cv.WaitKey(10) == 27:
					break	
		
if __name__ == '__main__':
	print("PraisePod (Proof Of Concept)")
	raw_input("Press Enter to start...")
	camera = Camera()
	camera.StartCam()
