from django.shortcuts import render, HttpResponse
from parkVision.models import Car
from datetime import datetime
from django.http import JsonResponse

import cv2
import easyocr

# Create your views here.
def home(request):
    return render(request, "home.html", {})

def features(request):
    return render(request, "features.html", {})

def entry(request):
    print("working")
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
    response = {
        'number' : 23,
        'image_url' : "https://imgs.search.brave.com/Rj-yt2o7wXMGBGe_q2Von992X5y1C8W6Gd_Z1XFoURs/rs:fit:500:0:0/g:ce/aHR0cHM6Ly9pbWFn/ZXMudW5zcGxhc2gu/Y29tL3Bob3RvLTE0/NDQ3MDM2ODY5ODEt/YTNhYmJjNGQ0ZmUz/P2F1dG89Zm9ybWF0/JmZpdD1jcm9wJnE9/ODAmdz0xMDAwJml4/bGliPXJiLTQuMC4z/Jml4aWQ9TTN3eE1q/QTNmREI4TUh4elpX/RnlZMmg4T0h4OGNH/bGpkSFZ5Wlh4bGJu/d3dmSHd3Zkh4OE1B/PT0.jpeg"
    }
    return JsonResponse(response)

def show(request):
    number = request.POST.get('number')
    car = Car.objects.get(car_number = number)
    car.delete()
    return render(request, "delete.html", {})