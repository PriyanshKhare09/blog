from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment,Premium ,Profile
from .forms import PostForm, EditForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from datetime import date,datetime
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now


def like_view(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # return HttpResponseRedirect(reverse('article-detail', args=[str(pk)]))


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-date_time']
    

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['cat_menu'] = cat_menu
        return context
    

        
def search(request):
    if request.method == "POST":
        searched = request.POST['search']
        all_posts = Post.objects.filter(body__icontains=searched) or Post.objects.filter(title__icontains=searched)\
            or Post.objects.filter(author__first_name__icontains=searched) or Post.objects.filter(author__last_name__icontains=searched)
        return render(request, 'search.html', {'all_posts':all_posts})  

                
def category_view(request, cats):
    category_posts = Post.objects.filter(category=cats.replace('-',' '))
    return render(request, 'categories.html', {'category_posts':category_posts,'cats':cats.replace('-',' ')})


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article_details.html'
    
    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        val = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = val.total_likes()
        liked = False
        post_id = self.kwargs['pk']
        recently_viewed_posts = None
        
        if 'recently_viewed' in self.request.session:
            if post_id in self.request.session['recently_viewed']:
                self.request.session['recently_viewed'].remove(post_id)
            posts = Post.objects.filter(pk__in=self.request.session['recently_viewed'])
            recently_viewed_posts = sorted(posts, 
                    key=lambda x: self.request.session['recently_viewed'].index(x.id)
                    )
            
            self.request.session['recently_viewed'].insert(0, post_id)
            if len(self.request.session['recently_viewed']) > 5:
                self.request.session['recently_viewed'].pop()
        else:
            self.request.session['recently_viewed'] = [post_id]
        
        self.request.session.modified = True
            
        if val.likes.filter(id=self.request.user.id).exists():
            liked = True
        
        context['cat_menu'] = cat_menu
        context['total_likes'] = total_likes
        context['recently_viewed_posts'] = recently_viewed_posts
        context['liked'] = liked
        
        return context
    

def comment_post(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        c = request.POST['msg']
        user = str(request.user.first_name) + " " +str(request.user.last_name)
        td = date.today()
        post_data = Post.objects.get(id=pid)
        Comment.objects.create(name=user, content=c, post=post_data, created=td)
    return redirect('article-detail', pid)


class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'

def sub(req):
    return render(req,'subscription.html')


class AddCategoryView(CreateView):
    model = Category
    # form_class = PostForm
    template_name = 'add_category.html'
    fields = '__all__'


class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'update_post.html'


class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')

# def Premium_addPost(req):
#     check=Profile.objects.all()
#     context={'check':check}
#     return render(req,'base.html',context)

plan=Premium.objects.all()
context={'plan':plan}

def sub(req):
    return render(req,'subscription.html',context)

def payment(req,amout):
    Amount=amout
    contexts={'Amount':Amount}
    return render(req,'payment.html',contexts)


def success_payment(req):
    pre=Profile.objects.filter(user=req.user).first()
    pre.is_premium= True
    pre.premium_status= True
    current_date_time = now()
    pre.premium_expiry_date= current_date_time + relativedelta(months=1)
    pre.save()
    return redirect(reverse("home"))