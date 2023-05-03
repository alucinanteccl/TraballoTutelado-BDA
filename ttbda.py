# Autores: Lucía Conde Fuentes (l.conde@udc.es) Julia Roade Conejo (@udc.es)
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
            print('Can con chip:',chip,', nome:', nome, ', observacións:', observacions, ' e DNI do apadriñante:', nome, ' engadida correctamente')
            
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

## ------------------------------------------------------------
##Imprime un menú de opcións, solicita a opción e executa a función asociada. 'q' para saír.
##-------------------------------------------------------------
def menu(conn):
    MENU_TEXT = """
      -- MENÚ DA PROTECTORA --
1 - Engadir can
2 - Engadir apadriñante
3 - Engadir cuota
4 - ...
5 - ...
6 - ...
7 - ...
8 - ...
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
        #elif tecla == '4':
            #delete_row(conn)
        #elif tecla == '5':
            #show_row(conn)
        #elif tecla == '6':
            #show_by_price(conn)
        #elif tecla == '7':
            #update_row(conn)
        #elif tecla == '8':
            #increase_price(conn)


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