from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import *
from django.core.exceptions import ValidationError
from django.contrib import messages

# Create your views here.

def home(request):
    claves_en_venta = Clave.objects.filter(en_venta=True, vendida=False)
    return render(request, 'home.html', {'claves': claves_en_venta})

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')
        print(request.POST)
        try:
            usuario = Usuario.objects.get(correo=correo, contraseña=contrasena)
            messages.success(request, f"Bienvenido {usuario.nombre}")
             # aqui se creara un diccionario para capturar los datos(variables de sesion) de inicio de sesion
            datos = {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "rol": usuario.rol
            }
             #aqui se crea directamente la variable de sesión
            request.session["drope"] = datos
            return redirect("home")
        except Usuario.DoesNotExist:
            print("usuario no existe")
            messages.error(request, "Usuario o contraseña no validos.")
            return redirect("login")


def logout(request):
    try:
        del request.session["drope"]
        return redirect("login")
    except:
        messages.error(request, "Error, algo paso :( ...")
        return redirect("home")

def registro(request):
    if request.method == 'GET':
        return render(request, 'registrar.html')
    else:
        if request.method == "POST":
                # Obtener datos del formulario
                correo = request.POST.get('correo')
                contraseña = request.POST.get('contrasena')
                nombre = request.POST.get('nombre')
                apellidos = request.POST.get('apellidos')
                fecha_nacimiento = request.POST.get('fecha_nacimiento')
                telefono_contacto = request.POST.get('telefono')
                acepto_terminos = request.POST.get('terminos') == 'on'
                rol = request.POST.get('rol')

                if Usuario.objects.filter(correo=correo).exists():
                    print("este usuario ya existe")
                    return render(request, 'registrar.html')
                else:
                    # Crear el usuario
                    usuario = Usuario(
                    correo=correo,
                    contraseña=contraseña,
                    nombre=nombre,
                    apellidos=apellidos,
                    fecha_nacimiento=fecha_nacimiento,
                    telefono_contacto=telefono_contacto,
                    acepto_terminos=acepto_terminos,
                    rol=rol
                    )
                    usuario.save()
                    datos = {
                        "id": usuario.id,
                        "nombre": usuario.nombre,
                        "rol": usuario.rol
                    }
                    #aqui se crea directamente la variable de sesión
                    request.session["drope"] = datos
                    return redirect("home")
    return render(request, 'home.html')

def perfil_usuario(request):
    if "drope" not in request.session:
        return redirect("login")

    datos_usuario = request.session["drope"]
    try:
        usuario = Usuario.objects.get(id=datos_usuario["id"])
    except Usuario.DoesNotExist:
        return redirect("login")

    return render(request, 'perfil_usu.html', {'usuario': usuario})

def editar_perfil(request):
    datos_sesion = request.session.get("drope")
    if not datos_sesion:
        return redirect("login")

    usuario = Usuario.objects.get(id=datos_sesion["id"])

    if request.method == "POST":
        usuario.nombre = request.POST.get("nombre")
        usuario.apellidos = request.POST.get("apellidos")
        usuario.telefono_contacto = request.POST.get("telefono")
        usuario.contraseña = request.POST.get("contrasena")
        usuario.save()

        # actualizar la variable de sesión
        request.session["drope"]["nombre"] = usuario.nombre
        return redirect("perfil_usu")

    return render(request, "edit_perfil.html", {"usuario": usuario})


def ver_claves_compradas(request):
    datos_sesion = request.session.get("drope")
    if not datos_sesion:
        return redirect("login")
    
    if datos_sesion["rol"] != "u":
        return HttpResponse("No tienes permiso para ver esta página.", status=403)

    usuario = Usuario.objects.get(id=datos_sesion["id"])
    compras = Compra.objects.filter(comprador=usuario).select_related("clave")

    return render(request, "claves_compra.html", {"compras": compras})


def publicar_clave(request):
    datos_sesion = request.session.get("drope")
    if not datos_sesion:
        return redirect("login")

    if datos_sesion["rol"] != "v":
        return HttpResponse("No tienes permiso para publicar claves.", status=403)

    usuario = Usuario.objects.get(id=datos_sesion["id"])

    if request.method == "POST":
        nombre_juego = request.POST.get("nombre_juego")
        genero = request.POST.get("genero")
        descripcion = request.POST.get("descripcion")
        precio = request.POST.get("precio")
        clave_juego = request.POST.get("clave_juego")
        terminos = request.POST.get("terminos") == "on"

        Clave.objects.create(
            nombre_juego=nombre_juego,
            genero=genero,
            descripcion=descripcion,
            precio=precio,
            clave_juego=clave_juego,
            terminos_y_condiciones=terminos,
            usuario=usuario,
            en_venta=True,
            vendida=False
        )

        messages.success(request, "Clave publicada exitosamente.")
        return redirect("perfil_usu")

    return render(request, "clave_publi.html")

def detalle_clave(request, clave_id):
    clave = get_object_or_404(Clave, id=clave_id)
    return render(request, 'clave_deta.html', {'clave': clave})

def ver_claves(request):
    claves = Clave.objects.all()
    return render(request, 'claves.html', {'claves': claves})

def mis_claves(request):
    usuario_id = request.session.get('drope', {}).get('id')  # Asegúrate de que este sea el ID del usuario en sesión
    usuario = Usuario.objects.get(id=usuario_id)
    
    if usuario.rol != 'v':
        return render(request, 'perfil_usu.html', {'mensaje': 'Acceso denegado'})

    claves = Clave.objects.filter(usuario=usuario)
    return render(request, 'mis_claves.html', {'claves': claves})