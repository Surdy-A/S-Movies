from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Rating, Season, Comment, Review
from .forms import CommentForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
# from views  import 

def MovieHome(request):
    latestMovies = ''
    if Movie.objects.count() > 0:
        latestMovies = Movie.objects.order_by('-created_at')[:5] 
        #latestMovies = Movie.objects.latest('created_at')
        
    nollyWoodMovies = GetMovieCategory("Nolly")
    nollyWoodMoviesSeries = GetMovieCategory("Nolly-S")
    hollyWoodMovies = GetMovieCategory("Holly")
    hollyWoodMoviesSeries = GetMovieCategory("Holly-S")
    foreign = GetMovieCategory("FOR")
    korean = GetMovieCategory("KOR")
    return render(request, "movie-homepage.html", {"latestMovies": latestMovies, 
                                                   'nollyWoodMoviesList':nollyWoodMovies[:6],
           
                                        'nollyWoodMoviesSeriesList':nollyWoodMoviesSeries[:6],
                                                   'hollyWoodMoviesList':hollyWoodMovies[:6],
                                                   'hollyWoodMoviesSeriesList':hollyWoodMoviesSeries[:6],
                                                   'foreignList':foreign[:6],
                                                   'koreanList':korean})


    

def GetMovieCategory(category):
    nollyWoodObj=Movie(categories=category)
    nollyWood = nollyWoodObj.categories
    # nollywoodMovies = nollyWoodObj.get_categories_display()
    movieCategory = Movie.objects.filter(categories=nollyWood)
    return movieCategory


from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.utils import timezone
from .models import Movie, Comment
from .forms import CommentForm

from django.http import JsonResponse

def movie_detail(request, id):
    movie = get_object_or_404(Movie, id=id)
    ratings = movie.ratings.all()
    average_rating = movie.average_rating()

    if request.method == "POST":
        # Handle Like Button Click
        if request.POST.get("action") == "like_comment":
            comment_id = request.POST.get("comment_id")
            comment = get_object_or_404(Comment, id=comment_id)
            comment.likes += 1
            comment.save()

            return JsonResponse({"likes": comment.likes})  # ✅ Ensure JSON Response

        # Otherwise, process comment submission
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.movie = movie
            comment.created_at = timezone.now()
            comment.save()
            return redirect('movies:movie_detail', id=movie.id)

    else:
        form = CommentForm()

    comments = Comment.objects.filter(movie=movie).order_by('-created_at')

    return render(request, "movie_detail.html", {
        "movie": movie,
        "ratings": ratings,
        "average_rating": average_rating,
        "form": form,
        "comments": comments,
})




def movie_list(request, cat):
    if cat == "Nolly":
        movies = GetMovieCategory("Nolly")
        categoryName = "Nollywood"
    elif cat == "Nolly-S":
        movies = GetMovieCategory("Nolly-S")
        categoryName = "Nollywood Series"
    elif cat == "Holly":
        movies = GetMovieCategory("Holly")
        categoryName = "Hollywood"
    elif cat == "Holly-S":
        movies = GetMovieCategory("Holly-S")
        categoryName = "Hollywood Series"
    elif cat == "FOR":
        movies = GetMovieCategory("FOR")
        categoryName = "Foreign"
    elif cat == "KOR":
        movies = GetMovieCategory("KOR")
        categoryName = "Korean"

    else:
        "No Movies Correspond to this category"
        categoryName = "No Corresponding"
        movies = Movie.objects.none()
    
    return render(request, 'movie_list.html', {"movies":movies, "category":categoryName})


def series_movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    seasons = Season.objects.filter(movie=movie).prefetch_related("episodes")
    return render(request, "series_movie_detail.html", {"movie": movie, "seasons": seasons})

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)



@login_required
def movie_reviews(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = Review.objects.filter(movie=movie).order_by('-created_at')
    comments = movie.comments.all().order_by('-created_at')
     # Get parent comments for the logged-in user
    parent_comments = [comment for comment in comments if comment.is_parent() and comment.user == request.user]

    print(movie)
    print(reviews)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        rating = request.POST.get('rating')

        print("Received Data:", request.POST)  # Debugging: Check what data is received
        print("Received Data:", title, content, rating)  # Debugging: Check what data is received


        if not title or not content or not rating:
            messages.error(request, "All fields are required!")
            return redirect('movie_reviews', movie_id=movie.id)

        try:
            rating = float(rating)  # Ensure rating is a number
        except ValueError:
            messages.error(request, "Invalid rating value.")
            return redirect('movie_reviews', movie_id=movie.id)

        # Save the review
        Review.objects.create(
            user=request.user,
            movie=movie,
            title=title,
            content=content,
            rating=rating
        )

        messages.success(request, "Review added successfully!")
        return redirect('movie_reviews', movie_id=movie.id)
            
    return render(request, 'movie_reviews.html', {'movie': movie, 'reviews': reviews, "parent_comments": parent_comments})


def search_movies(request):
    query = request.GET.get('q', '')
    movies = Movie.objects.filter(title__icontains=query) if query else Movie.objects.all()

    return render(request, 'search_results.html', {'movies': movies, 'query': query})


@login_required
def rate_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == "POST":
        score = int(request.POST.get("score"))
        rating, created = Rating.objects.update_or_create(
            user=request.user, movie=movie, defaults={"score": score}
        )
        return redirect("movie_detail", movie_id=movie.id)

    return render(request, "rate_movie.html", {"movie": movie})

# def comment_view(request, id):
#     movie = get_object_or_404(Movie, id=id)
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.user = request.user
#             comment.save()
#             return redirect('movie_detail', movie_id=movie.id)
#         print(form)
#     else:
#         form = CommentForm()
#     comments = Comment.objects.all().order_by('-created_at')
#     return render(request, 'movie_detail.html', {'form': form, 'comments': comments})                                                                                                                                                                                                                          

def check_parent_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
        if comment.user == request.user and comment.is_parent():
            return True
        return False
    except Comment.DoesNotExist:
        return False
