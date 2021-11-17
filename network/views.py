from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from .models import User, Posts, UserDetails, Likes
from django.core.paginator import Paginator


def index(request):

    posts = Posts.objects.all()
    posts = posts.order_by("-date").all()
    paginator = Paginator(posts, 10)  # Show 5 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    icon_state = Likes.objects.all()
    return render(request, "network/index.html", {'page_obj': page_obj, 'icon_state': icon_state})


# Function to get the post to be edited.
def edit_post(request, id):
    global p_edit
    p_edit = id
    post = Posts.objects.get(id=id)
    return render(request, "network/edit_post.html", {"post": post})


# Function to do actual editing.
@csrf_exempt
def edit_post1(request):
    id = p_edit
    if request.method == 'PUT':
        data = json.loads(request.body)

        p = Posts.objects.get(id=id)
        p.post = data.get('posts')
        p.save()
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=403)


def user_details(request, name):
    posts = Posts.objects.filter(name=name)
    posts = posts.order_by("-date").all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get details
    detail = UserDetails.objects.filter(name=name)
    ct = 0
    cp = 0
    btn_value = 'follow'
    for i in detail:
        followers = i.followers
        following = i.following
        if followers == request.user.username:
            btn_value = 'unfollow'
        if followers != 'names':
            ct += 1
        if following != 'names':
            cp += 1

    return render(request, "network/user_details.html", {'page_obj': page_obj, 'name': name,
                                                         'followers': ct, 'following': cp, 'btn_value': btn_value})


def following(request):
    name = request.user.username
    obj_list = []
    p = UserDetails.objects.filter(name=name)
    for u in p:
        post = Posts.objects.filter(name=u.following)
        for a in post:
            obj_list.append(a)

    paginator = Paginator(obj_list, 10)  # Show 5 posts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {'page_obj': page_obj})


@csrf_exempt
def post(request):
    user = request.user.username
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    if request.method == "POST":

        # Get data from the post
        data = json.loads(request.body)
        post = data.get("post", "")

        posts = Posts(name=user, post=post, date=timezone.now())
        posts.save()
        messages.success(request, "Posted successfully.")
        return JsonResponse({"message": "Post sent successfully."}, status=201)
    return HttpResponse(user)


def all_posts(request, name):

    if name == request.user.username:
        obj_list = []
        p = UserDetails.objects.filter(name=name)
        for u in p:
            post = Posts.objects.filter(name=u.following)
            for a in post:
                obj_list.append(a)

        return JsonResponse([posts.serialize() for posts in obj_list],  safe=False)
    else:
        posts = Posts.objects.all()
        posts = posts.order_by("-date").all()
        return JsonResponse([post.serialize() for post in posts], safe=False)


@csrf_exempt
def details(request, name):

    if request.method == 'PUT':
        data = json.loads(request.body)
        if data.get("followers") is not None:
            followers = request.user.username

            if 'u' in data['btn']:

                UserDetails.objects.get(name=followers, following=name).delete()
                UserDetails.objects.get(name=name, followers=followers).delete()

            else:
                # Check if the user is a follower already.
                check = UserDetails.objects.filter(name=name, followers=followers)
                if not check:
                    follow = UserDetails(name=name, followers=followers)
                    follow.save()

                    following = UserDetails(name=followers, following=name)
                    following.save()
                else:
                    return HttpResponse(status=400)
            return HttpResponse(status=204)
    else:

        user_details = UserDetails.objects.filter(name=name)
        return JsonResponse([details.serialize() for details in user_details],  safe=False)


@csrf_exempt
def like_unlike(request, id):
    # Get the specific post.
    item = Posts.objects.get(id=id)
    name = request.user.username
    if request.method == 'PUT':
        data = json.loads(request.body)

        # Get the state of the like icon
        state = data.get('state')

        user_id = User.objects.get(username=name)
        if state == 'down':
            check = Likes.objects.filter(liked_by=user_id, liked_post=item)
            # if the user have not liked the post before
            if not check:
                Likes.objects.create(liked_by=user_id, liked_post=item)
                item.likes = Likes.objects.filter(liked_post=item).count()
                item.state = 'down'
                item.liked_by = name

        else:
            Likes.objects.filter(liked_by=user_id, liked_post=item).delete()
            item.likes = 0
            item.likes = Likes.objects.filter(liked_post=item).count()
            item.state = 'up'
            item.liked_by = ''

        item.save()
        return HttpResponse(status=204)
    if request.method == 'GET':
        item = Posts.objects.get(id=id)
        print(item.likes)
        return JsonResponse(item.serialize())


def user_posts(request, name):
    post = Posts.objects.filter(name=name)
    post = post.order_by('-date').all()
    return JsonResponse([posts.serialize() for posts in post], safe=False)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
