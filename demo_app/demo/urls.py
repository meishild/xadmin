import xadmin
from demo_app.app import views
from django.conf.urls import url, include
from rest_framework import routers
from xadmin.plugins import xversion

xversion.register_models()

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    url(r'^admin/', include(xadmin.site.urls)),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^', include(router.urls)),
]
