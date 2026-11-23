from django.urls import path
from myapp import views

urlpatterns = [
    path("",views.home,name="home"),
    path("about/",views.about,name="about"),
    path("contact/",views.contact,name="contact"),
    path("register/",views.register,name="register"),
    path("dashboard/",views.dashboard,name="dashboard"),
    path("update/<int:pk>/",views.update,name="update"),
    path("delete/<int:pk>/",views.delete,name="delete"),
    path("login/",views.login,name="login"),
    path("product/",views.product,name="product"),
    path("validate/",views.validate,name="validate"),
    path("update_list/<int:pk>/",views.update_list,name="update_list"), 
    path("profile",views.profile,name="profile"),
    path("logout/",views.login,name="logout"),
    path("student/",views.StudentList.as_view(),name="student")
]