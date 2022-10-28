from django.contrib import admin
from django.urls import path
from tareas import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('tareas/', views.tasks, name='tareas'),
    path('tareascompleto/', views.tasksCompleto, name='tareasCompleto'),
    path('tareas/crear/', views.crearTareas, name='creartareas'),
    path('tareas/<int:idt>/', views.detalleTarea, name='detalleTarea'),
    path('tareas/<int:idt>/completo/', views.completo, name='completo'),
    path('tareas/<int:idt>/borrar/', views.borrar, name='borrar'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
]
