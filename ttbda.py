# Autores: Lucía Conde Fuentes (l.conde@udc.es) Julia Roade Conejo (julia.roade@udc.es)
# Data de creación: 19-01-2021
#

import psycopg2
import psycopg2.extras
import psycopg2.errorcodes
import sys
import psycopg2.extensions

## ------------------------------------------------------------
##Función para conectarnos coa base de datos
##-------------------------------------------------------------
def connect_db():
    try:
        conn = psycopg2.connect("")
        conn.autocommit = False
        return conn
    except psycopg2.Error as e:
        print(f"Imposible connectar: {e}. Abortando programa")
        sys.exit(1)

## ------------------------------------------------------------
##Función para saír da base de datos
##-------------------------------------------------------------
def disconnect_db(conn):
    conn.commit()
    conn.close()

## ------------------------------------------------------------
##Función para engadir un can á base de datos
##-------------------------------------------------------------
def add_can(conn):
    """
        Crea e engade un novo Can á BD da protectora cos datos introducidos polo
        usuario
    """
    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED

    chip = input("Introduce o número do chip do can: ")
    if not chip.isnumeric():
        return print("Error código de chip incorrecto debe ser un número")
    if len(chip)!=15:
        return print("Error código de chip incorrecto debe tener 15 dígitos")
    
    if chip=="":
        chip=None

    nome = input ("Introduce o nome do novo can: ")
    if nome=="":
        nome=None
    observacions = input ("Introduce algunhas observacións necesarias: ")

    sql= """
        insert into can (codchip,nome,observacions,DNI_apadriñante) 
        VALUES  (%(chip)s,%(nome)s,%(observacions)s,NULL)
    """
    
    with conn.cursor() as cur:                                      
        try:                     
            cur.execute(sql,{'chip':chip,'nome':nome,'observacions':observacions})
            conn.commit()
            print('Can con chip:',chip,', nome:', nome, ', observacións:', observacions, ' e DNI do apadriñante: None engadida correctamente')
            
        except psycopg2.Error as e:
            if e.pgcode==psycopg2.errorcodes.NOT_NULL_VIOLATION:
                print("Error: non pode haber campos sen valor")
            elif e.pgcode==psycopg2.errorcodes.UNIQUE_VIOLATION:
                print("Error: xa existe un can co número de chip asociado:",chip,"")
            elif e.pgcode==psycopg2.errorcodes.STRING_DATA_RIGHT_TRUNCATION:
                print("Error: os datos introducidos están fora do límite de caracteres")
            elif e.pgcode==psycopg2.errorcodes.CHECK_VIOLATION:
                print("Error: os datos introducidos deben ser válidos")
            else:
                print(f'Error generico: {e.pgcode}: {e.pgerror}')
            conn.rollback()

## ------------------------------------------------------------
##Función para engadir un apadriñante á base de datos
##-------------------------------------------------------------
def add_apadriñante(conn):
    """
        Crea e engade un novo apadriñante á BD da protectora cos datos introducidos polo
        usuario
    """
    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED

    dni = input ("Introduce o dni do novo apadriñante: ")
    if len(dni)!=9:
        return print("Error: dni incorrecto debe tener 8 dígitos y una letra")
    if not dni[8:9].isalpha():
        return print("Error: dni incorrecto debe tener una letra al final")
    if not dni[1:8].isnumeric():
        return print("Error: dni incorrecto debe tener 8 dígitos al inicio")
    if dni=="":
        dni=None
    
    nome = input ("Introduce o nome do novo apadriñante: ")
    if nome=="":
        nome=None
    apelido1 = input ("Introduce o primeiro apelido do novo apadriñante: ")
    if apelido1=="":
        apelido1=None
    apelido2 = input ("Introduce o segundo apelido do novo apadriñante: ")
    if apelido2=="":
        apelido2=None

    sql= """
        insert into apadriñante (DNI,nome,apelido1,apelido2,codcuota) 
        VALUES  (%(DNI)s,%(nome)s,%(apelido1)s,%(apelido2)s,NULL)
    """
    
    with conn.cursor() as cur:                                      
        try:                     
            cur.execute(sql,{'DNI':dni,'nome':nome,'apelido1':apelido1,'apelido2':apelido2})
            conn.commit()
            print('Apadriñante con DNI:',dni,', nome:', nome,', apelidos:', apelido1,'', apelido2,' e código de cuota: None engadida correctamente')
            
        except psycopg2.Error as e:
            if e.pgcode==psycopg2.errorcodes.NOT_NULL_VIOLATION:
                print("Error: non pode haber campos sen valor")
            elif e.pgcode==psycopg2.errorcodes.UNIQUE_VIOLATION:
                print("Error: xa existe un apadriñante co DNI asociado:",dni,"")
            elif e.pgcode==psycopg2.errorcodes.STRING_DATA_RIGHT_TRUNCATION:
                print("Error: os datos introducidos están fora do límite de caracteres")
            elif e.pgcode==psycopg2.errorcodes.CHECK_VIOLATION:
                print("Error: os datos introducidos deben ser válidos")
            else:
                print(f'Error generico: {e.pgcode}: {e.pgerror}')
            conn.rollback()

## ------------------------------------------------------------
##Función para engadir unha cuota á base de datos
##-------------------------------------------------------------
def add_cuota(conn):
    """
        Crea e engade unha nova cuota á BD da protectora cos datos introducidos polo
        usuario
    """
    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED

    codcuota = input("Introduce o Código da nova cuota: ")
    if not codcuota.isnumeric():
        return print("Error: código da cuota incorrecto debe ser un número")
    if codcuota=="":
        codcuota=None
    nome = input ("Introduce o nome da nova cuota: ")
    if nome=="":
        nome=None
    valor = input ("Introduce o valor en euros da nova cuota: ")
    if not valor.isnumeric():
        return print("Error: valor da cuota incorrecto debe ser un número")


    sql= """
        insert into cuota (codcuota,nome,valor) 
        VALUES  (%(codcuota)s,%(nome)s,%(valor)s)
    """
    
    with conn.cursor() as cur:                                      
        try:                     
            cur.execute(sql,{'codcuota':codcuota,'nome':nome,'valor':valor})
            conn.commit()
            print('Cuota con código:',codcuota,', nome:', nome, ' e valor:',valor, '€   engadida correctamente')
            
        except psycopg2.Error as e:
            if e.pgcode==psycopg2.errorcodes.NOT_NULL_VIOLATION:
                print("Error: non pode haber campos sen valor")
            elif e.pgcode==psycopg2.errorcodes.UNIQUE_VIOLATION:
                print("Error: xa existe unha cuota co código asociado:",codcuota,"")
            elif e.pgcode==psycopg2.errorcodes.STRING_DATA_RIGHT_TRUNCATION:
                print("Error: os datos introducidos están fora do límite de caracteres")
            elif e.pgcode==psycopg2.errorcodes.CHECK_VIOLATION:
                print("Error: os datos introducidos deben ser válidos")
            elif e.pgcode == psycopg2.errorcodes.NUMERIC_VALUE_OUT_OF_RANGE:
                print("O valor é demasiado grande: debe ser menor de 1000")
            else:
                print(f'Error generico: {e.pgcode}: {e.pgerror}')
            conn.rollback()

## ------------------------------------------------------------
##Función para eliminar un can á base de datos
##-------------------------------------------------------------
def delete_can(conn):
    """
        Elimina o can desexado polo usuario
    """  
    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE
   
    chip = input("Introduce o código do chip do can a eliminar: ")
    if not chip.isnumeric():
        return print("Error código de chip incorrecto debe ser un número")
    if len(chip)!=15:
        return print("Error código de chip incorrecto debe tener 15 dígitos")
    
    if chip=="":
        chip=None
    sql= """ delete from can where codchip=%(chip)s"""
    
    with conn.cursor() as cur:                                               
        try:                               
            cur.execute(sql,{'chip':chip})
            if cur.rowcount == 0:
                print("Non existe un can rexistrado co chip:",chip,"")
            else:
                print("Can con chip:",chip," eliminado")
            conn.commit()
            
        except psycopg2.Error as e:
            if e.pgcode==psycopg2.errorcodes.STRING_DATA_RIGHT_TRUNCATION:
                print("Error: excedido límite de caracteres")
            else:
                print(f'Error generico: {e.pgcode}: {e.pgerror}')
            conn.rollback()


## ------------------------------------------------------------
##Función para mostrar unha cuota da base de datos
##-------------------------------------------------------------       
def show_cuota(conn, control_tx = True):
    """
    Pide por teclado o código dunha cuota e mostra os seus detalles
    :param conn: a conexión aberta á bd
    :return: Nada
    """
    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED

    cod=input("Código da cuota: ")
    if not cod.isnumeric():
        return print("Error: código da cuota incorrecto debe ser un número")
    if cod=="":
        cod=None

    sql= "select codcuota,nome,valor from cuota where codcuota = %(c)s"
    retval = None
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            cursor.execute(sql,{'c':cod})
            row = cursor.fetchone()
            if row is None:
                print("\nA cuota indicada non existe")
            else:
                valor = "Descoñecido" if row['valor'] is None else row['valor']
                print(f"Código: {cod}   Nome: {row['nome']}   Prezo: {valor}")
                retval = cod
            if control_tx:
                conn.commit()
                
        except psycopg2.Error as e:
            print(f"Erro: {e.pgcode} - {e.pgerror}")
        if control_tx:
            conn.rollback()
    return retval

## ------------------------------------------------------------
##Función para mostrar un can da base de datos
##-------------------------------------------------------------
def show_can(conn, control_tx = True):
    """
    Pide por teclado o código do chip dun can e mostra os seus detalles
    :param conn: a conexión aberta á bd
    :return: Nada
    """
    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED

    chip=input("Código do chip do can: ")
    if not chip.isnumeric():
        return print("Error código de chip incorrecto debe ser un número")
    if len(chip)!=15:
        return print("Error código de chip incorrecto debe tener 15 dígitos")
    
    if chip=="":
        chip=None

    sql= "select codchip,nome,observacions,DNI_apadriñante from can where codchip = %(c)s"
    retval = None
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            cursor.execute(sql,{'c':chip})
            row = cursor.fetchone()
            if row is None:
                print("\nO can indicado non existe")
            else:
                print(f"Chip:{chip}   Nome:{row['nome']}   Observacións:{row['observacions']}   DNI do apadriñante:{row[3]}")
                retval = chip
            if control_tx:
                conn.commit()
                
        except psycopg2.Error as e:
            print(f"Erro: {e.pgcode} - {e.pgerror}")
        if control_tx:
            conn.rollback()
    return retval

## ------------------------------------------------------------
##Función para mostrar un apadriñante da base de datos
##-------------------------------------------------------------
def show_apadriñante(conn, control_tx = True):
    """
    Pide por teclado o DNI dun apadriñante e mostra os seus detalles
    :param conn: a conexión aberta á bd
    :return: Nada
    """
    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED

    dni=input("DNI do apadriñante: ")
    if len(dni)!=9:
        return print("Error: dni incorrecto debe tener 8 dígitos y una letra")
    if not dni[8:9].isalpha():
        return print("Error: dni incorrecto debe tener una letra al final")
    if not dni[1:8].isnumeric():
        return print("Error: dni incorrecto debe tener 8 dígitos al inicio")
    if dni=="":
        dni=None

    sql= "select DNI,nome,apelido1,apelido2,codcuota from apadriñante where DNI = %(d)s"
    retval = None
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            cursor.execute(sql,{'d':dni})
            row = cursor.fetchone()
            if row is None:
                print("\nO apadriñante indicado non existe")
            else:
                print(f"DNI:{dni}   Nome:{row['nome']} {row['apelido1']} {row['apelido2']}  Código da cuota que ten asociada:{row[4]}")
                retval = dni
            if control_tx:
                conn.commit()
                
        except psycopg2.Error as e:
            print(f"Erro: {e.pgcode} - {e.pgerror}")
        if control_tx:
            conn.rollback()
    return retval


### ------------------------------------------------------------
##Función para mostrar un apadriñante e os seus cans apadriñados
##-------------------------------------------------------------
def show_apadriñante_and_cans(conn):
    """
        Mostra o apadriñante pedido e os cans que ten apadriñados 
    """    
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)


    dni = show_apadriñante(conn,control_tx=False)
    if dni is None:
        conn.rollback()
        return
    
    sql= """
        select codchip, nome, observacions, can.DNI_apadriñante
        from can
        where DNI_apadriñante = %(d)s
    """
    
    with conn.cursor() as cur:                                      
        try:                     
            cur.execute(sql,{'d':dni})
            row=cur.fetchone()
           
            if row:
                print("\nLista de cans apadriñados:")
                while row:
                    print(f"Can número {cur.rownumber} de {cur.rowcount}:")
                    print(f"-Código do chip: {row[0]}")
                    print(f"-Nome: {row[1]}")
                    print(f"-Observacións: {row[2]}")
                    print("\n")
                    row=cur.fetchone()

            else:
                print("Non hai cans apadriñados polo apadriñante indicado")
            conn.commit()
            
        except psycopg2.Error as e:
            if e.pgcode==psycopg2.errorcodes:
                print('Error: ')
            else:
                print(f'Error xenérico: {e.pgcode}: {e.pgerror}')
            conn.rollback()
    

## ------------------------------------------------------------
##Función para listar unha serie de cuotas da base de datos en base a un valor
##-------------------------------------------------------------
def show_cuotas_by_valor(conn):
    """
    Pide por teclado un valor e mostra as cuotas que teñan un valor inferior a ese
    :param conn: a conexión aberta á bd
    :return: Nada
    """
    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED

    valor=input("Valor da cuota: ")
    if not valor.isnumeric():
        return print("Error: valor da cuota incorrecto debe ser un número")

    sql= "select codcuota,nome,valor from cuota where valor < %(v)s"
    
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
       try:
           cursor.execute(sql,{'v':valor})
           rows = cursor. fetchall()
           for row in rows:
               print(f"Código: {row['codcuota']}   Nome: {row['nome']}   Valor: {row['valor']}")
           print(f"Atopadas {cursor.rowcount} cuotas")
           conn.commit()
               
       except psycopg2.Error as e:
           print(f"Erro: {e.pgcode} - {e.pgerror}")
           conn.rollback()


## ------------------------------------------------------------
##Función para cambiar o valor dunha cuota da base de datos
##-------------------------------------------------------------
def update_cuota(conn):
    """
    Pide por teclado o código dunha cuota e incrementa o seu valor en base a unha porcentaxe que tamén se pedirá
    :param conn: a conexión aberta á bd
    :return: Nada
    """
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)

    cod = show_cuota(conn,control_tx=False)
    if cod is None:
        conn.rollback()
        return
    
    
    incr=input("Incremento (%) da nova cuota: ")
    if not incr.isnumeric():
        return print("Error: valor da cuota incorrecto debe ser un número")
    incr = None if incr=="" else float(incr)

    sql= """
            update cuota
            set valor = valor + valor *(%(i)s/100)
            where codcuota = %(c)s
    """
    with conn.cursor() as cursor:
        try:
            cursor.execute(sql,{'c': cod,'i': incr,})
            conn.commit()
            print("\nValor actualizado correctamente")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.CHECK_VIOLATION:
                print("O valor debe ser positivo: non se modifica o a cuota")
            elif e.pgcode == psycopg2.errorcodes.NUMERIC_VALUE_OUT_OF_RANGE:
                print("O incremento é demasiado grande ou demasiado pequeno: debe ser menor de 1000")
            elif e.pgcode == psycopg2.errorcodes.SERIALIZATION_FAILURE:
                print("Non se pode modificar o valor. Outro usuario xa o modificou")
            else:
                print(f"Erro: {e.pgcode} - {e.pgerror}")
            conn.rollback()

## ------------------------------------------------------------
##Función para cambiar as observacións dun can da base de datos
##-------------------------------------------------------------
def update_can(conn):
    """
    Pide por teclado o código dun chip dun can e cambia as súas observacións a unhas pedidas
    :param conn: a conexión aberta á bd
    :return: Nada
    """
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)
    codchip = show_can(conn,control_tx=False)
    if codchip is None:
        conn.rollback()
        return
    
    
    sob=input("Novas observacións: ")
    ob = None if sob=="" else sob

    sql= """
            update can
            set observacions = %(o)s
            where codchip = %(c)s
    """
    with conn.cursor() as cursor:
        try:
            cursor.execute(sql,{'c': codchip,'o': ob,})
            conn.commit()
            print("\nObservacións actualizadas correctamente")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                print("O código do chip é requerido")
            elif e.pgcode == psycopg2.errorcodes.SERIALIZATION_FAILURE:
                print("Non se poden modificar as observacións. Outro usuario xa o modificou")
            else:
                print(f"Erro: {e.pgcode} - {e.pgerror}")
            conn.rollback()

## ------------------------------------------------------------
##Función para realizar un apadriñamento
##-------------------------------------------------------------
def realizar_apadriñamento(conn):
    """
        Efectua un apadriñamento a partir do DNI da persoa que queira apadriñar, a cuota que vai pagar
        e o chip do can a apadriñar
    """
    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE

    dni = input("Introduce o DNI da persoa que quere apadriñar: ")
    if len(dni)!=9:
        return print("Error: dni incorrecto debe tener 8 dígitos y una letra")
    if not dni[8:9].isalpha():
        return print("Error: dni incorrecto debe tener una letra al final")
    if not dni[1:8].isnumeric():
        return print("Error: dni incorrecto debe tener 8 dígitos al inicio")
    if dni=="":
        dni=None
    cod = input("Introduce o código da cuota que vai pagar (o que xa estaba pagando ou un novo se o desexa): ")
    if not cod.isnumeric():
        return print("Error: código da cuota incorrecto debe ser un número")
    if cod=="":
        cod=None
    chip = input("Introduce o chip do can que se quere apadriñar: ")
    if not chip.isnumeric():
        return print("Error código de chip incorrecto debe ser un número")
    if len(chip)!=15:
        return print("Error código de chip incorrecto debe tener 15 dígitos")
    
    if chip=="":
        chip=None

    sql_select_can = """
        select DNI_apadriñante from can 
        where codchip = %(chip)s
    """
    sql_select_cuota = """
        select codcuota from cuota 
        where codcuota = %(ccu)s
    """
    sql_apadriñante = """
        update apadriñante set codcuota = %(c)s  
        where DNI = %(d)s
    """

    sql_can = """
        update can set DNI_apadriñante = %(d)s 
        where codchip = %(ch)s
    """

    with conn.cursor() as cur:                                      
        try:  
            cur.execute(sql_select_can,{'chip':chip})
            row=cur.fetchone()
            if row and row[0] != dni:
                cur.execute(sql_select_cuota,{'ccu':cod})
                row=cur.fetchone()
           
                if row:
                    cur.execute(sql_apadriñante,{'c':cod,'d':dni})
                    if cur.rowcount == 0:
                        print("Error: DNI", dni, " non válido")
                    else:
                        cur.execute(sql_can,{'d':dni,'ch':chip})
                        if cur.rowcount == 0:
                            print("Error: error de actualización do can")
                        else:  
                            print("A acción de apadriñamento realizouse correctamente")
                else:
                    print("Error: non existe a cuota co código:",cod,"")
            else:
                print("Error: o can indicado non existe ou xa está apadriñado polo apadriñante indicado")

            conn.commit()

        except psycopg2.Error as e:
            if e.pgcode==psycopg2.errorcodes.NOT_NULL_VIOLATION:
                print("Error: ningún campo pode quedar vacío")
            elif e.pgcode==psycopg2.errorcodes.NUMERIC_VALUE_OUT_OF_RANGE:
                print("Error: valores numéricos fóra do rango")
            elif e.pgcode==psycopg2.errorcodes.STRING_DATA_RIGHT_TRUNCATION:
                print("Error: fóra do límite de caracteres")
            else:
                print(f'Error generico: {e.pgcode}: {e.pgerror}')
            conn.rollback()



## ------------------------------------------------------------
##Imprime un menú de opcións, solicita a opción e executa a función asociada. 'q' para saír.
##-------------------------------------------------------------
def menu(conn):
    MENU_TEXT = """
      -- MENÚ DA PROTECTORA --
1 - Engadir can
2 - Engadir apadriñante
3 - Engadir cuota
4 - Eliminar can
5 - Ver apadriñamentos de...
6 - Mostrar apadriñante
7 - Mostrar cuotas polo valor
8 - Mostrar cuota
9 - Mostrar can
10 - Actualizar cuota (Incrementar valor)
11 - Actualizar observacións dun can
12 - Realizar apadriñamento
q - Saír   
"""
    while True:
        print(MENU_TEXT)
        tecla = input('Opción> ')
        if tecla == 'q':
            break
        elif tecla == '1':
            add_can(conn)
        elif tecla == '2':
            add_apadriñante(conn)
        elif tecla == '3':
            add_cuota(conn)
        elif tecla == '4':
            delete_can(conn)
        elif tecla == '5':
            show_apadriñante_and_cans(conn)
        elif tecla == '6':
            show_apadriñante(conn)
        elif tecla == '7':
            show_cuotas_by_valor(conn)
        elif tecla == '8':
            show_cuota(conn)
        elif tecla == '9':
            show_can(conn)
        elif tecla == '10':
            update_cuota(conn)
        elif tecla == '11':
            update_can(conn)
        elif tecla == '12':
            realizar_apadriñamento(conn)


## ------------------------------------------------------------
##Función principal. Conecta á bd e executa o menú. Cando sae do menú, desconecta da bd e remata o programa
##-------------------------------------------------------------
def main():
    """
    Función principal. Conecta á bd e executa o menú.
    Cando sae do menú, desconecta da bd e remata o programa
    """
print('Conectando a PosgreSQL...')
conn = connect_db()
print('Conectado.')
menu(conn)
disconnect_db(conn)

## ------------------------------------------------------------

if __name__ == '__main__':
    main()