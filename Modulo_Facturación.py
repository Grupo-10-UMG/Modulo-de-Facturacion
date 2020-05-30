#-----------------------------------------------------------------------------------------------------------
#--------------Elaborado por José Francisco Armas Sosa---------------------
#--------------Carnet 1990 00 2168 ---------------------
#--------------Universidad Mariano Galvez---------------------
#--------------Programacion 1 seccion "A"---------------------
#--------------Modulo de Facturacion---------------------
#--------------Este modulo no contempla actualizar registrso de facturas por motivos legales ---------------------
#-----------------------------------------------------------------------------------------------------------

import sqlite3
import os
import pprint

#-----------------------------------------------------------------------------------------------------------
#--------------insertar registros  ---------------------
#-----------------------------------------------------------------------------------------------------------

def pr_inserta_datos():

    print("  INGRESO DE FACTURAS  ")
    v_fecha = (input(f"INGRESA LA FECHA: "))
    miConexion=sqlite3.connect("Vehiculos")

    # para crear tabla se crea cursor
    miCursor=miConexion.cursor()

    miCursor.execute("""CREATE TABLE IF NOT EXISTS FACTURAS (
                        codigo_factura INTEGER NOT NULL,
                        cod_venta INTEGER NOT NULL,
                        fecha datetime,  
                        Total number,
                        PRIMARY KEY (codigo_factura, cod_venta),
                        FOREIGN KEY (cod_venta) REFERENCES VENTAS (cod_venta))""")
    
    ##################################################Solicita cliente#################################################
    print("***** INGRESE EL CODIGO DEL CLIENTE *****")
    miCursor.execute("SELECT * FROM CLIENTES")

    listado_clientes=miCursor.fetchall()
    #pprint.pprint(listado_clientes)
    print( "Codigo, Nombre, Apellido, Dirección, Telefono, NIT")
    for ls_clientes in listado_clientes:
        print(ls_clientes)
    #    pprint.pprint(ls_clientes)
    print("Fin del listado" + '\n')

    while True:
        try:
            v_cod_cliente = int(input("ingrese opcion: "))
            break
        except ValueError:
            print("El cliente no existe")
    
    sentencia = "SELECT * FROM CLIENTES WHERE ID_CLIENTE LIKE ?;"
    miCursor.execute(sentencia, [ "%{}%".format(v_cod_cliente) ])
    clientes=miCursor.fetchall()
    print(clientes)
    
    #################################################solicita venta######################################################



    print("\n")
    v_correlativo_factura = ''
    # inicio ciclo para guardar varias ventas en una factura
    while True:
        print("*****INGRESE LAS VENTAS PENDIENTES A FACTURAR*****")
        miCursor.execute(f"""select a.CODIGO_VENTA, a.Fecha, b.nombre, 
                            b.APELLIDO, c.cod_vehiculo, c.marca, 
                            c.modelo, c.anio, c.descripcion, a.Cantidad, 
                            c.precio_venta, 
                            a.Cantidad * c.precio_venta  
                            from ventas a, clientes b, INVENTARIO c
                            where a.COD_INV = c.cod_vehiculo
                            and a.COD_CLIENTE = b.ID_CLIENTE
                            and b.ID_CLIENTE = {v_cod_cliente}
                            and not exists (select 1 from FACTURAS F where a.codigo_venta=f.cod_venta) 
                            order by a.codigo_venta""")
        listado_ventas=miCursor.fetchall()
        #pprint.pprint(listado_inventario)
        print( "CODIGO_VENTA, FECHA, NOMBRE, APELLIDO, COD VEHICULO, MARCA, MODELO, AñO, DESCRIPCION, CANTIDAD, PRECIO VENTA, TOTAL")
        for ls_ventas in listado_ventas:
            print(ls_ventas)
        print("Fin del listado" + '\n')
        while True:
                try:
                    v_cod_venta = int(input("Ingresa el codigo de venta: "))
                    break
                except ValueError:
                    print("El ingreso no existe")
        if v_correlativo_factura == '':
            miCursor.execute("Select max(codigo_factura) + 1 from FACTURAS")
            sql_corr_fac=(miCursor.fetchall())
            v_correlativo_factura =int(sql_corr_fac[0][0])
            #print(int(sql_corr_fac[0][0]))
            if v_correlativo_factura == '':
                v_correlativo_factura=1
        
        miCursor.execute(f"""insert into FACTURAS Values('{v_correlativo_factura}',
                        '{v_cod_venta}',
                        '{v_fecha}',
                        '0')""")
        miConexion.commit()
        print("Datos guardados exitosamente! \n")

        v_pide_mas = (input("Desea ingresar mas ventas? SI/NO: "))
        if v_pide_mas == 'NO':
            break
    ############################### impresion de factura ########################################   
    #MOSTRAR PRIMERO EL CLIENTE
    print("\n")
    print("\n")
    print(f"IMPRESION DE FACTURA NUMERO {v_correlativo_factura}")
    print("\n")
    print("AUTOVENTAS LA HUESERA")
    print("DETALLE DEL CLIENTE: ")
    print("Codigo, Nombre, Apellido, Dirección, Telefono, NIT")
    print(clientes)
    print("\n")
    print("DETALLE DE COMPRA:")
    print("CODIGO_VENTA, FECHA, CODIGO VEHICULO, MARCA, MODELO, AñO, DESCRIPCION, CANTIDAD, PRECIO VENTA, TOTAL")
    miCursor.execute(f"""select a.CODIGO_VENTA, a.Fecha, c.cod_vehiculo, c.marca, 
                        c.modelo, c.anio, c.descripcion, a.Cantidad, 
                        c.precio_venta, 
                        a.Cantidad * c.precio_venta  
                        from ventas a, clientes b, INVENTARIO c
                        where a.COD_INV = c.cod_vehiculo
                        and a.COD_CLIENTE = b.ID_CLIENTE
                        and exists (select 1 from FACTURAS F where a.codigo_venta=f.cod_venta and f.codigo_factura = {v_correlativo_factura} ) 
                        order by a.codigo_venta""")
    sql_detalle=(miCursor.fetchall())        
    for ls_det in sql_detalle:
        print(ls_det)
    miConexion.commit()
    miCursor.execute(f"""SELECT SUM(a.cantidad*c.precio_venta) 
                        from ventas a,  INVENTARIO c
                        where a.COD_INV = c.cod_vehiculo
                        and exists (select 1 from FACTURAS F 
                                        where a.codigo_venta=f.cod_venta 
                                        and f.codigo_factura = {v_correlativo_factura} ) 
                        """)
    sql_total=(miCursor.fetchall())
    v_gran_total=float(sql_total[0][0])
    print("\n")
    print(f"SU TOTAL A CANCELAR ES DE: {v_gran_total:,.2f} " )
    print("GRACIAS POR SU COMPRA")
    v_continuar = input("presione ENTER para continuar... ")
    v_continuar = v_continuar+"null" # solo lo puse para que no marque feo
    miConexion.commit()
        
    miCursor.execute(f"""UPDATE""")

    miConexion.close()
    ######################################################################################################################

#-----------------------------------------------------------------------------------------------------------
#--------------lista registros  ---------------------
#-----------------------------------------------------------------------------------------------------------

def pr_listar():
    miConexion=sqlite3.connect("Vehiculos")
    miCursor=miConexion.cursor()
    print("*****INGRESE LAS VENTAS PENDIENTES A FACTURAR*****")
    miCursor.execute(f"""select f.codigo_factura, f.fecha, a.CODIGO_VENTA, a.Fecha, b.nombre, 
                        b.APELLIDO, b.nit, c.cod_vehiculo, c.marca, 
                        c.modelo, c.anio, c.descripcion, a.Cantidad, 
                        c.precio_venta, 
                        a.Cantidad * c.precio_venta  
                        from ventas a, clientes b, INVENTARIO c, FACTURAS F
                        where a.COD_INV = c.cod_vehiculo
                        and a.COD_CLIENTE = b.ID_CLIENTE
                        and a.codigo_venta=f.cod_venta 
                        order by a.codigo_venta""")
    
    listado_ventas=miCursor.fetchall()
    print( "CODIGO FACTURA, FECHA FACTURA, CODIGO_VENTA, FECHA V, NOMBRE, APELLIDO, NIT, COD VEHICULO, MARCA, MODELO, AñO, DESCRIPCION, CANTIDAD, PRECIO VENTA, TOTAL")
    for ls_ventas in listado_ventas:
        print(ls_ventas)

    print("Fin del listado" + '\n')
    miConexion.commit()
    miConexion.close()    
    v_continuar = input("presione ENTER para continuar... ")
    v_continuar = v_continuar+"null" # solo lo puse para que no marque feo


#-----------------------------------------------------------------------------------------------------------
#--------------Busca registros  ---------------------
#-----------------------------------------------------------------------------------------------------------
def pr_busqueda():
    v_op_busqueda=0
    v_criterio_busqueda = ''
    while True:
        print("  BUSQUEDA DE FACTURAS   ")
        print("Criterios de busqueda: ")
        print("1. POR NIT DEL CLIENTE")
        print("2. POR NOMBRE DEL CLIENTE")
        print("3. POR APELLIDO DEL CLIENTE")
        print("4. POR RANGO DE FECHA")
        print("5. SALIR")
        while True:
            try:
                v_op_busqueda = int(input("ingrese opcion: "))
                break
            except ValueError:
                print("Error de ingreso pruebe nuevamente")

        if v_op_busqueda == 5:
            break
 
        if v_op_busqueda == 1:
            while True:
                try:
                    v_valor_busqueda = (input("ingrese b.nit: "))
                    v_criterio_busqueda = (f"and b.nit LIKE '%{v_valor_busqueda}%' ")
                    break
                except ValueError:
                    print("Error de ingreso pruebe nuevamente")
        elif v_op_busqueda == 2:
            while True:
                try:
                    v_valor_busqueda = (input("ingrese nombre: "))
                    v_criterio_busqueda = (f"and b.nombre LIKE '%{v_valor_busqueda}%' ")
                    break
                except ValueError:
                    print("Error de ingreso pruebe nuevamente")
        elif v_op_busqueda == 3:
            while True:
                try:
                    v_valor_busqueda = (input("ingrese Apellido: "))
                    v_criterio_busqueda = (f"and b.apellido LIKE '%{v_valor_busqueda}%' ")
                    break
                except ValueError:
                    print("Error de ingreso pruebe nuevamente")
        elif v_op_busqueda == 4:
            while True:
                try:
                    v_valor_busqueda = (input("ingrese fehca inicial: "))
                    v_valor_busqueda_b = (input("ingrese fehca final: "))
                    v_criterio_busqueda = (f"and f.fecha between '{v_valor_busqueda}' and '{v_valor_busqueda_b}' ")
                    break
                except ValueError:
                    print("Error de ingreso pruebe nuevamente")

        miConexion=sqlite3.connect("Vehiculos")
        miCursor=miConexion.cursor()
        print("*****INGRESE LAS VENTAS PENDIENTES A FACTURAR*****")
        miCursor.execute(f"""select f.codigo_factura, f.fecha, a.CODIGO_VENTA, a.Fecha, b.nombre, 
                            b.APELLIDO, b.nit, c.cod_vehiculo, c.marca, 
                            c.modelo, c.anio, c.descripcion, a.Cantidad, 
                            c.precio_venta, 
                            a.Cantidad * c.precio_venta  
                            from ventas a, clientes b, INVENTARIO c, FACTURAS F
                            where a.COD_INV = c.cod_vehiculo
                            and a.COD_CLIENTE = b.ID_CLIENTE
                            and a.codigo_venta=f.cod_venta 
                            {v_criterio_busqueda}
                            order by a.codigo_venta""")
        
        listado_ventas=miCursor.fetchall()
        print( "CODIGO FACTURA, FECHA FACTURA, CODIGO_VENTA, FECHA V, NOMBRE, APELLIDO, NIT, COD VEHICULO, MARCA, MODELO, AñO, DESCRIPCION, CANTIDAD, PRECIO VENTA, TOTAL")
        for ls_ventas in listado_ventas:
            print(ls_ventas)

        print("Fin del listado" + '\n')
        miConexion.commit()
        miConexion.close()    
        v_continuar = input("presione ENTER para continuar... ")
        v_continuar = v_continuar+"null" # solo lo puse para que no marque feo
#-----------------------------------------------------------------------------------------------------------
#--------------MENU PRINCIPAL   ---------------------
#-----------------------------------------------------------------------------------------------------------

v_opcion=0
while True:
	#os.system("cls")

	print("Menu principal Modulo de Facturación:" + '\n' )
	print("1. Creacion de facturas" + '\n' )
	print("2. Reporte de facturación" + '\n' )
	print("3. Busquedas de facturas" + '\n' )
	print("4. Salir" + '\n' )
    
	while True:
		try:
			v_opcion = int(input("ingrese opcion: "))
			break
		except ValueError:
			print("Error de ingreso pruebe nuevamente")

	if v_opcion == 4:
		break
	#print("el valor es" + v_opcion)


	if v_opcion == 1:
		pr_inserta_datos()
	elif v_opcion == 2:
		pr_listar()
	elif v_opcion == 3:
		pr_busqueda()
