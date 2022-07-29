
from cgitb import lookup
from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('categories',views.CategoryViewSet)
router.register('orders',views.OrderViewSet)
router.register('services',views.ServiceViewSet)



orders_router = routers.NestedDefaultRouter(router,'orders', lookup='order')
orders_router.register('items', views.OrderItemViewSet, basename='order-items')

service_router = routers.NestedDefaultRouter(router,'services',lookup='service')
service_router.register('items', views.ServiceItemViewSet, basename='service-items')


urlpatterns = router.urls + orders_router.urls + service_router.urls