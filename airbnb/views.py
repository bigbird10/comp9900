from django.shortcuts import render, redirect
from . import forms, models
from django.contrib import auth
from comp9900.settings import MEDIA_ROOT
from django.http import HttpResponseRedirect
from django.urls import reverse
import os
import geocoder

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

    if request.method == 'GET':
        if request.user and request.user.is_authenticated:
            listings = []
            temp = models.Listing.objects.filter(host_id=request.user.id)
            if temp.exists():
                for item in temp:
                    listings.append((item.id, item.city))
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
                        listings.append((item.id, item.city))
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
                "Bathrooms": listing.bathrooms
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

        g = geocoder.google([str(latitude), str(longitude)], method='reverse')
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


def calendar(request):
    pass


def logout(request):
    auth.logout(request)
    return redirect('/index/')


def search(request):
    pass
    '''if request.method == 'GET':
        return redirect('/index/')

    if request.method == 'POST':
        location = request.POST.get('where')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        guest_num = request.POST.get('guests')
        '''