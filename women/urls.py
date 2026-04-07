from django.urls import path, register_converter

from . import converters, views

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path("", views.WomenHome.as_view(), name="home"),
    path("about/", views.about, name="about"),
    path("addpage/", views.AddPage.as_view(), name="add_page"),
    path("contact/", views.contact, name="contact"),
    path("login/", views.login_view, name="login"),
    path("post/<slug:post_slug>/", views.ShowPost.as_view(), name="post"),
    path("edit/<int:pk>/", views.UpdatePage.as_view(), name="edit_page"),
    path("category/<slug:cat_slug>/", views.WomenCategory.as_view(), name="category"),
    path("tag/<slug:tag_slug>/", views.ShowTagPost.as_view(), name="tag"),
]
