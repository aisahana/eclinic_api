
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from medicines.views import MedicineViewSet, RecipeViewSet, RecipeItemViewSet
from orders.views import RegisterViewSet
from payments.views import PaymentViewSet
from polyclinics.views import PolyViewSet
from users.views import CustomAuthToken, DoctorViewSet, PatientViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', CustomAuthToken.as_view()),
]

router = DefaultRouter()
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'polys', PolyViewSet, basename='poly')
router.register(r'medicines', MedicineViewSet, basename='medicine')
router.register(r'registers', RegisterViewSet, basename='register')
router.register(r'recipes', RecipeViewSet, basename='recipe')
router.register(r'recipe-items', RecipeItemViewSet, basename='recipe-item')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns += router.urls
