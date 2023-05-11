from PIL import Image, ImageDraw
import json
import io
import PySimpleGUI as psg


def convertir_a_bytes(file_or_bytes, resize=None):
   #Esta funcion nos permite utilizar la imagen creada con PIL y mostrarla en la intergaz

   img = Image.open(file_or_bytes)
   with io.BytesIO() as bio:
      img.save(bio, format="PNG")
      del img
      return bio.getvalue()


image = Image.new('RGB', (250, 250), color ='white')
draw = ImageDraw.Draw(image)
image.save('test.png')

img_bytes = convertir_a_bytes('test.png')

imagen = psg.Image(data = img_bytes, size=(250,250))

datos = {}

def verificar_existe(alias):

   # Lee el archivo JSON en una lista de diccionarios
    try:
       with open('usuarios.json', 'r') as archivo:
           lista = json.load(archivo)
       for diccionario in lista:
           if 'alias' in diccionario and diccionario['alias'] == alias:
              return True
       return False 
    except:
       return False 

def verificar_numero(valor):
    # Comprueba si el valor es un número
    if valor.isdigit():
        return True
    else:
        # Muestra un popup de aviso si el valor no es un número
        return False

def popup_get_file(message, title=None):
   #Crea una ventana popup que busca una imagen

    layout = [
        [psg.Text(message)],
        [psg.Input(key='-INPUT-'), psg.FilesBrowse('Navegar', key="imagen", file_types=[("GIF files", "*.gif"), ("PNG files", "*.png"), ("JPG files", "*.jpg"), ("JPEG files", "*.jpeg")])],
        [psg.Button('Ok'), psg.Button('Cancelar')],
    ]
    window = psg.Window(title if title else message, layout)
    event, values = window.read(close=True)
    if event == 'Ok':
        datos['imagen'] = values['imagen']
        return datos
    else:
        return None


columma_izquierda = psg.Column(layout=[[psg.Text(text="Nuevo perfil", font=("Arial", 20), size=15, expand_x=True, justification='left')],
                                [psg.Text(text="Nick o Alias: ", font=("Arial", 15), size=15, expand_x=True, justification='left')],
                                [psg.Input(key='alias')],
                                [psg.Text(text="Nombre: ", font=("Arial", 15), size=15, expand_x=True, justification='left')],
                                [psg.Input(key='nombre')],
                                [psg.Text(text="Edad: ", font=("Arial", 20), size=15, expand_x=True, justification='left')],
                                [psg.Input(key='edad')],
                                [psg.Text(text="Genero autopercibido: ", font=("Arial", 20), size=15, expand_x=True, justification='left')],
                                [psg.OptionMenu(values=('Masculino', 'Femenino'),  k='genero')],
                                [psg.Checkbox('Otro', default=False,key='otro', enable_events=True)],
                                [psg.Text(text="Que otro:", font=("Arial", 20), size=15, expand_x=True, justification='left', key='-OTRO-', visible=False)],
                                [psg.Input(key='otro_genero', visible=False)],
                                [psg.B('Guardar')]], justification = 'left')

columna_derecha = psg.Column(layout = [[imagen], 
                  [psg.Button('Cargar imagen', size=(30, 2))]], justification='right')



layout = [

    [columma_izquierda],
    [columna_derecha]

]

si = False

window = psg.Window('crear usuario', layout, size=(1024, 720))
while True:
   event, values = window.read()
   print(event, values)
   if event in (None, 'Exit'):
      break
   if event == 'Guardar':
      if verificar_existe(values['alias']):
          psg.popup('El alias ingresado ya existe, ingrese otro')
      if verificar_numero(values['edad']):
          datos = values
      else:
          psg.popup('La edad ingresada no es un número')     
      if values['otro']:
          datos['genero'] = values['otro_genero']
      del datos['otro_genero']
   if event == 'otro': 
      si = not si
      window['-OTRO-'].update(visible = si)
      window['otro_genero'].update(visible=si)
   if event == 'Cargar imagen':
       # ahora nos permite seleccionar la foto
       datos = popup_get_file('Seleccionar imagen')
       if datos['imagen']:
           # modificaciones a la imagen
           image = Image.open(datos['imagen']).convert('RGB')
           image.thumbnail((250, 250))
           img_buffer = io.BytesIO()
           image.save(img_buffer, format='PNG')
           img_bytes = img_buffer.getvalue()
           imagen.update(data=img_bytes) # modifica lo que muestra la imagen
window.close()



del datos['otro']
print(datos)

try:
  with open('usuarios.json', 'r+') as archivo:
      data = json.load(archivo)
      data.append(datos)
      archivo.seek(0)
      json.dumps(data, ensure_ascii=False, indent=2)
      json.dump(data, archivo)
except FileNotFoundError:
   with open('usuarios.json', 'x') as archivo:
      json.dumps(datos, ensure_ascii=False, indent=2)
      json.dump([datos], archivo)
