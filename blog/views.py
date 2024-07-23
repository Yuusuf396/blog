from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render,get_object_or_404
from .models import Posts
from django.views.generic import CreateView,ListView,DetailView
from django.views import View
from .forms import CommentForm
 
# Create your views here.




def starting_page(request):
    latest_posts=Posts.objects.all().order_by('-date')[:3]
   
    return render(request, "blog/index.html",{
        "posts":latest_posts
    })
    # pass
    
class StartingPageView(ListView):
    model=Posts
    template_name="blog/index.html"
    context_object_name="posts"
    ordering=["-date"]
    def get_queryset(self) -> QuerySet[Any]:
        queryset= super().get_queryset()
        data=queryset[:3]
        return data

class PostsListView(ListView):
    model=Posts
    template_name="blog/all-posts.html"
    context_object_name="all_posts"
    ordering=["-date"]

# def posts(request):
    
#     all_posts=Posts.objects.all().order_by('-date')
#     return render(request, "blog/all-posts.html",{
#         "all_posts":all_posts
#     })

class PostDetailView(View):
    model=Posts
    template_name="blog/post-detail.html"
    # context_object_name="post"
    def get(self,request,slug):
        post=Posts.objects.get(slug=slug)
        context={
            "posts":post,
            "post_tags":post.tag.all(),
            "comment_form":CommentForm(),
            "comments":post.comments.all().order_by("-id")
        }
        return render(request,"blog/post-detail.html",context)
    
    def post(self,request,slug):
        comment_form=CommentForm(request.POST)
        post=Posts.objects.get(slug=slug)
        if comment_form.is_valid():
            comment=comment_form.save(commit=False)
            comment.post=post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page",args=[slug]))
        
        context={
            "posts":post,
            "post_tags":post.tag.all(),
            "comment_form":comment_form,
            "comments":post.comments.all().order_by("-id")
        }
        return render(request,"blog/post-detail.html",context)

    # def get_context_data(self, **kwargs) :
    #     context= super().get_context_data(**kwargs)
    #     # post=get_object_or_404(Posts,slug=slug)
    #     # print(context)
    #     context["post_tags"]=self.object.tag.all()
    #     context["comment_form"]=CommentForm()
    #     return context

def post_detail(request, slug):
    identified_post=get_object_or_404(Posts,slug=slug)
    return render(request, "blog/post-detail.html",{
        "post":identified_post,
        'post_tags':identified_post.tag.all()
    })
