#!/opt/local/bin/python
import cv

#cv.NamedWindow("w1", cv.CV_WINDOW_AUTOSIZE)
camera_index = 0
capture = cv.CaptureFromCAM(camera_index)
image_scale = 2

def repeat():
  global capture #declare as globals since we are assigning to them now
  global camera_index
  frame = cv.QueryFrame(capture)
  gray = cv.CreateImage((frame.width,frame.height), 8, 1)
  small_img = cv.CreateImage((cv.Round(frame.width / image_scale),
                              cv.Round (frame.height / image_scale)), 8, 1)
  img = small_img
  thres = cv.CreateImage((img.width, img.height), 8, 1)
  contours_img = cv.CreateImage((img.width, img.height), 8, 1)
  #ad_thres = cv.CreateImage((img.width, img.height), 8, 1)
  cv.CvtColor(frame, gray, cv.CV_BGR2GRAY)
  cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)
  cv.Threshold(img, thres, 80, 255, cv.CV_THRESH_BINARY);
  # should use Kenny algorithm too
  #cv.AdaptiveThreshold(img, ad_thres, 250, cv.CV_ADAPTIVE_THRESH_GAUSSIAN_C,
  #                     cv.CV_THRESH_BINARY, 5, 1);

  contours_img = cv.CloneImage(thres)
  contours = cv.FindContours(contours_img, cv.CreateMemStorage(0),
                             cv.CV_RETR_LIST,cv.CV_CHAIN_APPROX_SIMPLE);

  while contours:
    cv.DrawContours(img, contours, cv.CV_RGB(255,216,0),
                    cv.CV_RGB(0,0,250), 0, 1, 8);
    contours = contours.h_next()

  #cv.ShowImage("w1", frame)
  #cv.ShowImage("gray", gray)
  cv.ShowImage("test image", img)
  cv.ShowImage("thresshold", thres)
  #cv.ShowImage("adaptive threshold", ad_thres)
  c = cv.WaitKey(10)
  if(c=="n"): #in "n" key is pressed while the popup window is in focus
    camera_index += 1 #try the next camera index
    capture = cv.CaptureFromCAM(camera_index)
    if not capture: #if the next camera index didn't work, reset to 0.
      camera_index = 0
      capture = cv.CaptureFromCAM(camera_index)
while True:
  repeat()
