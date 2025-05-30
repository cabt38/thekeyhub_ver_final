"""
URL configuration for proyec_keyhub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from prinkeyhub import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('registro/', views.registro, name="registro"),
    path('key/', views.registro, name="publikey"),
    path('perfil/', views.perfil_usuario, name='perfil_usu'),
    path('editar_perfil/', views.editar_perfil, name='edit_perfil'),
    path('ver_claves/', views.ver_claves_compradas, name='claves_compra'),
    path('clave_publi/', views.publicar_clave, name='clave_publi'),
    path('clave_deta/<int:clave_id>/', views.detalle_clave, name='clave_deta'),
    path('claves/', views.ver_claves, name='claves'),
    path('mis_claves/', views.mis_claves, name='mis_claves')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)