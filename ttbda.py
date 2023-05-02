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
def add_dog(conn):
    """
        Crea e engade una nova Conta á BD cos datos introducidos polo
        usuario
    """
    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED

    chip = input("Introduce o número do chip do can:")
    if chip=="":
        chip=None

    nome = input ("Introduce o nome do novo can:")
    observacions = input ("Introduce algunhas observacións necesarias:")

    sql= """
        insert into can (codchip,nome,observacions) 
        VALUES  (%(chip)s,%(nome)s,%(observacions)s)
    """
    
    with conn.cursor() as cur:                                      
        try:                     
            cur.execute(sql,{'chip':chip,'nome':nome,'observacions':observacions})
            conn.commit()
            print('Can con chip:',chip,', nome:', nome, ' e observacións:', observacions, ' engadida correctamente')
            
        except psycopg2.Error as e:
            if e.pgcode==psycopg2.errorcodes.NOT_NULL_VIOLATION:
                print("Error: non pode haber campos sen valor")
            elif e.pgcode==psycopg2.errorcodes.UNIQUE_VIOLATION:
                print("Error: xa existe unha conta co campo DNI [",dni,"]")
            elif e.pgcode==psycopg2.errorcodes.NUMERIC_VALUE_OUT_OF_RANGE:
                print("Error: o valor do saldo da nova introducido non é válido")
            elif e.pgcode==psycopg2.errorcodes.STRING_DATA_RIGHT_TRUNCATION:
                print("Error: o DNI introducido está fora do límite de caracteres")
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
      -- MENÚ --
1 - ...
2 - ...
3 - ...
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
            create_tables(conn)
        elif tecla == '2':
            add_dog(conn)
        #elif tecla == '3':
            ##insert_row(conn)
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