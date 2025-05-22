from django.db import models

#Se tendran 3 modelos principales, Modelo Usuario, Modelo Clave y Modelo Compra

#En el modelo Usuarios se tendran dos roles para tener un mejor control y una mejor optimizacion en las vistas y los .html; estos dos roles son: Usuario y Vendedor, ya los campos son datos comunes que se le pediran a cualquier usuario que se quiera registrar

class Usuario(models.Model):
    ROLES = (
        ('u', 'Usuario'),
        ('v', 'Vendedor'),
    )

    correo = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=128)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    telefono_contacto = models.CharField(max_length=15)
    acepto_terminos = models.BooleanField(default=False)
    rol = models.CharField(max_length=10, choices=ROLES, default='u')

    def es_vendedor(self):
        return self.rol == 'v'

    def es_usuario(self):
        return self.rol == 'u'
    
    def __str__(self):
        return self.nombre + ' ' + self.apellidos + ' - ' + self.rol
    
#El modelo Clave sera donde se almacenaran todos los datos necesarios que contenga una Key y esta Key siempre va a estar relacionada a un usuario

class Clave(models.Model):
    GENERO = (
        ('ACC', 'ACCION'),
        ('AVE', 'AVENTURA'),
        ('RPG', 'RPG'),
        ('EST', 'ESTRATEGIA'),
        ('DEP', 'DEPORTES'),
        ('SAN', 'SANDBOX')
        )
    
    nombre_juego = models.CharField(max_length=100)
    genero = models.CharField(max_length=50, choices=GENERO)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    clave_juego = models.CharField(max_length=255)
    terminos_y_condiciones = models.BooleanField(default=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    #imagen = models.ImageField(upload_to='imagenes_juegos/') ruta aun por definir
    en_venta = models.BooleanField(default=True)
    vendida = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre_juego
    
    
class Compra(models.Model):
    clave = models.ForeignKey(Clave, on_delete=models.CASCADE)
    comprador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Compra de {self.clave.nombre_juego} por {self.comprador.nombre}"
    
    #Esta función lo que hace es automatizar el cambio de estado de una venta de una clave, osea las claves se publican para todos los usuarios, y cuando una de esta es comprada, ya no tiene porque estar visible para todos los usuarios, entonces este codigo lo que hace es cambiar el estado del campo "en_venta" por False y el campo "vendida" por True cuando efectivamente se hace la venta de una clave
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Marcar la clave como vendida
        self.clave.vendida = True
        self.clave.en_venta = False
        self.clave.save()
