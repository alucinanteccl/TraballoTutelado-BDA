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
def add_can(conn):
    """
        Crea e engade un novo Can á BD da protectora cos datos introducidos polo
        usuario
    """
    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED

    chip = input("Introduce o número do chip do can:")
    if chip=="":
        chip=None

    nome = input ("Introduce o nome do novo can:")
    observacions = input ("Introduce algunhas observacións necesarias:")
    dni = input ("Introduce o dni do seu apadriñante se o ten:")

    sql= """
        insert into can (codchip,nome,observacions,DNI_apadriñante) 
        VALUES  (%(chip)s,%(nome)s,%(observacions)s,%(DNI_apadriñante)s)
    """
    
    with conn.cursor() as cur:                                      
        try:                     
            cur.execute(sql,{'chip':chip,'nome':nome,'observacions':observacions,'DNI_apadriñante':dni})
            conn.commit()
            print('Can con chip:',chip,', nome:', nome, ', observacións:', observacions, ' e DNI do apadriñante:', dni, ' engadida correctamente')
            
        except psycopg2.Error as e:
            if e.pgcode==psycopg2.errorcodes.NOT_NULL_VIOLATION:
                print("Error: non pode haber campos sen valor")
            elif e.pgcode==psycopg2.errorcodes.UNIQUE_VIOLATION:
                print("Error: xa existe un can co número de chip asociado:",chip,"")
            elif e.pgcode==psycopg2.errorcodes.STRING_DATA_RIGHT_TRUNCATION:
                print("Error: os valores introducidos están fora do límite de caracteres")
            elif e.pgcode==psycopg2.errorcodes.CHECK_VIOLATION:
                print("Error: o valor dos datos introducidos debe ser válido")
            else:
                print(f'Error generico: {e.pgcode}: {e.pgerror}')
            conn.rollback()

## ------------------------------------------------------------
def add_apadriñante(conn):
    """
        Crea e engade un novo Can á BD da protectora cos datos introducidos polo
        usuario
    """
    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED

    dni = input ("Introduce o dni do novo apadriñante: ")
    nome = input ("Introduce o nome do novo apadriñante: ")
    apelido1 = input ("Introduce o primeiro apelido do novo apadriñante: ")
    apelido2 = input ("Introduce o segundo apelido do novo apadriñante: ")
    codcuota = input ("Introduce o código da cuota a pagar, para o(s) can(s) apadriñado(s) do novo apadriñante: ")

    sql= """
        insert into apadriñante (DNI,nome,apelido1,apelido2,codcuota) 
        VALUES  (%(DNI)s,%(nome)s,%(apelido1)s,%(apelido2)s,%(codcuota)s)
    """
    
    with conn.cursor() as cur:                                      
        try:                     
            cur.execute(sql,{'DNI':dni,'nome':nome,'apelido1':apelido1,'apelido2':apelido2,'codcuota':codcuota})
            conn.commit()
            print('Apadriñante con DNI:',dni,', nome:', nome,', apelidos', apelido1,'', apelido2,' e código de cuota ',codcuota,'engadida correctamente')
            
        except psycopg2.Error as e:
            if e.pgcode==psycopg2.errorcodes.NOT_NULL_VIOLATION:
                print("Error: non pode haber campos sen valor")
            elif e.pgcode==psycopg2.errorcodes.UNIQUE_VIOLATION:
                print("Error: xa existe un apadriñante co DNI asociado:",dni,"")
            elif e.pgcode==psycopg2.errorcodes.STRING_DATA_RIGHT_TRUNCATION:
                print("Error: os valores introducidos están fora do límite de caracteres")
            elif e.pgcode==psycopg2.errorcodes.CHECK_VIOLATION:
                print("Error: o valor dos datos introducidos debe ser válido")
            else:
                print(f'Error generico: {e.pgcode}: {e.pgerror}')
            conn.rollback()

## ------------------------------------------------------------
def add_cuota(conn):
    """
        Crea e engade un novo Can á BD da protectora cos datos introducidos polo
        usuario
    """
    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED

    codcuota = input("Introduce o Código da nova cuota: ")
    nome = input ("Introduce o nome da nova cuota: ")
    valor = input ("Introduce O valor en euros da nova cuota: ")


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
                print("Error: xa existe un can co número de chip asociado:",codcuota,"")
            elif e.pgcode==psycopg2.errorcodes.STRING_DATA_RIGHT_TRUNCATION:
                print("Error: os valores introducidos están fora do límite de caracteres")
            elif e.pgcode==psycopg2.errorcodes.CHECK_VIOLATION:
                print("Error: o valor dos datos introducidos debe ser válido")
            else:
                print(f'Error generico: {e.pgcode}: {e.pgerror}')
            conn.rollback()

def delete_can(conn):
    """
        Elimina o can desexado polo usuario
    """  
    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE
   
    chip = input("Introduce o código do chip do can a eliminar: ")
    if chip =="":
        chip = None
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
                print("Error: fóra do límite de caracteres")
            else:
                print(f'Error generico: {e.pgcode}: {e.pgerror}')
            conn.rollback()


def delete_apadriñante(conn):
    """
        Elimina o apadriñante desexado polo usuario
    """  
    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE
   
    dni = input("Introduce o DNI do apadriñante a eliminar: ")
    if dni =="":
        dni = None
    sql= """ delete from apadriñante where DNI=%(dni)s"""
    
    with conn.cursor() as cur:                                               
        try:                               
            cur.execute(sql,{'DNI':dni})
            if cur.rowcount == 0:
                print("Non existe un apadriñante rexistrado co DNI:",dni,"")
            else:
                print("Apadriñante con DNI:",dni," eliminado")
            conn.commit()
            
        except psycopg2.Error as e:
            if e.pgcode==psycopg2.errorcodes.STRING_DATA_RIGHT_TRUNCATION:
                print("Error: fóra do límite de caracteres")
            else:
                print(f'Error generico: {e.pgcode}: {e.pgerror}')
            conn.rollback()


def delete_cuota(conn):
    """
        Elimina a cuota desexada polo usuario
    """  
    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE
   
    codcuota = input("Introduce o código da cuota a eliminar: ")
    if codcuota =="":
        codcuota = None
    sql= """ delete from cuota where codcuota=%(codcuota)s"""
    
    with conn.cursor() as cur:                                               
        try:                               
            cur.execute(sql,{'codcuota':codcuota})
            if cur.rowcount == 0:
                print("Non existe unha cuota rexistrada co código:",codcuota,"")
            else:
                print("Cuota con código:",codcuota," eliminada")
            conn.commit()
            
        except psycopg2.Error as e:
            if e.pgcode==psycopg2.errorcodes.STRING_DATA_RIGHT_TRUNCATION:
                print("Error: fóra do límite de caracteres")
            else:
                print(f'Error generico: {e.pgcode}: {e.pgerror}')
            conn.rollback()

def show_cans(conn):
    """
        Lista os cans existentes na BD
    """    
    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED

    sql= """
        select can.codchip, can.nome, can.observacions, can.DNI_apadriñante
        from can
    """
    
    with conn.cursor() as cur:                                      
        try:                     
            cur.execute(sql)
            row=cur.fetchone()
           
            if row:
                print("Lista de cans rexistrados na BD:")
                while row:
                    print(f"Can número {cur.rownumber} de {cur.rowcount}:")
                    print(f"-Código do chip: {row[0]}")
                    print(f"-Nome: {row[1]}")
                    print(f"-Observacións: {row[2]}")
                    print(f"-DNI do seu apadriñante: {row[3]}")
                    print("\n")
                    row=cur.fetchone()

            else:
                print("Non hai cans rexistrados")
            conn.commit()
            
        except psycopg2.Error as e:
            if e.pgcode==psycopg2.errorcodes:
                print('Error: ')
            else:
                print(f'Error generico: {e.pgcode}: {e.pgerror}')
            conn.rollback()


def show_apadriñantes(conn):
    """
        Lista os apadriñantes existentes na BD
    """    
    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED

    sql= """
        select apadriñante.DNI, apadriñante.nome, apadriñante.apelido1, apadriñante.apelido2, apadriñante.codcuota
        from apadriñante
    """
    
    with conn.cursor() as cur:                                      
        try:                     
            cur.execute(sql)
            row=cur.fetchone()
           
            if row:
                print("Lista de apadriñantes rexistrados na BD:")
                while row:
                    print(f"Apadriñante número {cur.rownumber} de {cur.rowcount}:")
                    print(f"-DNI: {row[0]}")
                    print(f"-Nome: {row[1]}")
                    print(f"-Primeiro apelido: {row[2]}")
                    print(f"-Segundo apelido: {row[3]}")
                    print(f"-Código da cuota que paga: {row[4]}")
                    print("\n")
                    row=cur.fetchone()

            else:
                print("Non hai apadriñantes rexistrados")
            conn.commit()
            
        except psycopg2.Error as e:
            if e.pgcode==psycopg2.errorcodes:
                print('Error: ')
            else:
                print(f'Error generico: {e.pgcode}: {e.pgerror}')
            conn.rollback()


def show_cuotas(conn):
    """
        Lista as cuotas existentes na BD
    """    
    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED

    sql= """
        select cuota.codcuota, cuota.nome, cuota.valor
        from cuota
    """
    
    with conn.cursor() as cur:                                      
        try:                     
            cur.execute(sql)
            row=cur.fetchone()
           
            if row:
                print("Lista de cuotas rexistradas na BD:")
                while row:
                    print(f"Cuota número {cur.rownumber} de {cur.rowcount}:")
                    print(f"-Código da cuota: {row[0]}")
                    print(f"-Nome: {row[1]}")
                    print(f"-Valor: {row[2]} euros")
                    print("\n")
                    row=cur.fetchone()

            else:
                print("Non hai cuotas rexistradas")
            conn.commit()
            
        except psycopg2.Error as e:
            if e.pgcode==psycopg2.errorcodes:
                print('Error: ')
            else:
                print(f'Error generico: {e.pgcode}: {e.pgerror}')
            conn.rollback()
        
def show_cuota(conn, control_tx = True):
    """
    Pide por teclado o código dunha cuota e mostra os seus detalles
    :param conn: a conexión aberta á bd
    :return: Nada
    """
    scod=input("Código da cuota: ")
    cod = None if scod=="" else int(scod)

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

def show_can(conn, control_tx = True):
    """
    Pide por teclado o código do chip dun can e mostra os seus detalles
    :param conn: a conexión aberta á bd
    :return: Nada
    """
    schip=input("Código do chip do can: ")
    chip = None if schip=="" else int(schip)

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

def update_cuota(conn):
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)
    cod = show_cuota(conn,control_tx=False)
    if cod is None:
        conn.rollback()
        return
    
    
    sincr=input("Incremento (%) da nova cuota")
    incr = None if sincr=="" else float(sincr)

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
                print("O valor debe ser positivo: non se modifica o artigo")
            elif e.pgcode == psycopg2.errorcodes.NUMERIC_VALUE_OUT_OF_RANGE:
                print("O prezo é demasiado grande ou demasiado pequeno: debe ser menor de 1000")
            elif e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                print("O nome do artigo é requerido")
            elif e.pgcode == psycopg2.errorcodes.SERIALIZATION_FAILURE:
                print("Non se pode modificar o prezo. Outro usuario xa o modificou")
            else:
                print(f"Erro: {e.pgcode} - {e.pgerror}")
            conn.rollback()

def update_can(conn):
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
                print("O pedido é requerido")
            elif e.pgcode == psycopg2.errorcodes.SERIALIZATION_FAILURE:
                print("Non se pode modificar o valor das observacións. Outro usuario xa o modificou")
            else:
                print(f"Erro: {e.pgcode} - {e.pgerror}")
            conn.rollback()

def show_can_apadriñante_cuota(conn, control_tx = True):
    """
    Pide por teclado o código do chip dun can e mostra os seus detalles
    :param conn: a conexión aberta á bd
    :return: Nada
    """
    schip=input("Código do chip do can: ")
    chip = None if schip=="" else int(schip)

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
##Imprime un menú de opcións, solicita a opción e executa a función asociada. 'q' para saír.
##-------------------------------------------------------------
def menu(conn):
    MENU_TEXT = """
      -- MENÚ DA PROTECTORA --
1 - Engadir can
2 - Engadir apadriñante
3 - Engadir cuota
4 - Eliminar can
5 - Eliminar apadriñante
6 - Eliminar cuota
7 - Listar cans
8 - Listar apadriñantes
9 - Listar cuotas
10 - Mostrar cuota
11 - Mostrar can
12 - Actualizar cuota (Incrementar valor)
13 - Actualizar observacións dun can
14 - Mostrar can, o seu apadriñante e o seu tipo de cuota.
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
            delete_apadriñante(conn)
        elif tecla == '6':
            delete_cuota(conn)
        elif tecla == '7':
            show_cans(conn)
        elif tecla == '8':
            show_apadriñantes(conn)
        elif tecla == '9':
            show_cuotas(conn)
        elif tecla == '10':
            show_cuota(conn)
        elif tecla == '11':
            show_can(conn)
        elif tecla == '12':
            update_cuota(conn)
        elif tecla == '13':
            update_can(conn)
        elif tecla == '13':
            show_can_apadriñante_cuota(conn)


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