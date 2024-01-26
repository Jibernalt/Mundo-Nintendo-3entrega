from django.shortcuts import render, redirect

# Create your views here.
# accounts/views.py
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.edit import FormView
from .forms import CustomUserCreationForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .forms import ProductoForm


from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.http import JsonResponse

from .models import Producto, Venta, DetalleVenta
from .serializers import ProductoSerializer, VentaSerializer, DetalleVentaSerializer

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

class DetalleVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer
    
def listar_productos(request):
    # Obtén todos los productos desde la base de datos
    productos = Producto.objects.all()

    # Pasa los productos a la plantilla
    return render(request, 'producto_list.html', {'productos': productos})

def listar_catalogo(request):
    # Obtén todos los productos desde la base de datos
    productos = Producto.objects.all()

    # Pasa los productos a la plantilla
    return render(request, 'productos.html', {'productos': productos})

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

    else:
        form = ProductoForm()
    # Recupera todos los productos
    productos = Producto.objects.all()
    
    return render(request, 'agregar.html', {'form': form, 'productos': productos})

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Producto, DetalleVenta, Venta

@login_required
def comprar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    usuario = request.user

    venta_abierta = Venta.objects.filter(usuario=usuario, total_venta=0).first()

    if not venta_abierta:
        venta_abierta = Venta.objects.create(usuario=usuario)

    detalle_venta_existente = DetalleVenta.objects.filter(venta=venta_abierta, producto=producto).first()

    if detalle_venta_existente:
        detalle_venta_existente.cantidad += 1
        detalle_venta_existente.save()
    else:
        DetalleVenta.objects.create(venta=venta_abierta, producto=producto)

    venta_abierta.total_venta = sum(detalle.subtotal for detalle in venta_abierta.detalles.all())
    venta_abierta.save()

    producto.cantidad -= 1
    producto.save()
    
    messages.success(request, 'Compra exitosa. Gracias por tu compra!')


    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('crear_producto')  # Reemplaza 'lista_productos' con el nombre de tu vista de lista de productos
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'editar_producto.html', {'form': form, 'producto': producto})

@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        # Si la solicitud es un POST, elimina el producto y redirige a la lista de productos.
        producto.delete()
        return redirect('crear_producto')

    return render(request, 'eliminar_producto.html', {'producto': producto})

@login_required
def lista_ventas_cliente(request):
    # Obtén las ventas del cliente actual (usando la relación ForeignKey)
    ventas_cliente = Venta.objects.filter(usuario=request.user)

    # Puedes personalizar esta vista según tus necesidades, por ejemplo, agregar más información
    return render(request, 'carrito.html', {'ventas_cliente': ventas_cliente})