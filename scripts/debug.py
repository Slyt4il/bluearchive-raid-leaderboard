import pyautogui
import pygetwindow as gw
import cv2

emulator_window = gw.getWindowsWithTitle("LDPlayer")[0]  # Replace with your emulator's title
emulator_window.activate()
window_x, window_y, window_width, window_height = emulator_window.left, emulator_window.top, emulator_window.width, emulator_window.height

def update():
    return emulator_window.left, emulator_window.top, emulator_window.width, emulator_window.height

relative_anchor_x, relative_anchor_y = (530, 320) #(530, 320)
anchor_pixel = (55, 57, 60) #(55, 57, 60)

def check_anchors():
    anchor_x = window_x + relative_anchor_x
    anchor_y = window_y + relative_anchor_y
    if not pyautogui.pixel(anchor_x, anchor_y) == anchor_pixel:
        return 'Anchor is not in position'
    elif pyautogui.pixel(anchor_x, anchor_y - 1) == anchor_pixel:
        return 'Anchor is not in position'
    else:
        return 'Anchor is in position'

print("Ctrl + C to exit")

while True:
    window_x, window_y, window_width, window_height = update()
    print(f'Window: {window_x, window_y} | {check_anchors()}'.ljust(50), end='\r')

""" def click_event(event, x, y, flags, params):
   if event == cv2.EVENT_LBUTTONDOWN:
      print(f'({x},{y})')
      cv2.putText(im, f'({x},{y})',(x,y),
      cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
      cv2.circle(im, (x,y), 3, (0,255,255), -1)

im = cv2.imread('raw_data\S44_Hieronymus_Urban\\1.jpg')
cv2.namedWindow('coords')
cv2.setMouseCallback('coords', click_event)
while True:
   cv2.imshow('coords', im)
   k = cv2.waitKey(1) & 0xFF
   if k == 27:
      break
cv2.destroyAllWindows() """

pyautogui.displayMousePosition()
