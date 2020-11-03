from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Place
from .forms import NewPlaceForm, TripReviewForm

# Create your views here.

@login_required
def place_list(request):
    
    if request.method == 'POST':
        form = NewPlaceForm(request.POST)
        place = form.save(commit=False)     # make Place object from form
        place.user = request.user           # assign a user to the place
        if form.is_valid():                 # validate form input
            place.save()                    # save Place to db
            return redirect('place_list')
    
    # if not POST, or if POST is invalid
    places = Place.objects.filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()
    return render(request, 'travel_wishlist/wishlist.html', { 'places': places, 'new_place_form': new_place_form })

@login_required
def places_visited(request):
    visited = Place.objects.filter(user=request.user).filter(visited=True).order_by('name')
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited })

@login_required
def place_was_visited(request, place_pk):
    
    if request.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk)
        
        # only allow users to modify their own places
        if place.user == request.user:
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()
    
    return redirect('place_list')

@login_required
def place_details(request, place_pk):
    
    place = get_object_or_404(Place, pk=place_pk)
    
    if place.user != request.user:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        
        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors)
        
        return redirect('place_details', place_pk=place_pk)
    
    else:
        if place.visited:
            
            # form will have data about this place already filled in
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form})
        
        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place})

@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    
    # only allow users to modify their own places
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()
