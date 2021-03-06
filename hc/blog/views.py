from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.models import Post
from blog.models import Tag
from blog.models import Page
from django.conf import settings
    

def index(request):
    #get the blog posts that are published
    tagParam = request.GET.get('tag')
    if tagParam:
        post_list = Post.objects.filter(published=True, tag__slug=tagParam)
    else:
        post_list = Post.objects.filter(published=True)
    paginator = Paginator(post_list,4) # Show 4 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        #If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        #If page is out of range, deliver last page of results
        posts = paginator.page(paginator.num_pages)
    for post in posts:
        post.tags = Tag.objects.filter(post__slug=post.slug)
    #find all published pages
    pages = Page.objects.filter(published=True)
    #now return the rendered template
    return render(request,'blog/index.html',{'posts':posts,'tagParam':tagParam,'pages':pages,'MEDIA_URL':settings.MEDIA_URL})

def page(request,slug):
    page = get_object_or_404(Page,slug=slug)
    #find all published pages
    pages = Page.objects.filter(published=True)
    return render(request,'blog/page.html',{'page':page,'pages':pages,'MEDIA_URL':settings.MEDIA_URL})

def post(request,slug):
    #get the Post object
    post = get_object_or_404(Post,slug=slug)
    post.tags = Tag.objects.filter(post__slug=post.slug)
    #find all published pages
    pages = Page.objects.filter(published=True)
    #now return the rendered template
    return render(request,'blog/post.html',{'post':post,'pages':pages,'MEDIA_URL':settings.MEDIA_URL})
