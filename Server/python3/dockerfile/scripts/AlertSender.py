import smtplib

def enviar_alerta(mensaje):
    servidor = smtplib.SMTP("smtp.gmail.com", 587)
    servidor.starttls()
    servidor.login("tu_correo@gmail.com", "tu_contraseña")
    servidor.sendmail("tu_correo@gmail.com", "destinatario@gmail.com", mensaje)
    servidor.quit()

# Dentro de la estrategia
def next(self):
    acciones = []

    # Lógica para RSI
    if self.rsi > 70:
        acciones.append("vender")
    elif self.rsi < 30:
        acciones.append("comprar")
    else:
        acciones.append("hold")

    # Lógica para MACD
    if self.macd.macd > self.macd.signal:
        acciones.append("comprar")
    else:
        acciones.append("vender")

    # Enviar alerta si el 70% de las técnicas coinciden
    if acciones.count("comprar") / len(acciones) >= 0.7:
        enviar_alerta("Alerta: COMPRAR")
    elif acciones.count("vender") / len(acciones) >= 0.7:
        enviar_alerta("Alerta: VENDER")