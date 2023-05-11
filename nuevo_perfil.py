from PIL import Image, ImageDraw
import json
import io
import PySimpleGUI as sg


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

imagen = sg.Image(data = img_bytes, size=(250,250))

datos = {}

def verificar_existe(alias):

   # Lee el archivo JSON en una lista de diccionarios
    try:
       with open('usuarios.json', 'r') as archivo:
           lista = json.load(archivo)
       for diccionario in lista:
           if 'alias' in diccionario and diccionario['alias'] == alias:
              sg.popup('El alias ingresado ya existe, ingrese otro')
              return True
       return False 
    except FileNotFoundError:
       return False

def verificar_numero(valor):
    # Comprueba si el valor es un número
    if valor.isdigit():
        return True
    else:
        # Muestra un popup de aviso si el valor no es un número
        sg.popup('El alias ingresado ya existe, ingrese otro')
        return False
    
def verificar(datos):
   if(not (verificar_existe(datos['alias'])) and verificar_numero(datos['edad'])):
      return True 
   else:
      return False
    

def tiene_imagen(datos):
   if('imagen' in datos.keys()):
      return True
   else:
      return False

def popup_get_file(message, title=None):
   #Crea una ventana popup que busca una imagen

    layout = [
        [sg.Text(message)],
        [sg.Input(key='-INPUT-'), sg.FilesBrowse('Navegar', key="imagen", file_types=[("PNG files", "*.png"), ("JPG files", "*.jpg"), ("JPEG files", "*.jpeg")])],
        [sg.Button('Ok'), sg.Button('Cancelar')],
    ]
    window = sg.Window(title if title else message, layout)
    event, values = window.read(close=True)
    if event == 'Ok':
        datos['imagen'] = values['imagen']
        print(datos['imagen'])
        return datos
    else:
        return None
    
def guardar_json(datos):
   """
      Guarda en usuarios.json los datos del usuario ingresado
   """
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


columma_izquierda = sg.Column(layout=[[sg.Text(text="Nuevo perfil", font=("Arial", 20), size=15, expand_x=True, justification='left')],
                                [sg.Text(text="Nick o Alias: ", font=("Arial", 15), size=15, expand_x=True, justification='left')],
                                [sg.Input(key='alias')],
                                [sg.Text(text="Nombre: ", font=("Arial", 15), size=15, expand_x=True, justification='left')],
                                [sg.Input(key='nombre')],
                                [sg.Text(text="Edad: ", font=("Arial", 20), size=15, expand_x=True, justification='left')],
                                [sg.Input(key='edad')],
                                [sg.Text(text="Genero autopercibido: ", font=("Arial", 20), size=15, expand_x=True, justification='left')],
                                [sg.OptionMenu(values=('Masculino', 'Femenino'),  k='genero')],
                                [sg.Checkbox('Otro', default=False,key='otro', enable_events=True)],
                                [sg.Text(text="Que otro:", font=("Arial", 20), size=15, expand_x=True, justification='left', key='-OTRO-', visible=False)],
                                [sg.Input(key='otro_genero', visible=False)],
                                [sg.B('Guardar')]], justification = 'left')

columna_derecha = sg.Column(layout = [[imagen], 
                  [sg.Button('Cargar imagen', size=(30, 2))]], justification='right')



layout = [

    [columma_izquierda],
    [columna_derecha]

]

si = False

window = sg.Window('crear usuario', layout, size=(1024, 720))
while True:
   event, values = window.read()
   print(event, values)
   if event in (None, 'Exit'):
      break
   if event == 'Guardar':
      if verificar(values):        
          if values['otro']:
             print('watatatataq')
             values['genero'] = values['otro_genero']   
          del values['otro_genero']
          del values['otro']
          datos.update(values) 
          if(tiene_imagen(datos)):
             guardar_json(datos)
             break
          else:
             events_popup, values_popup = sg.popup('Ingrese una imagen')   
   if event == 'otro': 
      si = not si
      window['-OTRO-'].update(visible = si)
      window['otro_genero'].update(visible=si)
   if event == 'Cargar imagen':
       # ahora nos permite seleccionar la foto
       datos_img = popup_get_file('Seleccionar imagen')
       if datos_img['imagen']:
           # modificaciones a la imagen
           image = Image.open(datos['imagen']).convert('RGB')
           image.thumbnail((250, 250))
           img_buffer = io.BytesIO()
           image.save(img_buffer, format='PNG')
           img_bytes = img_buffer.getvalue()
           imagen.update(data=img_bytes) # modifica lo que muestra la imagen
window.close()




print(datos)

