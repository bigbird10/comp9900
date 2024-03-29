from django.shortcuts import render, redirect
from . import forms, models
from django.contrib import auth
from comp9900.settings import MEDIA_ROOT
from django.http import HttpResponseRedirect
from django.urls import reverse
import os
import geocoder
import datetime
import pandas as pd

# Create your views here.

googlekey = "AIzaSyDjov91CSH-WKVpABgttFZnDS4_RSvaTSw"
def index(request):
    return render(request, 'homePage.html')


def userRegister(request):
    message = ""
    if request.method == 'POST':
        registerForm = forms.UserRegisterForm(request.POST)
        if registerForm.is_valid():
            email = registerForm.cleaned_data['email']
            username = registerForm.cleaned_data['username']
            password = registerForm.cleaned_data['password']
            firstName = registerForm.cleaned_data['firstName']
            lastName = registerForm.cleaned_data['lastName']
            phone = registerForm.cleaned_data['phone']
            birthday = registerForm.cleaned_data['birthday']
            if not models.User.objects.filter(username=username).exists() \
                or not models.User.objects.filter(email=email):
                newGuest = models.User()
                newGuest.email = email
                newGuest.username = username
                newGuest.set_password(password)
                newGuest.first_name = firstName
                newGuest.last_name = lastName
                newGuest.phone = phone
                newGuest.birthday = birthday
                newGuest.save()
                message = "register successful!"
                return redirect('/index/')
            else:
                message = "username or email already exists"
        else:
            message = "invalid input"
    else:
        RegisterForm = forms.UserRegisterForm()

    return render(request, "userRegister.html", locals())


def userLogin(request):
    message = ""
    if request.method == 'POST':
        user = None
        loginForm = forms.UserForm(request.POST)
        if loginForm.is_valid():
            username = loginForm.cleaned_data['username']
            password = loginForm.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
        if user and models.User.objects.filter(username=username).exists():
            auth.login(request, user)
            return redirect('/index/')
        else:
            message = "User doesn't exist or password is incorrect!"
            return render(request, "userLogin.html", locals())
    else:
        loginForm = forms.UserForm()
        return render(request, "userLogin.html", locals())


def updateUserInfo(request):
    if request.method == 'POST':
        form = forms.UserInfoUpdateForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            firstName = form.cleaned_data['firstName']
            lastName = form.cleaned_data['lastName']
            phone = form.cleaned_data['phone']
            birthday = form.cleaned_data['birthday']
            description = form.cleaned_data['description']

            user1 = models.User.objects.get(id=request.user.id)
            user1.email = email
            user1.first_name = firstName
            user1.last_name = lastName
            user1.phone = phone
            user1.birthday = birthday
            user1.description = description
            user1.save()

            return redirect('/updateUserInfo/')

    dict = {}
    user1 = models.User.objects.get(id=request.user.id)
    if user1.email:
        dict['email'] = user1.email
    if user1.first_name:
        dict['firstName'] = user1.first_name
    if user1.last_name:
        dict['lastName'] = user1.last_name
    if user1.phone:
        dict['phone'] = user1.phone
    if user1.birthday:
        dict['birthday'] = user1.birthday
    if user1.description:
        dict['description'] = user1.description

    photo = "/pictures/e1b5f44d998ccbf08cf5571d45e93cbb.png"
    if user1.portrait:
        photo = user1.portrait

    InitialUserForm = forms.UserInfoUpdateForm(initial=dict)
    FileForm = forms.FileForm()
    return render(request, 'updateUserInfo.html', locals())


def portraitUpload(request):
    if request.method == 'POST':
        pic = request.FILES.get('file')
        user = models.User.objects.get(id=request.user.id)
        url = os.path.join(MEDIA_ROOT, pic.name)
        with open(url, 'w+b') as f:
            for data in pic.chunks():
                f.write(data)
        user.portrait = "pictures/" + pic.name
        user.save()
    return redirect('/updateUserInfo/')


def listingManage(request):
    if 'listing_id' in request.session:
        del request.session['listing_id']

    request.session['role'] = "host"
    if request.method == 'GET':
        if request.user and request.user.is_authenticated:
            listings = []
            temp = models.Listing.objects.filter(host_id=request.user.id)
            if temp.exists():
                for item in temp:
                    listings.append((item.id, item.city, item.name))
            return render(request, 'listingManage.html', locals())
    elif request.method == 'POST':
        listing_id = int(request.POST.get('listing_id'))
        delete = int(request.POST.get('delete'))
        if delete == 0:
            if listing_id == -1:
                return HttpResponseRedirect(reverse('listingStart'))
            else:
                request.session['listing_id'] = listing_id
                return HttpResponseRedirect(reverse('listingStart'))
        else:
            if models.Listing.objects.filter(pk=listing_id, host_id=request.user.id).exists():
                if models.Scene.objects.filter(listing_id=listing_id).exists():
                    for item in models.Scene.objects.filter(listing_id=listing_id):
                        item.delete()
                cur = models.Listing.objects.get(pk=listing_id)
                cur.delete()
                listings = []
                if models.Listing.objects.filter(host_id=request.user.id).exists():
                    for item in models.Listing.objects.filter(host_id=request.user.id):
                        listings.append((item.id, item.city, item.name))
            return render(request, 'listingManage.html', locals())


def listingStart(request):
    if request.method == 'POST':
        form = forms.ListingForm(request.POST)
        if form.is_valid():
            property_type = form.cleaned_data['property_type']
            room_type = form.cleaned_data['room_type']
            numOfGusets = form.cleaned_data['Guests']
            numOfBedrooms = form.cleaned_data['Bedrooms']
            numOfBeds = form.cleaned_data['Beds']
            numOfBathrooms = form.cleaned_data['Bathrooms']
            price = form.cleaned_data['Price']

            if 'listing_id' in request.session:
                listing_id = request.session['listing_id']
                listing = models.Listing.objects.get(pk=listing_id)
            else:
                listing = models.Listing()

            listing.host_id = request.user.id
            listing.property_type = property_type
            listing.room_type = room_type
            listing.accommodates = numOfGusets
            listing.bedrooms = numOfBedrooms
            listing.beds = numOfBeds
            listing.bathrooms = numOfBathrooms
            listing.price = price
            listing.save()
            request.session['listing_id'] = listing.id
            return HttpResponseRedirect(reverse('amenities'))
    else:
        if 'listing_id' in request.session:
            listing_id = request.session['listing_id']
            listing = models.Listing.objects.get(pk=listing_id)
            listingForm = forms.ListingForm(initial={
                "property_type": listing.property_type,
                "room_type": listing.room_type,
                "Guests": listing.accommodates,
                "Bedrooms": listing.bedrooms,
                "Beds": listing.beds,
                "Bathrooms": listing.bathrooms,
                "Price": listing.price
            })
        else:
            listingForm = forms.ListingForm()
        return render(request, 'listingAdd/listingStart.html', locals())


def amenities(request):
    if request.method == 'POST':
        form = forms.AmenitiesForm(request.POST)
        if form.is_valid():
            amenities_list = ['essentials', 'air_conditioning', 'heat', 'hair_dryer', 'wifi', 'iron', 'shampoo', 'desk']
            if 'listing_id' in request.session:
                listing_id = request.session['listing_id']
                listing = models.Listing.objects.get(pk=listing_id)
                amenities_text = ''
                for i in range(len(amenities_list)):
                    item = form.cleaned_data[amenities_list[i]]
                    if item:
                        amenities_text += amenities_list[i]
                        amenities_text += ','
                amenities_text = amenities_text[:-1]

                listing.amenities = amenities_text
                listing.save()
                return HttpResponseRedirect(reverse('scene'))
    else:
        if 'listing_id' in request.session:
            listing_id = request.session['listing_id']
            listing = models.Listing.objects.get(pk=listing_id)
            amenities_text = {}
            if listing.amenities is not None:
                for item in listing.amenities.split(','):
                    amenities_text[item] = True
                amenitiesForm = forms.AmenitiesForm(initial=amenities_text)
            else:
                amenitiesForm = forms.AmenitiesForm()
        else:
            amenitiesForm = forms.AmenitiesForm()
        return render(request, 'listingAdd/amenities.html', locals())


def scene(request):
    listing_id = request.session['listing_id']
    sceneFileForm = forms.SceneFileForm()
    if request.method == 'POST':
        pics = request.FILES.getlist('file')
        for pic in pics:
            pt = models.Scene()
            pt.listing_id = listing_id
            url = os.path.join(MEDIA_ROOT, pic.name)
            with open(url, 'w+b') as f:
                for data in pic.chunks():
                    f.write(data)
            pt.picture = "pictures/" + pic.name
            pt.save()
        return HttpResponseRedirect(reverse('scene'))
    else:
        pictures = []
        res = models.Scene.objects.filter(listing_id=listing_id)
        if res:
            for item in res:
                pictures.append((item.id, item.picture))
        return render(request, 'listingAdd/scene.html', locals())


def description(request):
    if request.method == 'POST':
        form = forms.DescriptionForm(request.POST)
        if form.is_valid():
            listing_id = request.session['listing_id']
            listing = models.Listing.objects.get(pk=listing_id)
            listing.name = form.cleaned_data['name']
            listing.summary = form.cleaned_data['summary']
            listing.neighborhood = form.cleaned_data['neighborhood']
            listing.transit = form.cleaned_data['transit']
            listing.save()
            return HttpResponseRedirect(reverse('location'))
    else:
        if 'listing_id' in request.session:
            listing_id = request.session['listing_id']
            listing = models.Listing.objects.get(pk=listing_id)
            desForm = forms.DescriptionForm(initial={
                "name": listing.name,
                "summary": listing.summary,
                "neighborhood": listing.neighborhood,
                "transit": listing.transit
            })
        else:
            desForm = forms.DescriptionForm()
        return render(request, 'listingAdd/description.html', locals())


def location(request):
    default_lat = -33.9163798
    default_lng = 151.2325216
    if request.method == 'POST':
        listing_id = request.session['listing_id']
        listing = models.Listing.objects.get(pk=listing_id)

        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        listing.latitude = latitude
        listing.longitude = longitude

        g = geocoder.google([str(latitude), str(longitude)], method='reverse', key=googlekey)
        print(g.address)
        if g.ok:
            print('success')
            listing.city = g.city
            listing.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "listingAdd/location.html", {'lat': default_lat, 'lng': default_lng})
    else:
        listing_id = request.session['listing_id']
        listing = models.Listing.objects.get(pk=listing_id)
        if listing.latitude and listing.longitude:
            default_lat = listing.latitude
            default_lng = listing.longitude
        return render(request, "listingAdd/location.html", {'lat': default_lat, 'lng': default_lng})


def listingInfo(request, listing_id):
    listing = models.Listing.objects.get(pk=listing_id)
    pictures = models.Scene.objects.filter(listing_id=listing_id)
    l = []
    for item in listing.amenities.split(','):
        l.append(item)
    total = {'name': listing.name, 'city': listing.city, 'price': listing.price, 'amenities': l}
    if pictures.exists():
        total['picture'] = pictures[0].picture
    return render(request, 'listingInfo.html', {'listing_id': listing_id, 'total': total})


def logout(request):
    auth.logout(request)
    return redirect('/index/')


def search(request):
    if request.method == 'GET':
        return HttpResponseRedirect('/index/')

    guests = 0
    results = []
    request.session['role'] = "guest"

    if request.method == 'POST':
        location = request.POST.get('where')
        check_in = request.POST.get('check-in')
        check_out = request.POST.get('check-out')
        guest_num = request.POST.get('guests')

        request.session['check_in'] = check_in
        request.session['check_out'] = check_out
        request.session['guest_num'] = guest_num

        if guest_num == "1 guest":
            guests = 1
        elif guest_num == "2 guests":
            guests = 2
        elif guest_num == "3 guests":
            guests = 3
        res = models.Listing.objects.filter(city__icontains=location, accommodates__gte=guests)

        for item in res:
            if check(check_in, check_out, item.id):
                pic_url = models.Scene.objects.filter(listing_id=item.id)[0].picture
                results.append({"id": item.id, "url": pic_url, "name": item.name, "price": item.price})

        return render(request, 'searchList.html', {'results': results, 'number': len(results)})


def check(check_in, check_out, listing_id):
    bookings = models.Booking.objects.filter(listing_id=listing_id)
    check_in = check_in.split('-')
    check_out = check_out.split('-')

    for item in bookings:
        start = datetime.datetime(int(check_in[2]), int(check_in[1]), int(check_in[0]))
        end = datetime.datetime(int(check_out[2]), int(check_out[1]), int(check_out[0]))
        pre_in = str(item.check_in).split('-')
        pre_out = str(item.check_out).split('-')
        pre_in = datetime.datetime(int(pre_in[0]), int(pre_in[1]), int(pre_in[2]))
        pre_out = datetime.datetime(int(pre_out[0]), int(pre_out[1]), int(pre_out[2]))
        if end <= pre_in or start >= pre_out:
            continue
        else:
            return False
    return True


def booking(request, listing_id):
    check_in = request.session['check_in'].split('-')
    check_out = request.session['check_out'].split('-')
    guests = request.session['guest_num']
    res = models.Listing.objects.get(pk=listing_id)

    start = datetime.datetime(int(check_in[2]), int(check_in[1]), int(check_in[0]))
    end = datetime.datetime(int(check_out[2]), int(check_out[1]), int(check_out[0]))
    total_days = (end - start).days

    if total_days < 1:
        total_days = 1

    total_price = res.price * total_days

    check_in = check_in[2] + "-" + check_in[1] + "-" + check_in[0]
    check_out = check_out[2] + "-" + check_out[1] + "-" + check_out[0]

    if request.method == 'GET':
        return render(request, 'bookingConfirm.html', {'listing_id': listing_id, 'name': res.name, 'guests': guests,
                        'check_in': check_in, 'check_out': check_out, 'total_price': total_price})
    else:
        new_booking = models.Booking()
        new_booking.listing_id = listing_id
        new_booking.check_in = check_in
        new_booking.check_out = check_out
        new_booking.guest_id = request.user.id
        new_booking.total_price = total_price
        new_booking.save()

        return HttpResponseRedirect(reverse('index'))


def bookingHistory(request):
    user_id = request.user.id
    bookings = models.Booking.objects.filter(guest_id=user_id)

    res = []

    for item in bookings:
        listing = models.Listing.objects.get(pk=item.listing_id)

        res.append({'name': listing.name, 'check_in': item.check_in, 'check_out': item.check_out,
                    'price': item.total_price})

    return render(request, 'history.html', {'results': res})






