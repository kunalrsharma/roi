from django.urls import path, include
from django.contrib import admin

admin.autodiscover()

import hello.views
import hello.polls
import hello.jobs

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", hello.views.index, name="index"),
    path("jobs/", hello.jobs.index, name="jobs"),
    path("polls/", hello.polls.index, name="polls"),
    path("admin/", admin.site.urls),
]
