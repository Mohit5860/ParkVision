import cv2
import easyocr

def generate_number():
    image = cv2.imread('new.jpeg')
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image)

    slot_numbers = []

    for (bbox, text, prob) in results:
        if text.isdigit() and prob > 0.7: 
            slot_numbers.append(text)

    return slot_numbers

list = generate_number()
# print(list)
    # for i, slot_number in enumerate(slot_numbers):
    #     print(f"Slot {i + 1}: {slot_number}")

    # for (bbox, text, prob) in results:
    #     (top_left, top_right, bottom_right, bottom_left) = bbox
    #     top_left = tuple(map(int, top_left))
    #     bottom_right = tuple(map(int, bottom_right))
    #     cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
    #     cv2.putText(image, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # cv2.imshow('Parking Lot', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
