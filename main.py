#!/usr/bin/env python
# coding: utf-8

# # Instalaciones PIP

# In[1]:


#!pip install lxml
#!pip install beautifulsoup4
#!pip install twilio
#!pip install mysqlclient
#!pip install tornado==6.1
#!pip install python-telegram-bot
#!pip3 install yagmail[all]
#!pip install nltk
#!pip install smtplib
#!pip install -U scikit-learn scipy matplotlib
#!pip install pywhatkit
#!pip install twilio


# # Importaciones

# In[2]:


import nltk
import logging
import smtplib 
from email.message import EmailMessage 
import random
import string
import pywhatkit
import logging
from telegram import *
from telegram.ext import *
from datetime import datetime, timedelta
from random import randint
import xml.etree.ElementTree as ET  
import math


#nltk.download('omw-1.4')
#nltk.download('punkt') # Instalar módulo punkt si no está ya instalado (solo ejecutar la primera vez)
#nltk.download('wordnet') # Instalar módulo wordnet si no está ya instalado (solo ejecutar la primera vez)'
#nltk.download('stopwords')


# # configuración de la DATABASE

# In[3]:


#=============================================
   # CONEXION A LA BASE DE DATOS
   # ============================================="""   
import MySQLdb

hostname = 'localhost'
username1 = 'root'
password = ''
database = 'chatbot'

def connect():
  connection = None
  try:
    connection =  MySQLdb.connect( host=hostname, user=username1, passwd=password, db=database )
    print('success')
  except MySQLdb.Error as e:
    print(e) 
  return connection


def execute_query(connection, query): 
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
        return cursor.lastrowid
    except MySQLdb.Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except MySQLdb.Error as e:
        print(f"The error '{e}' occurred")


connection = connect()


# # Base de conocimiento

# In[4]:


data = open('memoria.txt', 'r', errors='ignore')
conocimiento = data.read()
conocimiento = conocimiento.lower()

sent_tokens = nltk.sent_tokenize(conocimiento)
word_tokens = nltk.sent_tokenize(conocimiento)
lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# # Saludos

# In[5]:


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords

#=============================================
   # FUNCION PARA DETERMINAR LA SIMILITUD DEL TEXTO INSERTADO Y EL CORPUS
   # ============================================="""   

def response(user_response):
    robo_response = ''
    # Añade al corpus la respuesta de usuario al final
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(
        tokenizer=LemNormalize, stop_words=stopwords.words('spanish'))
    tfidf = TfidfVec.fit_transform(sent_tokens)
    # 3 EVALUAR SIMILITUD DE COSENO ENTRE MENSAJE USUARIO (tfidf[-1]) y el CORPUS (tfidf)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]

    if(req_tfidf == 0):
        robo_response = robo_response +               "Lo siento, no he entendido tu mensaje. Trata de utilzar otras palabras"
        return robo_response

    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response


SALUDOS_INPUTS = ("hola", "buenas", "saludos", "qué tal", "hey", "buenos dias", 'klk')
SALUDOS_OUTPUTS = ["Hola", "Hola, ¿Qué tal?", "Hola, ¿Cómo te puedo ayudar?", "Hola, encantado de hablar contigo"]

def saludos(sentence):
    for word in sentence.split():
        if word.lower() in SALUDOS_INPUTS:
            return random.choice(SALUDOS_OUTPUTS)

def verificarTexto(msg):
    respuesta = ''
    if(saludos(msg) != None):  
        respuesta =  saludos(msg)

    else: 
        respuesta = response(msg)
        sent_tokens.remove(msg)
    return respuesta


# # Importacion XML  biblia 

# In[6]:


#=============================================
   # GENERADOR DE VERSICULOS Y FRASES
   # ============================================="""   
arbol = ET.parse('Bible_Espanol_oso.xml') 
def generarVersiculo():
    root = arbol.getroot() 

    partesXML=arbol.findall('BIBLEBOOK')
    partes = randint(0, len(partesXML)-1)

    capituloXML=root[partes].findall('CHAPTER')
    capitulo = randint(0, len(capituloXML)-1)

    versiculoXML= root[partes][capitulo].findall('VERS')
    versiculo=randint(0, len(versiculoXML)-1)

    nombre_=root[partes].attrib['bname']
    cap_=root[partes][capitulo].attrib['cnumber']
    ver_=root[partes][capitulo][versiculo].attrib['vnumber']
    versiculo=root[partes][capitulo][versiculo].text
    formato="{} {} {}\n{}".format(nombre_,cap_,ver_,versiculo)  
    return formato


# In[7]:


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


# # Lista de mensajes

# In[8]:


INICIO_MSG = (
    "Hola  *{first_name}*!\n\n"
    "Soy el bot de alas de Paz 🕊️.\n\n"
    "Envia /ayuda para empezar y ver las instrucciones 📖."
) 

AYUDA_MSG = (
    "Hola *{first_name}*!\n\n"
    "Esta es la lista de comandos📖:\n\n"
    "*suscribirse*: para recibir versiculos diarios✍️.\n\n"
    "*desuscribirse*: para anular la suscripcion✍️.\n\n"
    "*flores/productos*: para ver todas las floresdisponibles de Alas de Paz 🕊️.\n\n"
    "*agregar nombre_producto*: para ver descripcion del arreglo floral y poder ser agregado al carrito🌺.\n\n"
    "*correo correo@electronico*: configurar correo✉️.\n\n"
    "*Telefono*: configurar tu numero telefonico📞.\n\n"
    "*carrito*: ver la orden actual🛒.\n\n"
    "Si envias la *ubicación* 🏠 esta se guardará para futuros pedidos de flores\n"
)


# # Funciones del bot

# In[9]:


#=============================================
   # FUNCION PARA LISTADO DE ARREGLO DE FLORES
   # ============================================="""   
def floresLista(update):
  select_flor = "SELECT flor_nombre,  flor_precio, flor_imagen from flores"
  arreglosFlorales = execute_read_query(connection, select_flor)
  update.message.reply_text('Listado de los arreglos florales disponibles')
  update.message.reply_text('Para ver las descripciones de los arreglos y poder agregarlos al carrito escribe\n agregar nombre_arreglo, ej: descripcion AMOROSSA')
  listado = ''
  for flor in arreglosFlorales:
    listado+= f'Arreglo Floral: {flor[0]}\nPrecio: RD${flor[1]}\n'
    listado+= '----------------------------\n'
    update.message.reply_photo(flor[2], listado)
    listado=''
    
#=============================================
   # FUNCION PARA GUARDAR EL CORREO DEL USUARIO
   # ============================================="""
def cambiarCorreo(update, message):
  username = update.message.chat.username
  correo = message.split()[1]
  query = f'UPDATE cliente SET cliente_email = "{correo}" WHERE cliente_nombreUsuario = "{username}"'
  execute_query(connection, query)
  update.message.reply_text("Correo cambiado correctamente")
  return

#=============================================
   # FUNCION PARA GUARDAR EL TELEFONO DEL USUARIO
   # ============================================="""
def cambiarTel(update, message):
  username = update.message.chat.username
  print(username)
  telefono = message.split()[1]
  query = f'UPDATE cliente SET cliente_telefono = "{telefono}" WHERE cliente_nombreUsuario = "{username}"'
  execute_query(connection, query)
  update.message.reply_text("Numero agregado correctamente")
  return


# #=============================================
   # FUNCION PARA GUARDAR LA UBICACION DEL USUARIO
   # ============================================="""
def changeLocation(username, latitude, longitude, update):
    query = f'UPDATE cliente SET cliente_direccion = "{latitude} {longitude}" WHERE 	cliente_nombreUsuario = "{username}"'
    execute_query(connection, query)
    update.message.reply_text('Ubicación cambiada correctamente!')
    return

#=============================================
   # FUNCION PARA VER DESCIPCION DEL ARREGLO
   # ============================================="""
def descripcionDeArregloFloral(update, message):
  name = message[8:] 
  # debe estar en formato: agregar nombre_producto
  if(len(message) == 0):
    update.message.reply_text("Escribe el nombre del arreglo floral")
    return 0

  query = f'SELECT flor_id , flor_nombre,flor_descripcion, flor_precio, flor_imagen from flores WHERE flor_nombre LIKE "%{name}%"'
  arreglosFlorales = execute_read_query(connection, query)
  user = update.message.from_user
  # Mostrar los items que coiciden con la busqueda
  if(len(arreglosFlorales)):
    for flor in arreglosFlorales:
      update.message.reply_photo(flor[4], f'Arreglo Floral: {flor[1]}\nPrecio: RD${flor[3]}\nDescripcion: {flor[2]}')
      buttons = [[InlineKeyboardButton("Añadir", callback_data=f'agregas {flor[0]}')]]
      user.send_message(reply_markup=InlineKeyboardMarkup(buttons), text="¿Quieres añadirla al pedido")
  else:
     update.message.reply_text(f'No se encontró ningún arreglo floral con el nombre de {name}')     
        

#=============================================
   # FUNCION PARA LOS BOTONES DEL CHAT
   # ============================================="""
def queryHandler(update: Update, context: CallbackContext):
    
    query = update.callback_query.data
    update.callback_query.answer()
    bot = context.bot
    chat_id = update.effective_chat.id
    
    id = update.callback_query.message.chat.id
    username = update.callback_query.message.chat.username
    
    if(query.find('ayuda') > -1):
        menu_1 = [[KeyboardButton('suscribirse')],
                  [KeyboardButton('desuscribirse')],
                  [KeyboardButton('flores')],
                  [KeyboardButton('agregar')],
                  [KeyboardButton('carrito')]]
                  
        context.bot.send_message(chat_id=update.effective_chat.id, text=AYUDA_MSG.format(first_name=username, chat_id=chat_id),parse_mode= 'Markdown', reply_markup=ReplyKeyboardMarkup(menu_1))
    
    
    queryEmail = f'SELECT cliente_email, cliente_direccion, cliente_telefono, cliente_nombre from cliente c WHERE c.cliente_nombreUsuario = "{username}"'
    data = execute_read_query(connection, queryEmail)
    user_email = data[0][0]
    user_location = data[0][1]
    user_tel = data[0][2]
    user_nombre = data[0][3]
    

    PAYMENT_PROVIDER_TOKEN = "284685063:TEST:OGM3ODNkZjM2OTMx"
        
    chat_id = id
    title = "Funeraria Alas de Paz"
    description = "Pagos"
    # select a payload just for you to recognize its the donation from your bot
    payload = "Custom-Payload"
    # In order to get a provider_token see https://core.telegram.org/bots/payments#getting-a-token
    currency = "DOP"
    
        
    if(query.find('agregas') > -1):
      flor_id = query[8:]
      guardarPedido(username, flor_id)
      bot.send_message(chat_id=id, text="Arreglo floral añadido al carrito🛒\n\nPara ver su pedido escriba carrito.") 
    #=============================================
   # PAGOS SIN ENVIO 
   # ============================================="""
    if(query.find('hacer_pedido_recojer') > -1):
    
      if(user_email and user_location and user_tel):
        data = query.split()
        idPedido=data[1]
        idUsuario=data[2]
        
        # Calcular el total a pagar
        queryprice = f'SELECT SUM(oi.precio) FROM orden o INNER JOIN ordenitem oi ON o.orden_id = oi.ordenItem_id WHERE o.orden_id = {idPedido}'
        # Listado de productos de la orden
        queryFlorList = f'SELECT flor_nombre, cantidad, flor_precio from (SELECT o.orden_id, oi.flor_id, oi.cantidad FROM orden o INNER JOIN ordenitem oi ON o.orden_id = oi.ordenItem_id WHERE o.orden_id = {idPedido}) as p INNER JOIN flores ON flores.flor_id = p.flor_id'
        price1 = execute_read_query(connection, queryprice)
        florList = execute_read_query(connection, queryFlorList)
        
        query = f'UPDATE orden SET orden_estatus = 4, orden_creado = "{datetime.now()}" WHERE orden_id = {idPedido} AND cliente_id = {idUsuario}'
        mensaje = 'La orden ha sido realizada, tienes 4 Horas para cancelarla\n'
        mensaje+= 'Contenido del pedido\n'
        for flor in florList:
            mensaje+= f'Arreglo Floral: {flor[0]} Cantidad: {flor[1]} Precio: RD${flor[2]}\n'
            
        mensaje+= '----------------------------\n'
        mensaje+= f'Subtotal: RD${float(price1[0][0])}\n'
        mensaje+= f'Envio: RD${0}\n'
        mensaje+= f'Total: RD${price1[0][0]}'
    

  # Se envia la factura al cliente si tiene el correo electronico y la ubicación configurados
        
        enviaremail(mensaje, user_email)
        enviarmsjwhatsapp(mensaje, user_tel)
        execute_query(connection, query)
        
  
    # price in dollars
        prices = []
        for flor in florList:
            prices.append(LabeledPrice(f'Arreglo Floral: {flor[0]}', flor[2] * 100))

    # optionally pass need_name=True, need_phone_number=True,
    # need_email=True, need_shipping_address=True, is_flexible=True
        context.bot.send_invoice(chat_id, title, description, payload, PAYMENT_PROVIDER_TOKEN, currency, prices)
        
        bot.send_message(chat_id=id, text="La orden se marcó como pendiente, tienes 4 horas para cancelarla.\n Además se envió un mensaje a tu cuenta de correo y tu whatsapp, asegurate de haberlo configurado correctamente\n\nSi deseas cancelar el pedido escriba carrito.")
            
      else:
        bot.send_message(chat_id=id, text="No tienes un correo o ubicación configurado.")
        bot.send_message(chat_id=id, text="Escribe el comando: correo mi@correo.com, para configurar el correo.")
        bot.send_message(chat_id=id, text="Escribe el comando: telefono, para configurar el numero telefonico.")
        bot.send_message(chat_id=id, text="Envia tu ubicación para guardarla")
     #=============================================
   # PAGOS CON ENVIOS CALCULANDO LA DIRRECION
   # ============================================="""
    if(query.find('hacer_pedido_envio') > -1):
     
      if(user_email and user_location and user_tel):
        data = query.split()
        idPedido=data[1]
        idUsuario=data[2]
        
        # Calcular el total a pagar
        queryprice = f'SELECT SUM(oi.precio) FROM orden o INNER JOIN ordenitem oi ON o.orden_id = oi.ordenItem_id WHERE o.orden_id = {idPedido}'
        # Listado de productos de la orden
        queryFlorList = f'SELECT flor_nombre, cantidad, flor_precio from (SELECT o.orden_id, oi.flor_id, oi.cantidad FROM orden o INNER JOIN ordenitem oi ON o.orden_id = oi.ordenItem_id WHERE o.orden_id = {idPedido}) as p INNER JOIN flores ON flores.flor_id = p.flor_id'
        price1 = execute_read_query(connection, queryprice)
        florList = execute_read_query(connection, queryFlorList)
        
        
        lat1= float(user_location.split()[0])
        lon1 = float(user_location.split()[1])
        print(lat1)
        #menos de 5 km
        lat2 = 19.469075
        lon2 = -70.686818
         
        #mas de 10km    
        #lat2 = 19.338997
        #lon2 = -70.910295
        
        #mas de 5 km
        #lat2 = 19.440720
        #lon2 = -70.716654
        
        distancia= haversine(lat1, lon1, lat2, lon2)
        #=============================================
   # ENVIO A MAS DE 10 KM 
   # ============================================="""
        if(distancia > 10):
           bot.send_message(chat_id=id, text="No se puede enviar el pedido a tu ubicacion, estas a " + format(distancia, '0.2f') + " KM de distancia")
        #=============================================
   # PAGOS CON ENVIOS A MAS DE 5KM
   # ============================================="""    
        elif(distancia > 5):
            
            query = f'UPDATE orden SET orden_estatus = 4, orden_creado = "{datetime.now()}" WHERE orden_id = {idPedido} AND cliente_id = {idUsuario}'
            mensaje = 'La orden ha sido realizada, tienes 4 Horas para cancelarla\n'
            mensaje+= 'Contenido del pedido\n'
            for flor in florList:
                mensaje+= f'Arreglo Floral: {flor[0]} Cantidad: {flor[1]} Precio: RD${flor[2]}\n'

            mensaje+= '----------------------------\n'
            mensaje+= f'Subtotal: RD${float(price1[0][0])}\n'
            mensaje+= f'Envio: RD${200}\n'
            mensaje+= f'Total: RD${float(price1[0][0]) + 200}'
        
        # Se envia la factura al cliente si tiene el correo electronico y la ubicación configurados
        
            enviaremail(mensaje, user_email)
            enviarmsjwhatsapp(mensaje, user_tel)
            execute_query(connection, query)
            
            # price in dollars
            prices = []
            for flor in florList:
                prices.append(LabeledPrice(f'Arreglo Floral: {flor[0]}', flor[2] * 100))
            
        # optionally pass need_name=True, need_phone_number=True,
        # need_email=True, need_shipping_address=True, is_flexible=True
            context.bot.send_invoice(
                  chat_id,
                  title,
                  description,
                  payload,
                  PAYMENT_PROVIDER_TOKEN,
                  currency,
                  prices,
                  need_name=True,
                  need_phone_number=user_tel,
                  need_email=user_email,
                  need_shipping_address=True,
                  is_flexible=True,)
            
            bot.send_message(chat_id=id, text="La orden se marcó como pendiente y *se aplicara un cargo adicional por el envio*, tienes 4 horas para cancelarla.\n Además se envió un mensaje a tu cuenta de correo y tu whatsapp, asegurate de haberlo configurado correctamente\n\nSi deseas cancelar el pedido escriba carrito.")
        
        #=============================================
            #PAGOS CON ENVIO GRATIS
        #=============================================
        else:
            query = f'UPDATE orden SET orden_estatus = 4, orden_creado = "{datetime.now()}" WHERE orden_id = {idPedido} AND cliente_id = {idUsuario}'
            mensaje = 'La orden ha sido realizada, tienes 4 Horas para cancelarla\n'
            mensaje+= 'Contenido del pedido\n'
            for flor in florList:
                mensaje+= f'Arreglo Floral: {flor[0]} Cantidad: {flor[1]} Precio: RD${flor[2]}\n'
                #mensaje1=f'Arreglo Floral: {flor[0]}'
            mensaje+= '----------------------------\n'
            mensaje+= f'Subtotal: RD${float(price1[0][0])}\n'
            mensaje+= f'Envio: RD${0}\n'
            mensaje+= f'Total: RD${price1[0][0]}'
        
        # Se envia la factura al cliente si tiene el correo electronico y la ubicación configurados
        
            enviaremail(mensaje, user_email)
            enviarmsjwhatsapp(mensaje, user_tel)
            execute_query(connection, query)
            
            # price in dollars
            prices = []
            for flor in florList:
                prices.append(LabeledPrice(f'Arreglo Floral: {flor[0]}', flor[2] * 100))
            
        # optionally pass need_name=True, need_phone_number=True,
        # need_email=True, need_shipping_address=True, is_flexible=True
            context.bot.send_invoice(
                  chat_id,
                  title,
                  description,
                  payload,
                  PAYMENT_PROVIDER_TOKEN,
                  currency,
                  prices,
                  need_name=True,
                  need_phone_number=True,
                  need_email=True,
                  need_shipping_address=True,
                  is_flexible=False,)
            bot.send_message(chat_id=id, text="La orden se marcó como pendiente, se enviara a la ubicacion seleccionada **sin cargo adicional**, tienes 4 horas para cancelarla.\n Además se envió un mensaje a tu cuenta de correo y tu whatsapp, asegurate de haberlo configurado correctamente\n\nSi deseas cancelar el pedido escriba carrito.")
    
      else:
        bot.send_message(chat_id=id, text="No tienes un correo o ubicación configurado.")
        bot.send_message(chat_id=id, text="Escribe el comando: correo mi@correo.com, para configurar el correo.")
        bot.send_message(chat_id=id, text="Escribe el comando: telefono, para configurar el numero telefonico.")
        bot.send_message(chat_id=id, text="Envia tu ubicación para guardarla.")  
    
   #=============================================
            #CANCELAR LA ORDEN
    #============================================="""                       
    if(query.find('cancelar_orden') > -1):
      data = query.split()
      cancelarOrden(data[1], bot, id)
        
   # """=============================================
   # SUSCRIBIRSE PARA RECIBIR VERSICULOS Y FRASES
   # ============================================="""     
    if(query.find('suscribirse') > -1):
      data = query[12:]  
      query = f'UPDATE cliente SET cliente_suscrito = 1 WHERE cliente_nombreUsuario  = "{data}"'
      execute_query(connection=connection, query=query)

    
      usser_id=update.callback_query.from_user.id
      print("usser_id : ",usser_id)  
      context.user_data['username']= username
      context.user_data['usser_id']= usser_id
      context.job_queue.run_repeating(enviarVersiculo, interval=50, first=10, context=id, name=f"{usser_id}")
     
      bot.send_message(chat_id=id, text="Te acabas de suscribir.\n recibiras textos biblicos y frases todos los dias\n para desuscribirte escribe desuscribirse o seleccionalo en el menu.")
    
    #"""=============================================
   ## DESUCRIBIRSE DE DECIBIR VERSICULOS Y FRASES
    #=============================================""" 
    if(query.find('des_uscribirse') > -1):
        x=query.split(" ")
        print("desuscribirse : ",x )
        usser_id=update.callback_query.from_user.id
        current_jobs = context.job_queue.get_jobs_by_name(f"{usser_id}")

        for job in current_jobs:
              job.schedule_removal()        

        data = query[15:]  
        query = f'UPDATE cliente SET cliente_suscrito = 0 WHERE cliente_nombreUsuario  = "{x[1]}"'
        execute_query(connection=connection, query=query)
        bot.send_message(chat_id=int(x[2]), text="Te acabas de desuscribir.\n dejaras de recibir textos biblicos y frases todos los dias\n para suscribirte escribe suscribirse.")


        
#"""=============================================
   # CANCELAR ORDEN
    #=============================================""" 
def cancelarOrden(idOrden, bot, id):  
  query = f'SELECT o.orden_creado from orden o WHERE o.orden_id = {idOrden}'
  data = execute_read_query(connection, query)
  fechaPedido = data[0][0]
  print('fechaPedido:',fechaPedido)
  fechaPedido = datetime.strptime(fechaPedido,'%Y-%m-%d %H:%M:%S.%f')
  print('fechaPedido 2:',fechaPedido)
  fechaActual = datetime.now()
  diferencia = fechaActual - fechaPedido
  diferencia = diferencia.total_seconds() / 60
  respuesta = ''
  if(diferencia > 240):
    respuesta ="Ya no se puede cancelar la orden, han pasado más de 4 horas"
  else:
    query = f'UPDATE orden SET orden_estatus = 3 WHERE orden_id  = {idOrden}'
    execute_query(connection=connection, query=query)
    respuesta ="Orden cancelada"
  bot.send_message(chat_id=id, text=respuesta)
  return

#"""=============================================
    #GUARDAR PEDIDO EN EL CARRITO
    #=============================================""" 
def guardarPedido(username, flor_id): 
  query = f'SELECT cliente_id FROM cliente where cliente_nombreUsuario = "{username}"'
  user = execute_read_query(connection, query)
  user_id = user[0][0]
  print("user id: ",user_id)

  query = f'SELECT flor_precio FROM flores where flor_id  = "{flor_id}"'
  flor = execute_read_query(connection, query)
  flor_precio = flor[0][0]
  print("flor_precio : ",flor_precio)
    
  # 1. Buscar si existe una orden con tipo carrito de este cliente
  query = f'SELECT * from orden where cliente_id = {user_id} AND orden_estatus = 4'
  exits = execute_read_query(connection, query)
  id_orden = 0
  if(len(exits) < 1):
    # Crear orden tipo carrito
    query = f'INSERT INTO orden(cliente_id, orden_estatus) VALUES({user_id}, "4")'
    id_orden = execute_query(connection, query)
  else:
    # Usar la orden ya creada
    id_orden = exits[0][0]
    print("id_orden id: ",id_orden)

  # Ahadir el producto a la orden  
  query = f'INSERT INTO ordenitem(ordenItem_id, flor_id, cantidad, precio) VALUES("{id_orden}", "{flor_id}", "1", "{flor_precio}")'
  execute_query(connection, query)
  return





# In[10]:


#=============================================
# FUNCION PARA ANADIR EL COSTO DE ENVIO 
# =============================================""" 
def shipping_callback(update, context) -> None:
 """Answers the ShippingQuery with ShippingOptions"""
 query = update.shipping_query
 # check the payload, is this from your bot?
 if query.invoice_payload != "Custom-Payload":
     # answer False pre_checkout_query
     query.answer(ok=False, error_message="Something went wrong...")
     return

 # First option has a single LabeledPrice
 options = [ShippingOption("1", "Envio", [LabeledPrice("Envio", 20000)])]
 query.answer(ok=True, shipping_options=options)
 
#"""=============================================
# FUNCION CHECKOUT PARA EL PAGO
# ============================================="""     
def precheckout_callback(update, context):
 """Answers the PreQecheckoutQuery"""
 query = update.pre_checkout_query
 # check the payload, is this from your bot?
 if query.invoice_payload != "Custom-Payload":
     # answer False pre_checkout_query
      query.answer(ok=False, error_message="Something went wrong...")
 else:
      query.answer(ok=True)


# # Funciones Generales

# In[11]:


#=============================================
   # FUNCION PARA ENVIAL EMAIL
   # =============================================""" 
#resive el mensaje que se desea enviar y el email del usuario
def enviaremail(mensaje, email):

    message = EmailMessage() 

    # Configure email headers 
    message['Subject'] = "Orden Pedido Floral"  
    message['From'] = "funebot21@gmail.com"
    message['To'] = email

    # Set email body text 
    message.set_content(mensaje) 

    # Set smtp server and port 
    server = smtplib.SMTP("smtp.mailtrap.io", '2525') 

    # Identify this client to the SMTP server 
    server.ehlo() 

    # Secure the SMTP connection 
    server.starttls() 

    # Login to email account 
    server.login("07dc4f467bde8f", "1634f4420b12ec" ) 

    # Send email 
    server.send_message(message) 

    # Close connection to server 
    server.quit()
    
#=============================================
   # FUNCION PARA ENVIAR MSJ A WHATSAPP
   # ============================================="""        
def enviarmsjwhatsapp(mensaje, user_tel):       
#Enviar msj del pedido a whatsapp
    from twilio.rest import Client 
    account_sid = 'AC588f0503e61c35a576bfe860dba7a3ea' 
    auth_token = 'f594f2c6ab8f11b548dd771468bfc9e1' 
    client = Client(account_sid, auth_token) 
    message = client.messages.create( 
                             from_='whatsapp:+14155238886',  
                             body=mensaje,      
                             to=f'whatsapp:+1{user_tel}' 
                        ) 

 #=============================================
   # FUNCION PARA CALCULAR LA DISTANCIA ENTRE DOS PUNTOS
   # ============================================="""          
#recibe las longitudes y latitudes como parametros 

def haversine(lat1, lon1, lat2, lon2):
  rad=math.pi/180
  dlat=lat2-lat1
  dlon=lon2-lon1
  R=6372.795477598
  a=(math.sin(rad*dlat/2))**2 + math.cos(rad*lat1)*math.cos(rad*lat2)*(math.sin(rad*dlon/2))**2
  distancia=2*R*math.asin(math.sqrt(a))
  return distancia


# In[12]:


#=============================================
   # FUNCION PARA VER CARRITO
   # ============================================="""   
def verCarrito(update, message):
  print("carrito") 
  print(update.message)
  userTelegram = update.message.from_user
  username = update.message.chat.username

  # Get Customerid
  query = f'SELECT cliente_id FROM cliente where cliente_nombreUsuario = "{username}"'
  user = execute_read_query(connection, query)
  user_id = user[0][0]

  # 1. Buscar si existe una orden con tipo carrito de este cliente
  query = f'SELECT * from orden where cliente_id = {user_id} AND orden_estatus = 4'
  exits = execute_read_query(connection, query)
  id_orden = 0

  if(len(exits) < 1):
    query = f'SELECT * from orden where cliente_id = {user_id} AND orden_estatus = 2'
    exitsPending = execute_read_query(connection, query)
    if(len(exitsPending) > 0 ):
      update.message.reply_text('Tienes una orden pendiente')
      buttons = [[InlineKeyboardButton("Cancelar orden", callback_data=f'cancelar_orden {exitsPending[0][0]}')]]
      userTelegram.send_message(reply_markup=InlineKeyboardMarkup(buttons), text='¿Deseas cancelarla?')
    else: 
      update.message.reply_text('No tienes ningún carrito')
    return
  else:
    id_orden = exits[0][0]

  print("verCarrito id_orden id: ",id_orden)
  queryprice = f'SELECT SUM(oi.precio) FROM orden o INNER JOIN ordenitem oi ON o.orden_id = oi.ordenItem_id WHERE o.orden_id = {id_orden}'
  queryFlorList = f'SELECT flor_nombre, cantidad, flor_precio from (SELECT o.orden_id, oi.flor_id, oi.cantidad FROM orden o INNER JOIN ordenitem oi ON o.orden_id = oi.ordenItem_id WHERE o.orden_id = {id_orden}) as p INNER JOIN flores ON flores.flor_id  = p.flor_id'
  price = execute_read_query(connection, queryprice)
  floresList = execute_read_query(connection, queryFlorList)

  # Mostrar el listado de articulos del carrito
  listado = ''
  for flor in floresList:
      listado+= f'Arreglo Floral: {flor[0]} Cantidad: {flor[1]} Precio: RD${flor[2]}\n'
  update.message.reply_text(listado)
  update.message.reply_text('----------------------------')
  update.message.reply_text(f'Total: RD${price[0][0]}')
  update.message.reply_text('Puedes hacer el pedido ahora o seguir añadiendo productos')
  buttons = [[InlineKeyboardButton("Pasar a recojer", callback_data=f'hacer_pedido_recojer {id_orden} {user_id}')]]
  userTelegram.send_message(reply_markup=InlineKeyboardMarkup(buttons), text="¿Deseas realizar el pedido para recojer?")
  buttons = [[InlineKeyboardButton("Enviar", callback_data=f'hacer_pedido_envio {id_orden} {user_id}')]]
  userTelegram.send_message(reply_markup=InlineKeyboardMarkup(buttons), text="¿Deseas realizar el pedido con envio?")
    


# In[14]:


#=============================================
   # FUNCION PARA SUSCRIBIRSE
   # ============================================="""   
def suscribirse(update, message):
    userTelegram = update.message.from_user
    username = update.message.chat.username
    
    query = f'SELECT cliente_suscrito FROM cliente where cliente_nombreUsuario = "{username}"'
    user_suscripcion = execute_read_query(connection, query)
    suscripcion = user_suscripcion[0][0]
    if (suscripcion == 0):
        #no esta suscripto
        
        update.message.reply_text('Recibiras versiculos biblicos y frases de forma diaria.')
        buttons = [[InlineKeyboardButton("Suscribirse", callback_data=f'suscribirse {username}')]]
        userTelegram.send_message(reply_markup=InlineKeyboardMarkup(buttons), text='¿Deseas suscribirte?')
    if (suscripcion == 1):
        update.message.reply_text('Ya estas suscrito.')
        
        
 #=============================================
   # FUNCION PARA DESUSCRIBIRSE
   # ============================================="""          
def desuscribirse(update, message):
    userTelegram = update.message.from_user
    username = update.message.chat.username
    
    query = f'SELECT cliente_suscrito FROM cliente WHERE cliente_nombreUsuario = "{username}"'
    user_suscripcion = execute_read_query(connection, query)
    suscripcion = user_suscripcion[0][0]
    if (suscripcion == 1):
        #esta suscripto

        chatt_id=update.message.chat.id
        update.message.reply_text('Dejaras de recibir versiculos biblicos de forma diaria.')
        buttons = [[InlineKeyboardButton("Desuscribirse", callback_data=f'des_uscribirse {username} {chatt_id}')]]
        userTelegram.send_message(reply_markup=InlineKeyboardMarkup(buttons), text='¿Deseas desuscribirte?')
    if (suscripcion == 0):
         #no esta suscripto
        update.message.reply_text('No estas estas suscrito.')
        
        
        


# In[15]:


#=============================================
   # MENU DE OPCIONES
   # ============================================="""   
def respuestas(message, update): 
    if message in ('suscribirse'):
        return suscribirse(update, message)
    
    if message in ('desuscribirse'):
        return desuscribirse(update, message)
    if message in ('flores', 'productos'):
        return floresLista(update)
 
    if(message.find('agregar') > -1):
        return descripcionDeArregloFloral(update, message)

    if(message.find('correo') > -1):
        return cambiarCorreo(update, message)
    
    if message in ('carrito'):
        print(message)
        return verCarrito(update, message)
     
    
    if(message.find('telefono') > -1 ):
        return cambiarTel(update, message)
   
        
    return verificarTexto(message)


# In[16]:


#=============================================
   # FUNCION PARA COMANDO INICIAL
   # ============================================="""   
def start_comando(update, context):
    first_name = update.message.from_user.first_name
    username =update.message.from_user['username']
    buttons = [[InlineKeyboardButton("ayuda", callback_data='ayuda')]]
    chat_id = update.effective_chat.id
    id =update.effective_chat.id
    context.bot.send_message(reply_markup=InlineKeyboardMarkup(buttons),
        chat_id=update.message.chat_id,
        text=INICIO_MSG.format(first_name=first_name, chat_id=chat_id),parse_mode= 'Markdown'
    )
 #=============================================
   # FUNCION PARA COMANDO AYUDA
   # ============================================="""      
def ayuda_comando(update: Update, context: CallbackContext) -> None:
    first_name = update.message.from_user.first_name
    chat_id = update.effective_chat.id
    
    
    context.bot.send_message( 
        chat_id=update.message.chat_id,
        text=AYUDA_MSG.format(first_name=first_name, chat_id=chat_id),parse_mode= 'Markdown'
    )
    
#=============================================
   # FUNCION PARA ENVIO DE MENSAJES
   # ============================================="""       
def handle_message(update, context):
  text = str(update.message.text).lower()
  user = update.message.from_user  
  ''' Verificar si el usuario está guardado '''
  verificarUsuario(user)
  #verificarSuscripcion()
  response = respuestas(text, update)
  if(response):
    update.message.reply_text(response)
    
#=============================================
   # FUNCION PARA RECIBIR LA LOCALIZACION DEL CHAT
   # ============================================="""       
def LocationMessageEvent(update, context):
    username  = update.message.chat.username
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude
    changeLocation(username, latitude, longitude, update)


# In[17]:


#=============================================
   # FUNCION PARA GUARDAR USUARIOS
   # ============================================="""   
def verificarUsuario(user):
  query = f'SELECT * FROM cliente where cliente_nombreUsuario = "{user.username}"'
  user_exits = execute_read_query(connection, query)
  if(len(user_exits)):
    print(f'Existe el usuario: {user.username}')
  else:
    print('Guardando el usuario en la DB')
    query = f'INSERT INTO cliente VALUES(NULL, "{user.first_name}", "default@gmamil.com","", "{user.username}", "",0)'
    execute_query(connection, query)
    print(query)
  return


# In[18]:


#=============================================
   # FUNCION PARA VERIFICAR SUSCRIPCION
   # ============================================="""   
def verificarSuscripcion(update , context):
    username = update.message.chat.username
    queryE = f'SELECT client_id from cliente c WHERE c.cliente_nombreUsuario = "{username}"'
    data = execute_read_query(connection, queryE)
    user_ssuscrito = data[0][0]
    
    #=============================================
   # FUNCION PARA ENVIAR LOS VERSICULOS
   # =============================================
def enviarVersiculo(context):
    try:
          for user_id, user_data in context.dispatcher.user_data.items():
                print("user_id:: ",user_id)
                print("user_data:: ", user_data['username'])
                if 'username' in user_data.keys():
                    print("olita if username: ",user_data['username'])
                    username = user_data['username']
                    queryE = f'SELECT cliente_suscrito from cliente c WHERE c.cliente_nombreUsuario = "{username}"'
                    data = execute_read_query(connection, queryE)
                    user_suscrito = data[0][0]
                    print("user_suscrito: ",user_suscrito)
                    if(user_suscrito==1):
                        id_index = user_data['usser_id']
                        context.bot.send_message(chat_id=id_index,  text=generarVersiculo()) 
       
    except TypeError as e:
        print(e)
        print("handled successfully")

    


# # Conexion a telegram

# In[ ]:


#=============================================
   # FUNCION MAIN
   # ============================================="""   

def main():
    updater = Updater("5602068962:AAHx1JnpjxUk6UfFMbadqRpmT_aDU_Mf66g",use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start",start_comando, pass_job_queue=True))
    dp.add_handler(CommandHandler("ayuda", ayuda_comando))
    
    
    # Controladores de mensajes
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message, pass_job_queue=True))
    dp.add_handler(MessageHandler(Filters.location, LocationMessageEvent))
    dp.add_handler(CallbackQueryHandler(queryHandler))
    
    # Optional handler if your product requires shipping
    dp.add_handler(ShippingQueryHandler(shipping_callback))
    # Pre-checkout handler to final check
    dp.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()


# In[ ]:




