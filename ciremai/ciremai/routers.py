from rest_framework import routers
from billing.viewsets import PatientViewSet,ArticleViewSet

router = routers.DefaultRouter()

router.register(r'patient', PatientViewSet)
router.register(r'article', ArticleViewSet)