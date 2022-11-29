from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("categories", views.categories, name="categories"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("watchlistRemove/<int:id>", views.watchlistRemove, name="watchlistRemove"),
    path("watchlistAdd/<int:id>", views.watchlistAdd, name="watchlistAdd"),
    path("watchlist", views.watchlist, name="watchlist")
]
