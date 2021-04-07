from django.shortcuts import render,HttpResponseRedirect
from django.views import generic
from .models import Blog
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse,reverse_lazy
from .models import Blog,Likes
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.conf import settings

def blog_list(request):
    return render(request,'App_Blog/blog_list.htm')


class MyBlogs(LoginRequiredMixin,generic.TemplateView):
    redirect_field_name = 'App_Blog:my_blog'
    template_name = 'App_Blog/my_blogs.htm'

class UpdateBlog(LoginRequiredMixin,generic.UpdateView):
    model = Blog
    template_name = 'App_Blog/edit_blog.htm'
    fields = ('blog_title','blog_content','blog_image',)

    def get_success_url(self,**kwargs):
        return reverse_lazy('App_Blog:blog_details',kwargs={'slug':self.object.slug})


class CreateBlog(LoginRequiredMixin,generic.CreateView):
    model = Blog
    redirect_field_name = 'App_Blog:create_blog'
    template_name = 'App_Blog/create_blog.htm'
    fields = ('blog_title','blog_content','blog_image',)
    
    def form_valid(self,form):
        blog_obj = form.save(commit=False)
        blog_obj.author = self.request.user
        blog_obj.save()
        return HttpResponseRedirect(reverse('index'))

class BlogList(generic.ListView):
    context_object_name  = 'blogs'
    model = Blog
    template_name = 'App_Blog/blog_list.htm'

@login_required(login_url=settings.LOGIN_URL)
def blog_details(request,slug):
    blog = Blog.objects.get(slug=slug)
    comment_form = CommentForm()
    already_liked = Likes.objects.filter(blog=blog,user=request.user)

    if already_liked:
        liked = True
    else:
        liked = False    


    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            return HttpResponseRedirect(reverse('App_Blog:blog_details',kwargs={'slug':slug}))

    
    context = {
        'blog':blog,
        'comment_form':comment_form,
        'liked':liked,
    }    
    return render(request,'App_Blog/blog_details.htm',context)

@login_required
def liked(request,pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    already_liked = Likes.objects.filter(blog=blog,user=user)
    if not already_liked:
        liked_post = Likes(blog=blog,user=user)
        liked_post.save()
    return HttpResponseRedirect(reverse('App_Blog:blog_details',kwargs={'slug':blog.slug}))

@login_required
def unliked(request,pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    already_liked = Likes.objects.filter(blog=blog,user=user)
    already_liked.delete()
    return HttpResponseRedirect(reverse('App_Blog:blog_details',kwargs={'slug':blog.slug}))