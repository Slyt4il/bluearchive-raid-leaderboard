import time
import os
import pyautogui
import pygetwindow as gw

# The Android emulator window
emulator_window = gw.getWindowsWithTitle("LDPlayer")[0]  # Replace with your emulator's title
emulator_window.activate()

# The coordinates of the capture area within the emulator window
relative_start_x = 512
relative_start_y = 300
relative_end_x = 740 #1170
relative_end_y = 450

# Save folder
save_folder = "raw_data\S44_Hieronymus_Urban"

# Number of screenshots to take
num_screenshots = 1

# Start index for filename
offset = 10000

# Delay between each action (in seconds)
delay = 0.1

print("To exit, slam your mouse to the corner of the screen and trigger PyAutoGUI failsafe :)")
for i in range(3):
    print(f"Starting in {3-i}...")
    time.sleep(1)

correction_deg = 1
correction_dir = 0
for i in range(num_screenshots):
    window_x, window_y, window_width, window_height = emulator_window.left, emulator_window.top, emulator_window.width, emulator_window.height

    start_x = window_x + relative_start_x
    start_y = window_y + relative_start_y
    end_x = window_x + relative_end_x
    end_y = window_y + relative_end_y

    screenshot = pyautogui.screenshot(region=(start_x, start_y, end_x - start_x, end_y - start_y))
    screenshot.save(os.path.join(save_folder, f'{offset+i}.jpg'))

    pyautogui.moveTo(end_x, end_y)

    relative_anchor_x, relative_anchor_y = (530, 320) #(530, 320)
    anchor_pixel = (55, 57, 60) #(55, 57, 60)
    anchor_x = window_x + relative_anchor_x
    anchor_y = window_y + relative_anchor_y
    target_y = start_y - 51
    # Check if undershooting
    if not pyautogui.pixel(anchor_x, anchor_y) == anchor_pixel:
        print(f"Undershooting at {offset+i}. Correcting by {correction_deg}px".ljust(50), end='\r')
        correction_deg = correction_deg + 1 if correction_dir == -1 else 1
        correction_dir = -1
        correction_deg = max(min(correction_deg, 3), -3)
    # Check if overshooting
    elif pyautogui.pixel(anchor_x, anchor_y - 1) == anchor_pixel:
        print(f"Overshooting at {offset+i}. Correcting by {correction_deg}px".ljust(50), end='\r')
        correction_deg = correction_deg + 1 if correction_dir == 1 else 1
        correction_dir = 1
        correction_deg = max(min(correction_deg, 3), -3)
    else:
        correction_deg = 1
        correction_dir = 0

    target_y = start_y - 51 + (correction_deg * correction_dir)

    pyautogui.dragTo(end_x, target_y, duration=2.0, tween=pyautogui.easeOutQuad)

    time.sleep(delay)
