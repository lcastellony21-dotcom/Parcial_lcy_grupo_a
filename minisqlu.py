import re


# ANÁLISIS LÉXICO 
def analisis_lexico(instruccion):
    tokens = []
    partes = instruccion.replace(";", " ;").split()

    for token in partes:
        # Reservadas EXACTAS
        if token == "INSERT" or token == "SHOW":
            tokens.append(("RESERVADA", token))
        elif token == "estudiante" or token == "curso":
            tokens.append(("RESERVADA", token))
        elif token == ";":
            tokens.append(("FIN", token))
        # Identificadores genéricos (letras, números y guion)
        elif re.match(r'^[A-Za-z0-9-]+$', token):
            tokens.append(("IDENTIFICADOR", token))
        else:
            return None, f"Error: token inválido ({token})"

    return tokens, None



# ANÁLISIS SINTÁCTICO

def analisis_sintactico(tokens):
    try:
        # INSERT estudiante <nombre> <codigo> ;
        if tokens[0][1] == "INSERT" and tokens[1][1] == "estudiante":
            if len(tokens) != 5 or tokens[4][0] != "FIN":
                return "Error: Sintaxis incorrecta en INSERT estudiante"

        # INSERT curso <nombre> <codigo> ;
        elif tokens[0][1] == "INSERT" and tokens[1][1] == "curso":
            if len(tokens) != 5 or tokens[4][0] != "FIN":
                return "Error: Sintaxis incorrecta en INSERT curso"

        # SHOW estudiante <nombre> ;
        elif tokens[0][1] == "SHOW" and tokens[1][1] == "estudiante":
            if len(tokens) != 4 or tokens[3][0] != "FIN":
                return "Error: Sintaxis incorrecta en SHOW estudiante"

        # SHOW curso <codigo> ;
        elif tokens[0][1] == "SHOW" and tokens[1][1] == "curso":
            if len(tokens) != 4 or tokens[3][0] != "FIN":
                return "Error: Sintaxis incorrecta en SHOW curso"

        else:
            return "Error: Sintaxis desconocida"
    except IndexError:
        return "Error: Sintaxis incompleta"

    return None



# ANÁLISIS SEMÁNTICO (regex)
def analisis_semantico(tokens):
    # INSERT estudiante <nombre> <codigo>
    if tokens[0][1] == "INSERT" and tokens[1][1] == "estudiante":
        nombre = tokens[2][1]
        codigo = tokens[3][1]
        if not re.match(r'^[A-Za-z]+$', nombre):
            return f"Error: nombre de estudiante inválido ({nombre})"
        if not re.match(r'^202[0-9]-[0-9]{5}$', codigo):
            return f"Error: código de estudiante inválido ({codigo})"

    # INSERT curso <nombre> <codigo>
    elif tokens[0][1] == "INSERT" and tokens[1][1] == "curso":
        nombre = tokens[2][1]
        codigo = tokens[3][1]
        if not re.match(r'^[A-Za-z]+$', nombre):
            return f"Error: nombre de curso inválido ({nombre})"
        if not re.match(r'^[A-Z]{3}[0-9]{3}$', codigo):
            return f"Error: código de curso inválido ({codigo})"

    # SHOW estudiante <nombre>
    elif tokens[0][1] == "SHOW" and tokens[1][1] == "estudiante":
        nombre = tokens[2][1]
        if not re.match(r'^[A-Za-z]+$', nombre):
            return f"Error: nombre de estudiante inválido ({nombre})"

    # SHOW curso <codigo>
    elif tokens[0][1] == "SHOW" and tokens[1][1] == "curso":
        codigo = tokens[2][1]
        if not re.match(r'^[A-Z]{3}[0-9]{3}$', codigo):
            return f"Error: código de curso inválido ({codigo})"

    return None



def ejecutar(instruccion):
    tokens, error = analisis_lexico(instruccion)
    if error:
        return error

    if tokens is None:
        return "Error: análisis léxico fallido"

    error_sintaxis = analisis_sintactico(tokens)
    if error_sintaxis:
        return error_sintaxis

    error_semantico = analisis_semantico(tokens)
    if error_semantico:
        return error_semantico

    return "Instrucción válida: ejecutada"



def main():
    with open("programa.txt", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            
            linea = linea.split("#")[0].strip()
            if linea == "":
                continue
            resultado = ejecutar(linea)
            print(resultado)


if __name__ == "__main__":
    main()
