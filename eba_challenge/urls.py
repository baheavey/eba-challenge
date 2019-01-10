"""eba_challenge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import register_converter, path
from challenge import views, converters

# Relies on NegativeIntConverter class in converters.py stored in challenges directory
# Negative number solution found here: https://stackoverflow.com/questions/48867977/django-2-url-path-matching-negative-value
register_converter(converters.NegativeIntConverter, 'negint')

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('scorecard/<int:challenge_id>/<str:email>', views.daily_tracker),
    path('scorecard/<int:challenge_id>/<str:email>/<int:offset>', views.daily_tracker),
    path('scorecard/<int:challenge_id>/<str:email>/<negint:offset>', views.daily_tracker),
]
