import cv2 
import argparse
import os

# Function to extract frames 
def FrameCapture(path, threshold, callbacks): 
	
	# Path to video file 
	vidObj = cv2.VideoCapture(path) 

	# Used as counter variable 
	count = 0

	# checks whether frames were extracted 
	success = 1

	while success: 
		# Function extract frames 
		success, image = vidObj.read()
	
		if success:
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			
			for callback in callbacks:
				image = callback(image)

			#Filter to check for blurriness
			fm = cv2.Laplacian(gray, cv2.CV_64F).var()
			if fm >= threshold:
				name = "frame" + str(count) + ".jpg"
				cv2.imwrite(os.path.join(os.getcwd(), "custom hammer dataset/" + name), image)
			count += 1
			cv2.imshow("InnoIris", image)

		# Code for terminating the window
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			vidObj.release()
			cv2.destroyAllWindows()
			break

# Driver Code 
def main():
	ap = argparse.ArgumentParser()
	ap.add_argument("-p", "--path", required=True, help="path to video file")
	ap.add_argument("-t", "--thres", required=False, type=float, default=500.0) # Threshold is very scene dependent. Make sure to specify one
	args = vars(ap.parse_args())
	FrameCapture(args["path"], args["thres"]) 

if __name__ == "__main__":
	main()