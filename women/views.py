from typing import Any

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseNotFound,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.functional import cached_property
from django.views import View
from django.views.generic import (
    CreateView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
)

import women
from women.utils import DataMixin

from .forms import AddPostForm, UploadFileForm
from .models import Category, TagPost, UploadFiles, Women
from .utils import menu


class WomenHome(DataMixin, ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    title_page = "Главная страница"
    cat_selected = 0

    def get_queryset(self) -> QuerySet:
        return Women.published.all().select_related("cat")

@login_required
def about(request: HttpRequest) -> HttpResponse:
    contact_list = Women.published.all()
    paginator = Paginator(contact_list, 3)
    page_num = request.GET.get("page")
    page_obj = paginator.get_page(page_num)
    data = {
        "title": "О сайте",
        "menu": menu,
        "page_obj": page_obj,
        }
    return render(request, "women/about.html", data)


def contact(request: HttpRequest) -> HttpResponse:
    data = {
        "title": "Контакты",
        "menu": menu,
        }
    return render(request, "women/contact.html", data)


class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = "women/addpage.html"
    title_page = "Добавление статьи"
    permission_required = "women.add_women"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)
    
    
class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Women
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = "women/addpage.html"
    title_page = "Добавление статьи"
    permission_required = "women.change_women"


def login_view(request):
    return HttpResponse("Авторизация")


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = "women/post.html"
    slug_url_kwarg = "post_slug"
    context_object_name = "post"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context["post"].title)
    
    def get_object(self, queryset=None) -> Any:
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


class WomenCategory(DataMixin, ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    
    def get_queryset(self) -> QuerySet:
        return Women.published.filter(cat__slug=self.kwargs["cat_slug"]).select_related("cat")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=self.kwargs["cat_slug"])
        return self.get_mixin_context(
            context,
            title=f"Категория - {category.name}",
            cat_selected = category.pk            
            )


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Cтраница не найдена</h1>")


class ShowTagPost(DataMixin, ListView):
    template_name = "women/index.html"
    context_object_name = "posts"

    @cached_property
    def tag(self):
        return get_object_or_404(TagPost, slug=self.kwargs["tag_slug"])
    
    def get_queryset(self) -> QuerySet:
        return self.tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related("cat")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            title=f"Тег: {self.tag.tag}"
            )