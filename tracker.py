import cv2

class Tracker:
  def __init__(self):
    self.bb = None
    self.frame = None
    self.tracker = cv2.TrackerCSRT_create()

  def callback(self, frame):
    if self.bb is not None:
      (success, box) = self.tracker.update(frame)
      if success:
        (x, y, w, h) = [int(v) for v in box]
        cv2.rectangle(frame, (x, y), (x + w, y + h),(0, 255, 0), 2)
      return frame
    else:
      cv2.imshow("Select object", frame)
      key = cv2.waitKey(1) & 0xFF
      
      if key == ord('s'):
        self.bb = cv2.selectROI("Select object", frame, fromCenter=False, showCrosshair=True)
        self.tracker.init(frame, self.bb)
        cv2.destroyWindow("Select object")
      return frame

  def defineBB(self):
    pass