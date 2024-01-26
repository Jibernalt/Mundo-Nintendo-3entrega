
from django.urls import path, include

from .views import SignUpView
from .views import ProductoViewSet, VentaViewSet, DetalleVentaViewSet

from rest_framework.routers import DefaultRouter
from .views import listar_productos
from .views import crear_producto
from .views import listar_catalogo
from .views import comprar_producto
from .views import lista_ventas_cliente
from .views import editar_producto
from .views import eliminar_producto

router = DefaultRouter()
router.register('productos', ProductoViewSet, basename='producto')
router.register('ventas', VentaViewSet, basename='venta')
router.register('detalles-ventas', DetalleVentaViewSet, basename='detalleventa')

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('api/', include(router.urls)),
    path('listar_productos/', listar_productos, name='listar_productos'),
    path('crear_producto/', crear_producto, name='crear_producto'),
    path('editar-producto/<int:pk>/', editar_producto, name='editar_producto'),
    path('eliminar_producto/<int:pk>/', eliminar_producto, name='eliminar_producto'),
    path('catalogo/', listar_catalogo, name='catalogo'),
    path('comprar_producto/<int:producto_id>/', comprar_producto, name='comprar_producto'),
    path('ventas/', lista_ventas_cliente, name='lista_ventas_cliente'),

]