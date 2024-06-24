from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404
from .models import  Profile, Land ,Transaction,Listing
from .models import Listing
from django.contrib.auth import authenticate

def index(request):

  
    return render(request,"product/home.html", {})


def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        full_names = request.POST['full_names']
        whats_number = request.POST['whats_number']
        address = request.POST['address']
        county = request.POST['county']

        if not (username and email and password and full_names and whats_number and address and county):
            message = "Please fill in all the fields."
            return render(request, 'product/signup.html', {'message': message})
        
        if User.objects.filter(username=username).exists():
            message = "Username already exists."
            return render(request, 'product/signup.html', {'message': message})

        if User.objects.filter(email=email).exists():
            message = "Email already exists."
            return render(request, 'product/signup.html', {'message': message})

        user = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.create(
                user=user,
                full_names=full_names,
                whats_number=whats_number,
                address=address,
                county=county
            )


       
     
        login(request, user)

        return redirect('profile')

    return render(request, 'product/signup.html')

def login_view(request):
   
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:

            
              message = "Invalid username or password."

    return render(request, 'product/login.html', {})



def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    
    # Redirect to  the login page
    return redirect('login')  

@login_required(login_url='auth')
def profile(request):
    user_profile = Profile.objects.get(user=request.user)
    user_listings = Listing.objects.filter(created_by=request.user)
    user_transactions = Transaction.objects.filter(buyer=user_profile) | Transaction.objects.filter(seller=user_profile)
    owned_lands = Land.objects.filter(owner=user_profile)

    context = {
        'user_profile': user_profile,
        'user_listings': user_listings,
        'user_transactions': user_transactions,
        'owned_lands': owned_lands,
    }
    return render(request, 'product/profile.html', context)

    
    
    



def land_listings(request):
    listings = Listing.objects.filter(is_active=True).select_related('land')
    return render(request, 'product/lands.html', {'listings': listings})


def checkout(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    seller_profile = get_object_or_404(Profile, user=listing.created_by)
    return render(request, 'product/checkout.html', {'listing': listing, 'seller_profile': seller_profile})





def about(request):
   

    return render(request,"product/about.html", {})



@login_required
def add_land_view(request):
    if request.method == "POST":
        title_deed = request.POST.get('title_deed')
        price = request.POST.get('price')
        location = request.POST.get('location')
        county = request.POST.get('county')
        size = request.POST.get('size')
        description = request.POST.get('description')
        image = request.FILES.get('image')


        land = Land(
            title_deed=title_deed,
            price=price,
            location=location,
            owner= Profile.objects.get(user=request.user),
            county=county,
            size=size,
            description=description,
            image=image
        )
        land.save()
        return redirect('profile')  # Redirect to the listings page after saving

    profiles = Profile.objects.all()
    username=request.user
    return render(request, 'product/add_land.html', {'profiles': profiles,'username': username})




@login_required
def add_listing_view(request):
    if request.method == "POST":
        land_id = request.POST.get('land')
        is_active = request.POST.get('is_active') == 'True'
        
        land = Land.objects.get(id=land_id)

        listing = Listing(
            land=land,
            created_by=request.user,
            is_active=is_active
        )
        listing.save()
        return redirect('profile')  # Redirect to the listings page after saving

    lands = Land.objects.all()
    return render(request, 'product/add_listing.html', {'lands': lands})