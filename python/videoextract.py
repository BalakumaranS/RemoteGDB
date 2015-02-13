import cv2

vidcap = cv2.VideoCapture('C:\Users\Public\Videos\Sample Videos\Wildlife.wmv')
count = 0;
while success:
  image = vidcap.read()
  cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
  if cv2.waitKey(10) == 27:                     # exit if Escape is hit
      break
  count += 1
