from django.shortcuts import render, HttpResponse
from parkVision.models import Car
from datetime import datetime
from django.http import JsonResponse

import cv2
import easyocr

# Create your views here.
def home(request):
    return render(request, "home.html", {})

# def features(request):
#     return render(request, "features.html", {})

def entry(request):
    if request.method == "POST":
        print("request")
        car_number = request.POST.get('number')
        slot_number = request.POST.get('mycheckbox')
        dateAndTime = datetime.now()
        car = Car(car_number=car_number, slot_number=slot_number, time=dateAndTime.strftime("%H:%M:%S"))
        car.save()
        print("Saved")
    return render(request, "entry.html", {})

def manage(request):
    if request.method == "POST":
        input = request.POST.get('input')
        car = Car.objects.get(car_number = input)
        return render(request, "search.html", {'car': car})
    context = Car.objects.all()
    return render(request, "manage.html", {'cars' : context})

def exit(request):
    if request.method == "POST":
        number = request.POST.get('number')
        car = Car.objects.get(car_number=number)
        return render(request, "show.html", {'car' : car})
    return render(request, "exit.html", {})

def generate(request):
    # if request == "POST":
    image = cv2.imread('/home/mohit/Coding/Python/Project/parkVision/new.jpeg')
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image)

    slot_numbers = []

    for (bbox, text, prob) in results:
        if text.isdigit() and prob > 0.7: 
            slot_numbers.append(text)
    # for i, slot_number in enumerate(slot_numbers):
    #     print(f"Slot {i + 1}: {slot_number}")

    for (bbox, text, prob) in results:
        (top_left, top_right, bottom_right, bottom_left) = bbox
        top_left = tuple(map(int, top_left))
        bottom_right = tuple(map(int, bottom_right))
        cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
        cv2.putText(image, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow('Parking Lot', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    response = {'my_list': slot_numbers}
    return JsonResponse(response)

def scan(request):
    harcasecade = "model/numberplate_haarcade.xml"
    reader = easyocr.Reader(['en'])

    cap = cv2.VideoCapture(0)

    cap.set(3,640) # width
    cap.set(4,480) # height

    min_area = 500
    count = request.session.get('count', 0)
    car_number = None

    while True:
        success, img = cap.read()
        plate_cascade = cv2.CascadeClassifier(harcasecade)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

        for (x,y,w,h) in plates:
            area = w*h 
            if area>min_area:
                cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
                cv2.putText(img, "Number Plate", (x,y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,255), 2)

                img_roi = img[y: y+h, x: x+w]

        cv2.imshow("Result", img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            cv2.imwrite("plates/scned_img_" + str(count) + ".jpg", img_roi)
            cv2.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, "Plate Saved", (150, 265), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), 2)
            cv2.imshow("Results", img)
            cv2.waitKey(500)
            output = reader.readtext("plates/scned_img_" + str(count) + ".jpg")
            if output:
                car_number = output[0][-2]
                print("Car Number:", car_number)
            else:
                print("No text detected on the number plate.")
            count += 1
        elif key == ord('q'):
            break
    request.session['count'] = count
    cap.release()
    cv2.destroyAllWindows()

    response = {
        'number' : car_number,
        'image_url' : f"plates/scned_img_{count - 1}.jpg"
    }
    return JsonResponse(response)

def show(request):
    number = request.POST.get('number')
    car = Car.objects.get(car_number = number)
    car.delete()
    return render(request, "delete.html", {})