import tkinter as tk, requests, serial,time, re, os
from xml.etree import ElementTree
from tkinter import messagebox
from PIL import ImageTk,Image 
from datetime import datetime
from threading import Timer
####Configuración inicial del programa   ##################################
window = tk.Tk()
window.attributes("-fullscreen", True)
#window.geometry("770x480")

global filtro, cantidad_escaneo, modelo
error = 0
filtro = 0
cantidadPasoFinal = 0

cantidad_escaneo = 0
mensaje = ""
modelo = ""

###Método con todo el diseño de la interfaz principal ##################################
def iniciar():
    try: 
        global datos_entrada, campo_informacion, ventanaPrincipal
        global boton_uno, boton_dos, boton_tres, boton_cuatro, cantidad_seleccion



        ventanaPrincipal = tk.Frame(window)
        ventanaPrincipal.pack(fill="both", expand="yes")

        ### Tamaño de los números de los botones, su ancho y espacio en Y y X ##################################
        numero_size = ("arial", 33)
        ancho_boton = 5
        espacio_botonx = 5
        espacio_botony = 5
        
        ### Creando las variables de botones como null ##################################
        boton_uno = boton_dos = boton_tres = boton_cuatro = None

        botonFrame = tk.Frame(ventanaPrincipal)
        botonFrame.place(x = 240, y = 15)

        filaUno = tk.Frame(botonFrame)
        filaUno.pack()
        filaDos = tk.Frame(botonFrame)
        filaDos.pack()

        ###Botones de selección de imágenes de PARAMETRIC ##################################
        boton_uno = tk.Button(filaUno, text= "1", font = numero_size, width = ancho_boton, 
            command = lambda: seleccionEscaneo(boton_uno, reset= True ) )
        boton_uno.pack(side = tk.LEFT, padx = espacio_botonx, pady = espacio_botony)

        boton_dos = tk.Button(filaUno, text= "2", font = numero_size, width = ancho_boton,
            command = lambda: seleccionEscaneo(boton_dos, reset= True ) )
        boton_dos.pack(side = tk.LEFT, padx = espacio_botonx, pady = espacio_botony)

        boton_tres = tk.Button(filaDos, text= "3", font = numero_size, width = ancho_boton,
            command = lambda: seleccionEscaneo(boton_tres, reset= True ) )
        boton_tres.pack(side = tk.LEFT, padx = espacio_botonx, pady = espacio_botony)

        boton_cuatro = tk.Button(filaDos, text= "4", font = numero_size, width = ancho_boton,
            command = lambda: seleccionEscaneo(boton_cuatro, reset= True))
        boton_cuatro.pack(side = tk.LEFT, padx = espacio_botonx, pady = espacio_botony)


        ###Botón ALL: habilita todos los botones de selección ##################################
        boton_all = tk.Button(ventanaPrincipal, text= "ALL", font =  ("arial", 25), width = 10, bg = "SeaGreen1",
            command = lambda: seleccionEscaneo(all = True, reset= True ) )
        boton_all.place(x = 20, y = 15)
        ###Botón CLEAR: deshabilita todos los botones de selección ##################################
        boton_clear = tk.Button(ventanaPrincipal, text= "CLEAR", font =  ("arial", 25), width = 10, bg = "SkyBlue1",
            command = lambda: seleccionEscaneo(clear = True, reset= True))
        boton_clear.place(x = 570, y = 15)
        ###Botón CONF: modo soporte, para configuración del programa, usar teclado o teclas ##################################
        boton_conf = tk.Button(ventanaPrincipal, text= "CONF", font =  ("arial", 25), width = 10, bg = "grey",
            command = ventanaPassword )
        boton_conf.place(x = 20, y = 100)
        ###Botón OK: para cerrar ventana emergente. Llama a función que envía un dato por com serial al arduino para enviar un Enter ####
        boton_ok = tk.Button(ventanaPrincipal, text= "OK", font =  ("arial", 25), width = 10, height = 2,bg = "SkyBlue1",
            command = lambda: enviarDatos("OK"))
        boton_ok.place(x = 570, y = 80)


        serialFrame = tk.Frame(ventanaPrincipal)
        serialFrame.place(x = 50, y = 190)

        serial_label = tk.Label(serialFrame, text = "SERIAL", font = ("arial", 20))
        serial_label.pack()

        datos_entrada = tk.Entry(serialFrame, width = 40, font = ("arial", 20))
        datos_entrada.pack(side = tk.LEFT)
        datos_entrada.focus()
        datos_entrada.bind('<Return>', lambda event: retenerSeriales(event, datos_entrada.get()))
        cantidad_seleccion = tk.Label(serialFrame, text = "", font = ("arial bold", 30))
        cantidad_seleccion.pack(side = tk.LEFT)


        respuestaFrame = tk.Frame(ventanaPrincipal)
        respuestaFrame.place(x = 20, y = 270)

        respuesta_label = tk.Label(respuestaFrame, text = "RESPUESTA", font = ("arial", 15))
        respuesta_label.pack()

        campo_informacion = tk.Text(respuestaFrame, width = 75, height = 7, font =("arial", 14))
        campo_informacion["state"] = "disabled"
        campo_informacion.pack()
        ### Configuro los botones en color verde, que el programa entiende como habilitados
        boton_uno["bg"] = boton_dos["bg"] = boton_tres["bg"] = boton_cuatro["bg"] = "green"
    except Exception as e:
        escribirLogFallas("iniciar(): " + str(e))

    

def seleccionEscaneo(objeto = False, reset = False, all = False, clear = False, mensaje  = ""):
    try:
        global  error, cantidad, cantidad_escaneo, serialesArr, cantidadPasoFinal, modelo
        
        cantidad = 0
        serialesArr = []
        mensaje_serial = ""

        limpiarCampo()
        modelo = ""
        
        if reset == True:
            
            if all == True:
                boton_uno["bg"] = boton_dos["bg"] = boton_tres["bg"] = boton_cuatro["bg"] = "green"
            if clear == True:
                boton_uno["bg"] = boton_dos["bg"] = boton_tres["bg"] = boton_cuatro["bg"] = "grey"
            cantidad_escaneo = 0
            error = 0
            campo_informacion["bg"] = "white"
            
        if objeto != False:
            if objeto["bg"] == "green":
                objeto["bg"] = "grey"
                objeto["activebackground"] = "grey"
            else:
                objeto["bg"] = "green"
                objeto["activebackground"] = "green"


        if boton_uno["bg"] == "green":
            cantidad = cantidad+1
            mensaje_serial += "1"
        else:
            mensaje_serial += "0"
        if boton_dos["bg"] == "green":
            cantidad = cantidad+1
            mensaje_serial += "1"
        else:
            mensaje_serial += "0"
        if boton_tres["bg"] == "green":
            cantidad = cantidad+1
            mensaje_serial += "1"
        else:
            mensaje_serial += "0"
        if boton_cuatro["bg"] == "green":
            cantidad = cantidad+1
            mensaje_serial += "1"
        else:
            mensaje_serial += "0"

        if mensaje_serial == "0000":
            datos_entrada["state"] = "disabled"
        else:
            datos_entrada["state"] = "normal"
        #print(cantidad)

        texto_seleccion = "0" + "/" + str (cantidad)
        cantidad_seleccion["text"] = texto_seleccion

        campo_informacion["state"] = "normal"
        campo_informacion.insert(tk.INSERT, mensaje)
        campo_informacion["state"] = "disabled"
        
        if cantidad_escaneo == cantidad and cantidad != 0:
            if error == 0:
                
                cantidad_escaneo = 0
                confirmacion(mensaje_serial)
            if error == 1:
                datos_entrada.focus()
                campo_informacion["state"] = "normal"
                campo_informacion.insert(tk.INSERT, "Una o más de las unidades no lleva el flujo correcto. Verifica el historial" )
                campo_informacion["bg"] = "red"
                campo_informacion["state"] = "disabled"
                error = 0
                
                cantidad_escaneo = 0
                cantidadPasoFinal = 0
    except Exception as e:
        escribirLogFallas("seleccionEscaneo(): " + str(e))
        
            
            
def timerFunc(opcionTimer):
    try: 
        if opcionTimer == "reinicio":
            seleccionEscaneo(reset=1)
        if  opcionTimer == "cerrar": 
            cerrarVentana()
            seleccionEscaneo(mensaje="Se agotó tiempo de espera en confirmación")
    except Exception as e:
        escribirLogFallas("timerFunc(): " + str(e))

def retenerSeriales(event, serial):
    try: 
        global cantidad_escaneo, serialesArr, datos_entrada, seriales2DArray, serialesMasterArray, filtro, mensaje, modelo, error, tiempoReinicio
        if serial == "":
            return
        if cantidad_escaneo <= cantidad:
            seriales2DArray = []
            serialesMasterArray = []
            cantidad_escaneo += 1
            texto_seleccion = str(cantidad_escaneo) + "/" + str (cantidad)
            cantidad_seleccion["text"] = texto_seleccion
            limpiarCampo()
            if cantidad_escaneo == 1:
                try:
                    if tiempoReinicio.is_alive():
                        tiempoReinicio.cancel()
                        
            
                except: 
                    pass
                tiempoReinicio = Timer(20.0, timerFunc, ["reinicio"])
                tiempoReinicio.start()
            

            if serial in serialesArr:
                error = 1
                seleccionEscaneo(reset=  1, mensaje = "Uno de los seriales es repetido\n")
                
                return
            serialesArr.append(serial)
            try:
                datos_entrada.delete('0', 'end')
                
                try:
                    if len(serial.split(",")[1]) > 6:
                        if modelo != "" and modelo != serial.split(",")[0]:
                            seleccionEscaneo(reset=1, mensaje = "Uno de los seriales no pertenece al mismo modelo.\n Modelos:\n- " + modelo + ":\n-"+ serial.split(",")[0])
                            return

                        modelo = serial.split(",")[0]
                    else:
                        if modelo != "" and modelo != serial[0: serial.rindex("-")]:
                            error = 1
                            seleccionEscaneo(reset=1, mensaje = "Uno de los seriales no pertenece al mismo modelo.\n Modelos: " + modelo + ", "+ serial[0: serial.rindex("-")])
                            return
                        modelo = serial[0: serial.rindex("-")]
                except: 
                    messagebox.showinfo(title="ERROR", message="Serial no valido: "+ serial +"\n" + "Asegúrese de escanear el serial 2D")
                    seleccionEscaneo(reset=1)
                    return
                print(modelo)
                if len(serialesArr) == cantidad:
                    tiempoReinicio.cancel()
                    mensaje = ""
                    datos_entrada["state"] = "disabled"
                    window.focus()
                    #datos_entrada.mainloop()
                    window.update()
                    #print("entre")
                    getGolden(serialesArr)
            except Exception as e: 
                print(e)
            filtro = 0
    except Exception as e:
        escribirLogFallas("retenerSeriales(): " + str(e))        
    

def limpiarCampo():
    try: 
        campo_informacion["state"] = "normal"
        campo_informacion.delete('1.0','end')
        campo_informacion["state"] = "disabled"
        datos_entrada.delete('0', 'end')
    except Exception as e:
        escribirLogFallas("limpiarCampo(): " + str(e))

def getGolden(array):

    try: 
        #errorGolden = 0
        url = "http://mxgdlm0webte02/OkToTesterWebServiceInterface/OkToTesterWebServiceInterface.asmx"

        headers = {"Content-Type" : "text/xml; charset=utf-8"}

        body = """<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
        <GetWhiteListFromCustomer xmlns="http://tempuri.org/">
        <customer>ACLARA</customer>
        </GetWhiteListFromCustomer>
        </soap:Body>
        </soap:Envelope>
        """

        ### Convierto texto recibido en XML
        response = requests.post(url, data = body, headers = headers)
        txtmesstep = response.text 
        


        xmlgolden = ElementTree.fromstring(txtmesstep)
        goldentxt = xmlgolden[0][0][0].text
        for i in array:
            time.sleep(0.100)
            if re.search(i, goldentxt):
                
                toMaster(i, isGolden= 1)
            else:
                toMaster(i)

    except Exception as e:
        escribirLogFallas("getGolden(): " + str(e))


def toMaster(serial_2d, isGolden = 0):
    try:
        global filtro
        
        #print("Valor de isGolden: " + str(isGolden))
        try:
            if len(serial_2d) < 12:
                raise Exception("Longitud de serial no valida")
            else:
                if isGolden == 1:
                    raise Exception()
                
                url = "http://mxgdlm0webte02/wsMesInterface/MesWebServiceInterface.asmx"

                headers = {"Content-Type" : "text/xml; charset=utf-8"}
            

                body = """<?xml version="1.0" encoding="utf-8"?>
                <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                <soap:Body>
                <GetBoardHistoryFromMesInstance xmlns="http://tempuri.org/">
                <mesInstance>1</mesInstance>
                <customerID>68</customerID>
                <serialNumber>"""+serial_2d+"""</serialNumber>
                </GetBoardHistoryFromMesInstance>
                </soap:Body>
                </soap:Envelope>"""
                response = requests.post(url, data = body, headers = headers)
                
                txtmes = response.text 
                txtmes2 = txtmes.replace("&lt;", "<").replace("&gt;", ">")
                xmlmes2d = ElementTree.fromstring(txtmes2)

                serialrespuesta = xmlmes2d[0][0][0][0][1].text
                #print(xmlmes2d[0][0][0][0][1].text)

        except:    
            
            url = "http://mxgdlm0webte02//OkToTesterWebServiceInterface/OkToTesterWebServiceInterface.asmx"

            headers = {"Content-Type" : "application/soap+xml; charset=utf-8"}
            body = """<?xml version="1.0" encoding="utf-8"?>
            <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
            <soap12:Body>
            <GetMesSerialFromLinkedCode xmlns="http://tempuri.org/">
            <customer>ACLARA</customer>
            <linkedCode>"""+serial_2d+"""</linkedCode>
            <instance>1</instance>
            </GetMesSerialFromLinkedCode>
            </soap12:Body>
            </soap12:Envelope>"""


            response = requests.post(url, data = body, headers = headers)


            xmlmes2d = ElementTree.fromstring(response.text)
        
            serialrespuesta = xmlmes2d[0][0][0].text

        seriales2DArray.append(serial_2d)
        serialesMasterArray.append(serialrespuesta)
    
    
        if serialrespuesta == "Serial Linked Not Founded" and filtro == 0:

            messagebox.showinfo(title="ERROR", message="Serial no valido: "+ serial_2d +"\n" + "Asegúrese de escanear el serial 2D")
            filtro = 1
            datos_entrada["state"] = "normal"
            seleccionEscaneo(reset=1)
        if len(seriales2DArray) == cantidad and filtro == 0:
            for i, j in zip(seriales2DArray, serialesMasterArray):
                okToTest(i, j, isGolden)
        return
    except Exception as e:
        escribirLogFallas("toMaster(): " + str(e))


def okToTest(serial_2d, serial_master, isGolden):
    try:

        global  error, cantidadPasoFinal, mensaje, modelo, isGoldenGlobal
        
        isGoldenGlobal = isGolden
        #print(serial_2d + " " + serial_master)
        
        url = "http://mxgdlm0tis01/MES-TIS/tis.asmx"

        headers = {"Content-Type" : "application/soap+xml; charset=utf-8"}

        body = """<?xml version="1.0" encoding="utf-8"?>
        <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
        <soap12:Body>
        <GetCurrentRouteStep xmlns="http://jabil.com/GMS/MES_TIS">
        <SerialNumber>"""+serial_master+"""</SerialNumber>
        </GetCurrentRouteStep>
        </soap12:Body>
        </soap12:Envelope>
        """

        try:
            response = requests.post(url, data = body, headers = headers)
            txtmes = response.text 
            txtmes2 = txtmes.replace("&lt;", "<").replace("&gt;", ">")
            xmlmes = ElementTree.fromstring(txtmes2)

            paso = xmlmes[0][0][0][0][0][6].text
            status = xmlmes[0][0][0][0][0][14].text
            tiempoprueba = xmlmes[0][0][0][0][0][12].text

            

            isTimeOK = testtime(tiempoprueba)
            #print(isTimeOK)

        
            if isGolden == 1:
                if paso == "MDA" and status == "Fail":
                    respuesta_programa = "Golden fallada en MDA. No puede probarse"
                    error = 1
                    
                else: 
                    respuesta_programa = "Se puede probar"
                    campo_informacion["bg"] = "white"

            else:
                if paso == "MDA" and status == "Pass" and isTimeOK[2] == True:
                    respuesta_programa = "Se puede probar"
                    campo_informacion["bg"] = "white"
                else:
                    if isTimeOK[2] == False:
                        respuesta_programa = "Necesario: "+isTimeOK[0].strip()+" min. Se probó hace: " + isTimeOK[1] + " min"
                    else:
                        if status == "Fail":
                            respuesta_programa = "Unidad fallada en paso: " + paso
                        else:
                            respuesta_programa = "Último dato: " + paso
                    error = 1
                
                if revisarSerialesBloqueados(serial_2d) == 0:
                    respuesta_programa =  "Esta unidad ya fue escaneada. Debe esperar 10 min para volver a probarla"
                    error = 1
            

            #respuesta_historial =  paso + " " + status 
            mensaje += serial_2d + " " + respuesta_programa + "\n"
            cantidadPasoFinal += 1
            
            if cantidadPasoFinal == cantidad:
                
                seleccionEscaneo(mensaje = "[MODELO: " + modelo + "]\n" + mensaje)

        except Exception as e:
            messagebox.showinfo(title="ERROR", message="Ocurrió un error\n Verifique el serial. " + str(e) )
            datos_entrada["state"] = "normal"

    except Exception as e:
        escribirLogFallas("okToTest(): " + str(e))        

def confirmacion(mensaje):
    try: 

        global ventanaConfirmar, cantidadPasoFinal, tiempoConfirmar
        cantidadPasoFinal = 0
        ventanaPrincipal.pack_forget()
        ventanaConfirmar  = tk.Frame(window)
        ventanaConfirmar.pack(fill="both", expand="yes")

        avisoLabel = tk.Label(ventanaConfirmar, text = "    CIERRA EL FIXTURE Y BAJA LA PALANCA", font = ("arial", 25))
        avisoLabel.place(x= 20, y = 10)

        tiempoConfirmar = Timer(10.0, timerFunc, ["cerrar"])
        tiempoConfirmar.start()

        try:
            imgdb = ImageTk.PhotoImage(Image.open("imagen/fixture.png").resize((300, 250)))
        except:
            imgdb = ImageTk.PhotoImage(Image.open("/home/pi/Documents/oktotest_pmc/imagen/fixture.png").resize((300, 250)))
            
        labeldb = tk.Label(ventanaConfirmar, image = imgdb)
        labeldb.place(x = 220, y = 90)


        btnConfirmar = tk.Button(ventanaConfirmar, text = "LISTO",activebackground = "green" ,command = lambda x = mensaje: enviarDatos(x, 1), font = ("arial", 20), bg = "green", width = 10, height = 8)
        btnConfirmar.place(x = 580, y = 80)
        btnCancelar = tk.Button(ventanaConfirmar, text = "CANCELAR",activebackground = "red", command = cerrarVentana, font = ("arial", 20), bg = "red", width = 10, height = 8)
        btnCancelar.place(x = 10, y = 80)
        ventanaPrincipal.mainloop()
    except Exception as e:
        escribirLogFallas("confirmacion(): " + str(e))    

def enviarDatos(datos, confirmacion = 0):
    try:
        ser = serial.Serial('/dev/ttyAMA0',9600)  
        ser.write(datos.encode())
        ser.close()
        datos_entrada.focus()
        if confirmacion == 1:
            cerrarVentana()
            
            #print("GoldenGLobal = " + str(isGoldenGlobal))
            if isGoldenGlobal == 0:
                bloquearSeriales()
    except Exception as e:
        escribirLogFallas("enviarDatos(): " + str(e))


def ventanaPassword():
    try:
        global ventanaPassword

        def pass_verify(password_reset):
            if password_reset == "aclara":
                cerrarVentanaPassword()
                panelDeControl()
                
            else: 
                label_password["fg"] = "red"
                input_password.delete('0', 'end')


        cerrarVentanaPassword()
        x = window.winfo_rootx()
        y = window.winfo_rooty()
        ventanaPassword = tk.Toplevel(bg = "ivory4")
        ventanaPassword.geometry("%dx%d+%d+%d" % (500, 300, x+200 , y+100))
        ventanaPassword.resizable(False, False)
        ventanaPassword.overrideredirect(1)

        label_password = tk.Label(ventanaPassword, text = "PASSWORD", font = ("arial", 20))
        label_password.pack(pady = 20)

        input_password = tk.Entry(ventanaPassword,  font = ("arial", 20))
        input_password.pack(pady = 20)
        input_password.focus()
        input_password.bind('<Return>', lambda event: pass_verify(input_password.get()))
        

        boton_cerrar = tk.Button(ventanaPassword ,text = "CANCELAR", command = cerrarVentanaPassword,  font = ("arial", 20))
        boton_cerrar.pack(pady = 20)
    except Exception as e:
        escribirLogFallas("ventanaPassword(): " + str(e))    


def cerrarVentanaPassword():
    try: 
        ventanaPassword.destroy()
    except Exception as e:
        escribirLogFallas("cerrarVentanaPassword(): " + str(e))

def panelDeControl():
    try:
        def seleccionOpcionesPanel(opcionSel, btnObjeto):

            opcion1["bg"] = opcion2["bg"] = opcion3["bg"] = opcion4["bg"] = "grey"
            
            if btnObjeto["bg"] == "grey":
                btnObjeto["bg"] = "white"

            if opcionSel == 1:
                controlFrame.pack_forget()
                generalFrame.pack(side = tk.LEFT, fill = "y")
            if opcionSel == 2:
                generalFrame.pack_forget()
                controlFrame.pack(side = tk.LEFT, fill = "y")
        def salirPanel():
            ventanaPanel.pack_forget()
            ventanaPrincipal.pack(fill="both", expand="yes")

        ventanaPrincipal.pack_forget()
        ventanaPanel  = tk.Frame(window)
        ventanaPanel.pack(fill="both", expand="yes")
        letraSizeMenu = ("arial", 20)
        letraSizeTeclasC =  ("arial", 17)
        letraSizeGeneral = ("arial", 20)

        ############################################MENU##################################################vvv
        try:

            imgFlechaAr = ImageTk.PhotoImage(Image.open("imagen/up.png").resize((70, 70)))
            imgFlechaAb = ImageTk.PhotoImage(Image.open("imagen/down.png").resize((70, 70)))
            imgFlechaD = ImageTk.PhotoImage(Image.open("imagen/right.png").resize((70, 70)))
            imgFlechaI = ImageTk.PhotoImage(Image.open("imagen/left.png").resize((70, 70)))

        except: 
            
            imgFlechaAr = ImageTk.PhotoImage(Image.open("/home/pi/Documents/oktotest_pmc/imagen/up.png").resize((70, 70)))
            imgFlechaAb = ImageTk.PhotoImage(Image.open("/home/pi/Documents/oktotest_pmc/imagen/down.png").resize((70, 70)))
            imgFlechaD = ImageTk.PhotoImage(Image.open("/home/pi/Documents/oktotest_pmc/imagen/right.png").resize((70, 70)))
            imgFlechaI = ImageTk.PhotoImage(Image.open("/home/pi/Documents/oktotest_pmc/imagen/left.png").resize((70, 70)))

        panelMenu =  tk.Frame(ventanaPanel, bg ="yellow")
        panelMenu.pack(side = tk.LEFT, fill = "y")

        opcion1 = tk.Button(panelMenu, text = "General", font = letraSizeMenu, width= 15, bg = "white", 
            command = lambda: seleccionOpcionesPanel(1, opcion1) )
        opcion1.pack()
        opcion2 = tk.Button(panelMenu, text = "Control Teclas", font = letraSizeMenu, width= 15, bg = "grey",
            command = lambda: seleccionOpcionesPanel(2, opcion2) )
        opcion2.pack()
        opcion3 = tk.Button(panelMenu, text = "Tiempo de Espera", font = letraSizeMenu, width = 15, bg = "grey")
        opcion3.pack()
        opcion4 = tk.Button(panelMenu, text = "Salir", font = letraSizeMenu, width = 15, bg = "grey",
            command = salirPanel)
        opcion4.pack()

        ############################################GENERAL##################################################vvv

        generalFrame = tk.Frame(ventanaPanel)
        generalFrame.pack(side = tk.LEFT, fill = "y")


        modoELabel = tk.Label(generalFrame, text = "MODO ESTRICTO ", font = letraSizeGeneral)
        modoELabel.grid(column = 1, row = 1)
        modoEBtn = tk.Button(generalFrame, text = modoESel, width = 3, font = letraSizeGeneral)
        modoEBtn.grid(column = 2, row = 1)

        bloqueoLabel = tk.Label(generalFrame, text = "BLOQUEAR SELECCIÓN ", font = letraSizeGeneral)
        bloqueoLabel.grid(column = 1, row = 2)
        bloqueoBtn = tk.Button(generalFrame, text = bloqueoSel, width = 3, font = letraSizeGeneral)
        bloqueoBtn.grid(column = 2, row = 2)



        ############################################CONTROL TECLAS###########################################vvv

        controlFrame = tk.Frame(ventanaPanel)
        #controlFrame.pack(side = tk.LEFT, fill = "y")

        controlOpciones = tk.Frame(controlFrame)
        controlOpciones.pack(side = tk.LEFT, padx = 50)


        btnF11 = tk.Button(controlOpciones, text = "TEST PLAN", width= 10, font = letraSizeTeclasC, bg = "cyan"
        , command = lambda : enviarDatos("TESTPLAN"))
        btnF11.grid(column = 1, row = 0, pady = 15)
        btnF11 = tk.Button(controlOpciones, text = "F11", width= 8, font = letraSizeTeclasC, bg = "cyan"
        , command = lambda : enviarDatos("1111"))
        btnF11.grid(column = 1, row = 1, pady = 15)
        btnTab = tk.Button(controlOpciones, text = "Tab", width= 8, font = letraSizeTeclasC, bg = "cyan"
        , command = lambda : enviarDatos("TAB"))
        btnTab.grid(column = 1, row = 2, pady = 15)
        btnEnter = tk.Button(controlOpciones, text = "Enter", width= 8, font = letraSizeTeclasC, bg = "green"
        , command = lambda : enviarDatos("OK"))
        btnEnter.grid(column = 1, row = 3, pady = 15)
        btnEnter = tk.Button(controlOpciones, text = "Espacio", width= 8, font = letraSizeTeclasC, bg = "cyan"
        , command = lambda : enviarDatos("ESPACIO"))
        btnEnter.grid(column = 1, row = 4, pady = 15)


        
        btnAltF4 = tk.Button(controlOpciones, text = "Alt+F4", width= 8, font = letraSizeTeclasC, bg = "cyan"
        , command = lambda : enviarDatos("CERRAR"))
        btnAltF4.grid(column = 1, row = 5, pady = 90)

        flechasFrame = tk.Frame(controlFrame)
        flechasFrame.pack(side = tk.LEFT,  padx = 30)


        btnAr = tk.Button(flechasFrame, image = imgFlechaAr, command = lambda : enviarDatos("UP"))
        btnAr.grid(column = 2, row = 1)

        
        btnI = tk.Button(flechasFrame, image = imgFlechaI, command = lambda : enviarDatos("LEFT"))
        btnI.grid(column = 1, row = 2)
        btnD = tk.Button(flechasFrame, image = imgFlechaD, command = lambda : enviarDatos("RIGHT"))
        btnD.grid(column = 3, row = 2)
        btnAb = tk.Button(flechasFrame, image = imgFlechaAb, command = lambda : enviarDatos("DOWN"))
        btnAb.grid(column = 2, row = 3)


        ventanaPanel.mainloop()
    except Exception as e:
        escribirLogFallas("panelDeControl(): " + str(e))

def cerrarVentana():
    try:
        global filtro, cantidad_escaneo, cantidad, serialesArr
        global tiempoConfirmar
        tiempoConfirmar.cancel()
        ventanaConfirmar.destroy()
        ventanaPrincipal.pack(fill="both", expand="yes")
        cantidad_escaneo  = 0
        texto_seleccion = "0" + "/" + str (cantidad)
        cantidad_seleccion["text"] = texto_seleccion
        serialesArr = []
        datos_entrada.focus()
        limpiarCampo()
    except Exception as e:
        escribirLogFallas("cerrarVentana(): " + str(e))    

def initConf():
    try:
        global modoESel, bloqueoSel
        try:
            archivoconf = open('conf.conf', 'r')
        except: 
            archivoconf = open('/home/pi/Documents/oktotest_pmc/conf.conf', 'r')
        textosBtn = []
        while True:
            # Get next line from file
            line = archivoconf.readline()
            if re.search("=1", line):
                textosBtn.append("SÍ")
            else:
                textosBtn.append("NO")

            if not line:
                break

        archivoconf.close()
        modoESel = textosBtn[0]
        bloqueoSel = textosBtn[1]
    except Exception as e:
        escribirLogFallas("initConf(): " + str(e))

def testtime(tiempo):
    try:
        formatodia = tiempo[0: tiempo.find("T")]
        formatohora = tiempo[tiempo.find("T") + 1: tiempo.find("T") + 9]
        formatodiaarray =  formatodia.split("-")
        formatohoraarray = formatohora.split(":")
        anio = int(formatodiaarray[0])
        mes = int(formatodiaarray[1])
        dia = int(formatodiaarray[2])

        h = int(formatohoraarray[0])
        m = int(formatohoraarray[1])
        s = int(formatohoraarray[2])

        diferencia = datetime(anio, mes, dia, h, m, s)

        duracion = datetime.now() - diferencia
        duracionsegundos = duracion.total_seconds()
        duracionminutos = duracionsegundos/60

        print(duracionminutos)
        try:
            archivotexto = open('testtime.txt', 'r')
        except: 
            archivotexto = open('/home/pi/Documents/oktotest_pmc/testtime.txt', 'r')

        resultado = []
        while True:
            
            line = archivotexto.readline()
            if re.search(modelo + "=", line):
                minutosespera = line.split("=")[1]
                if duracionminutos < int(minutosespera):
                    archivotexto.close()
                    resultado = [minutosespera ,str(int(duracionminutos)), False]
                    return resultado
                else:
                    archivotexto.close()
                    resultado = ["", "", True]
                    return resultado
            if not line:
                break
        resultado = ["", "", True]
        archivotexto.close()
        return resultado
    except Exception as e:
        escribirLogFallas("testtime(): " + str(e))

def revisarSerialesBloqueados(serial):
    try:
        puedeProbarse = 1
        
        try:
            ruta = "serialesbloqueados.txt"
            listaBloqueadostxt = open(ruta, "r")
        except: 
            ruta = "/home/pi/Documents/oktotest_pmc/serialesbloqueados.txt"
            listaBloqueadostxt = open(ruta, "r")

        
        #listaBloqueadostxt.seek(0)
        while True:
            linea = listaBloqueadostxt.readline()
            if not linea:
                break
            
            if re.search(serial, linea):
                
                diferencia =  datetime.now() - datetime.fromisoformat(linea.split("#T")[1].strip())
                diferenciasegundos = diferencia.total_seconds()
                diferenciaminutos = int(diferenciasegundos/60)
                #print(diferenciaminutos)
                #print(diferenciaminutos<10)
                if diferenciaminutos<10:
                    puedeProbarse = 0

        
        listaBloqueadostxt.close
        return puedeProbarse
    except Exception as e:
        escribirLogFallas("revisarSerialesBloqueados(): " + str(e))

def bloquearSeriales():
    try:
        global seriales2DArray
        arrayListaBloqueados = []
        try:
            ruta = "serialesbloqueados.txt"
            listaBloqueadostxt = open(ruta, "r")
        except: 
            ruta = "/home/pi/Documents/oktotest_pmc/serialesbloqueados.txt"
            listaBloqueadostxt = open(ruta, "r")
        #os.remove(ruta)
        arrayListaBloqueados = listaBloqueadostxt.readlines()
        listaBloqueadostxt.close()

        listaBloqueadostxt = open(ruta, "w")
        for serial in seriales2DArray:
            arrayListaBloqueados.append(serial+" #T"+ str(datetime.now())+"\n" )
            #print(arrayListaBloqueados)
            if len(arrayListaBloqueados) > 10:
                arrayListaBloqueados.pop(1)
        listaBloqueadostxt.writelines(arrayListaBloqueados)
        listaBloqueadostxt.close()
    except Exception as e:
        escribirLogFallas("bloquearSeriales(): " + str(e))

def escribirLogFallas(error):
    
    try:
        ruta = "log.txt"
        log = open(ruta, "a")
    except: 
        ruta = "/home/pi/Documents/oktotest_pmc/log.txt"

    log.write(error + "   " + str(datetime.now()) + "\n")
    log.write("-----------------------------------------------------------------" + "\n")
    log.close

iniciar()
initConf()
seleccionEscaneo(reset=1)

window.mainloop()

            