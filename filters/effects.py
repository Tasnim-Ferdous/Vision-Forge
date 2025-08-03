import cv2

def apply_filter(frame, filter_type):
    if filter_type == "gray":
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    elif filter_type == "sketch":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        inv = 255 - gray
        blur = cv2.GaussianBlur(inv, (21, 21), 0)
        sketch = cv2.divide(gray, 255 - blur, scale=256.0)
        return cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)

    elif filter_type == "cartoon":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(blur, 255,
                                      cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(frame, 9, 300, 300)
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        return cartoon

    else:
        return frame
