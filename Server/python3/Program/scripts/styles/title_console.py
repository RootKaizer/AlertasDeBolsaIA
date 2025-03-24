def mostrar_titulo_estrategia(estrategia):
    """
    Muestra un título destacado con la estrategia seleccionada.
    :param estrategia: Nombre de la estrategia.
    """
    titulo = f"{estrategia.upper()} "
    borde = "*" * (len(titulo) + 4)
    print("\n" + borde)
    print(f"{titulo}")
    print(borde + "\n")