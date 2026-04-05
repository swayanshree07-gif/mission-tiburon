#!/usr/bin/env python3

import cv2
import numpy as np

def main():
    # Open default camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return

    # Define the color range for tracking (HSV)
    # Example: Red color
    lower_color = np.array([0, 120, 70])
    upper_color = np.array([10, 255, 255])
    # You can change the color as per preference

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Cannot receive frame")
            break

        # -------- Edge Detection --------
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)  # vertical
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)  # horizontal
        sobelx = cv2.convertScaleAbs(sobelx)
        sobely = cv2.convertScaleAbs(sobely)
        edges = cv2.addWeighted(sobelx, 0.5, sobely, 0.5, 0)

        # Convert edges to BGR to overlay on original
        edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        # -------- Color Tracking --------
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_color, upper_color)

        # Morphology to remove noise
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            # Get the largest contour
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                # Draw centroid
                cv2.circle(edges_bgr, (cx, cy), 5, (0, 255, 0), -1)
                cv2.putText(edges_bgr, f"Centroid: ({cx},{cy})", (cx+10, cy-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
                print(f"Centroid: ({cx}, {cy})")

        # Overlay edges on original frame
        combined = cv2.addWeighted(frame, 0.7, edges_bgr, 0.3, 0)

        # Show result
        cv2.imshow('Perception - Edge + Color Tracking', combined)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
