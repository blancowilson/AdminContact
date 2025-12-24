import re

def verify_phone_number(phone_number):
    """Valida, limpia y almacena un número de teléfono.

    Args:
        telefono: El número de teléfono a validar.
        telefonos_almacenados: La lista donde se almacenarán los teléfonos validados.

    Returns:
        True si el teléfono fue validado y almacenado, False en caso contrario.
    """

    if not isinstance(phone_number, str):
        print(f"Entrada no válida: {phone_number} (Debe ser una cadena)")
        return False

    telefonos_limpios = []
    
    # Manejo de múltiples números separados por :::
    for num in phone_number.split(":::"):
        num = num.strip()

        # Eliminar espacios, guiones, puntos y otros caracteres no numéricos
        num_limpio = re.sub(r"[ \-\.,]", "", num)

        if not num_limpio:
            continue

        if num_limpio.startswith("0"):
            num_limpio = "+58" + num_limpio[1:]
        elif num_limpio.startswith(tuple(map(str, range(212,296))) or tuple(map(str, range(412,427)))):
            num_limpio = "+58" + num_limpio
        elif num_limpio.startswith("+1"):
            num_limpio = num_limpio
        elif num_limpio.startswith("+5"):
            num_limpio = num_limpio
        elif num_limpio.startswith("1"):
            num_limpio = "+1" + num_limpio
        else:
            print(f"Número no reconocido: {num}")
            return False

        telefonos_limpios.append(num_limpio)

    # Almacenar los teléfonos limpios en la lista principal
    # telefonos_almacenados.extend(telefonos_limpios) # Usamos extend para agregar los elementos de la lista telefonos_limpios individualmente
    return num_limpio


# Ejemplo de uso:
telefonos_a_validar = [
    "04148224570",
    "+51943 013 946",
    "+584145838527",
    "04144207623",
    "0412-8887309",
    "+584124978300",
    "0414-4054203",
    "0414-4402450 ::: 0414-4051351",
    "+584265440877",
    "+58 412-3262995",
    "texto no valido", #ejemplo de texto no valido
    1234, #ejemplo de numero no valido
    "+58 412-4774799",
    "+584149425266",
    "0416-4456-531",
    "+58 424-5177988",
    "0414-5843330",
    "0414-9401566",
    "+58 414-5980771",
    "+58 412-4029683",
    "+58 412-6474466",
    "0412-4029683",
    "04264340581",
    "0424-4479390 ::: 0412-4070042",
    "042-442-48797",
    "0245-9957-828",
    "0412-8855907",
    "+58 424-4083796",
    "0416-6416-007",
    "04128985187",
    "0414-4292019",
    "0412-1576-853",
    "+58 426-2205249",
    "+507 6579-7715",
    "0426-2243-230",
    "+584244358600",
    "+18148809578",
    "+58 414-3594515",
    "0424-4338-265",
    "0414-4963-222",
    "0424-1543-459",
    "0426-8377-172",
    "+58 424-4188118",
    "0412-4082-851",
    "+584246031804",
    "0412-7416372 ::: 0414-3496209",
    "241-831.84.41"
]

telefonos_validados = []

for telefono in telefonos_a_validar:
    if verify_phone_number(telefono):
        print(f"Teléfono(s) '{telefono}' validado(s) y almacenado(s).")
    
print("-" * 20)
# print("Teléfonos validados y almacenados:")
# print(telefonos_validados)


