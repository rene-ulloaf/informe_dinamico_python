#-------------------------------------------------------------------------------
# Name:        clsInforme
# Purpose:
#
# Author:      Rene Ulloa
#
# Created:     09/11/2011
# Copyright:   (c) chechex 2011
# Licence:     GPL
#-------------------------------------------------------------------------------
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from clsUtilidades import clsUtil

class clsInforme:
    __f=""
    __con = ""
    __host = ""
    __user = ""
    __pass = ""
    __bd = ""

    def __init__(self,dir_cfg):
        self.__U = clsUtil()
        self.__DatosCFG(dir_cfg)

        self.__con = self.__U.coneccion(self.__host, self.__user, self.__pass, self.__bd)
        self.__CreaInteraz()

    def __CreaInteraz(self):
        self.__r = Tk()
        self.__r.withdraw() #ocultamos la ventana

        self.__r.title("Informes")
        self.__r.geometry("=800x600+%d+%d" % (self.__r.winfo_screenwidth()/2-400,self.__r.winfo_screenheight()/2-300)) #Tamano y posicion
        self.__r.maxsize(1024,768)
        self.__r.minsize(800,600)
        self.__r.resizable(FALSE, FALSE) # Booleanos

        self.__menu()

        self.__r.wm_deiconify() #mostramos la ventana en su sitio
        self.__r.mainloop()

    def __menu(self):
        menubar = Menu(self.__r)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Recargas", command=self.__InformeRecarga)
        filemenu.add_command(label="Ventas por Persona", command=self.__InformeVentaPer)
        filemenu.add_command(label="Ventas por Compania", command=self.__InformeVentaCia)
        filemenu.add_command(label="Salir", command=self.__r.quit,)
        menubar.add_cascade(label="Informes", menu=filemenu)
        self.__r.config(menu=menubar)

    def __frame(self):
        self.__esconder()

        self.__f = Frame(self.__r, height=600, width=800)
        self.__f.pack_propagate(0)
        self.__f.pack()

    def __esconder(self):
        if self.__f <> "":
            self.__f.destroy()

    def __InformeRecarga(self):
        self.__frame()

        Label(self.__f, text="Recargas", borderwidth=6).grid(row=0, columnspan=6, sticky=W+E)
        Label(self.__f, text="").grid(row=1, column=0, rowspan=6, columnspan=2)

        Label(self.__f, text="Telefono: ").grid(row=3, column=2, sticky=E+W)
        self.__txtTel = Entry(self.__f)
        self.__txtTel.grid(row=3, column=3, sticky=E+W)
        Label(self.__f, text="Compania: ").grid(row=4, column=2, sticky=E+W)
        self.__txtCia = Entry(self.__f)
        self.__txtCia.grid(row=4, column=3, sticky=E+W)
        Label(self.__f, text="").grid(row=5, column=6, rowspan=2, columnspan=2)

        Button(self.__f, text="Buscar", width=6, command=self.__BusRecargas).grid(row=5, column=2)
        Button(self.__f, text="Limpiar", width=6, command=self.__limpiarRecargas).grid(row=5, column=3)
        Label(self.__f, text="").grid(row=6, column=0, rowspan=2, columnspan=6, sticky=E+W+N+S)

    def __BusRecargas(self):
        tel = self.__txtTel.get()
        cia = self.__txtCia.get()

        Label(self.__f, text="Compania").grid(row=8, column=0)
        Label(self.__f, text="Cod. Compania").grid(row=8, column=1)
        Label(self.__f, text="Telefono").grid(row=8, column=2)
        Label(self.__f, text="Monto").grid(row=8, column=3)
        Label(self.__f, text="Fecha Recarga").grid(row=8, column=4)
        Label(self.__f, text="Fecha Ingreso").grid(row=8, column=5)

        con_cur = self.__con.cursor()
        sql_query = "SELECT c.nombre, r.cod_cia, t.numero, r.monto, r.fecha_recarga, r.fecha_ingreso"
        sql_query += " FROM recargas r"
        sql_query += " JOIN cia c ON r.id_cia = c.id_cia"
        sql_query += " JOIN telefono t ON r.id_telefono = t.id_telefono"
        sql_query += " WHERE t.numero = CASE WHEN '" + tel + "' = '' Then t.numero ELSE '" + tel + "' END"
        sql_query += " AND c.nombre = CASE WHEN '" + cia + "' = '' Then c.nombre ELSE '" + cia + "' END"
        sql_query += " ORDER BY r.fecha_ingreso;"

        if con_cur.execute(sql_query) > 0:
            resultados = con_cur.fetchall()

            fil = 9
            for registro in resultados:
                Label(self.__f, text=registro[0]).grid(row=fil, column=0, sticky=W)
                Label(self.__f, text=registro[1]).grid(row=fil, column=1, sticky=W)
                Label(self.__f, text=registro[2]).grid(row=fil, column=2, sticky=W)
                Label(self.__f, text=registro[3]).grid(row=fil, column=3, sticky=W)
                Label(self.__f, text=registro[4]).grid(row=fil, column=4, sticky=W)
                Label(self.__f, text=registro[5]).grid(row=fil, column=5, sticky=W)

                fil += fil
        else:
            Label(self.__f, text="No existen registros").grid(row=9, column=0, sticky=E+W)

    def __limpiarRecargas(self):
        self.__txtTel.delete(0, END)
        self.__txtCia.delete(0, END)

    def __InformeVentaPer(self):
        self.__frame()

        Label(self.__f, text="Recargas por Telefono", borderwidth=6).grid(row=0, columnspan=6, sticky=W+E)
        Label(self.__f, text="").grid(row=1, column=0, rowspan=6, columnspan=2)

        Label(self.__f, text="Telefono: ").grid(row=3, column=2, sticky=E+W)
        self.__txtTelPer = Entry(self.__f)
        self.__txtTelPer.grid(row=3, column=3, sticky=E+W)
        Label(self.__f, text="Compania: ").grid(row=4, column=2, sticky=E+W)
        self.__txtCiaPer = Entry(self.__f)
        self.__txtCiaPer.grid(row=4, column=3, sticky=E+W)
        Label(self.__f, text="").grid(row=5, column=6, rowspan=2, columnspan=2)

        Button(self.__f, text="Buscar", width=6, command=self.__BusRecargasPer).grid(row=5, column=2)
        Button(self.__f, text="Limpiar", width=6, command=self.__limpiarRecargasPer).grid(row=5, column=3)
        Label(self.__f, text="").grid(row=6, column=0, rowspan=2, columnspan=6, sticky=E+W+N+S)

    def __BusRecargasPer(self):
        tel = self.__txtTelPer.get()
        cia = self.__txtCiaPer.get()

        Label(self.__f, text="Compania").grid(row=8, column=0)
        Label(self.__f, text="Cod. Compania").grid(row=8, column=1)
        Label(self.__f, text="Telefono").grid(row=8, column=2)
        Label(self.__f, text="Cantidad").grid(row=8, column=3)
        Label(self.__f, text="Monto").grid(row=8, column=4)
        Label(self.__f, text="Fecha Recarga").grid(row=8, column=5)
        Label(self.__f, text="Fecha Ingreso").grid(row=8, column=6)

        con_cur = self.__con.cursor()
        sql_query = "SELECT c.nombre, r.cod_cia, t.numero, COUNT(t.numero), SUM(r.monto), r.fecha_recarga, r.fecha_ingreso"
        sql_query += " FROM recargas r"
        sql_query += " JOIN cia c ON r.id_cia = c.id_cia"
        sql_query += " JOIN telefono t ON r.id_telefono = t.id_telefono"
        sql_query += " WHERE t.numero = CASE WHEN '" + tel + "' = '' Then t.numero ELSE '" + tel + "' END"
        sql_query += " AND c.nombre = CASE WHEN '" + cia + "' = '' Then c.nombre ELSE '" + cia + "' END"
        sql_query += " GROUP BY r.id_telefono "
        sql_query += " ORDER BY r.fecha_ingreso;"

        if con_cur.execute(sql_query) > 0:
            resultados = con_cur.fetchall()

            fil = 9
            for registro in resultados:
                Label(self.__f, text=registro[0]).grid(row=fil, column=0, sticky=W)
                Label(self.__f, text=registro[1]).grid(row=fil, column=1, sticky=W)
                Label(self.__f, text=registro[2]).grid(row=fil, column=2, sticky=W)
                Label(self.__f, text=registro[3]).grid(row=fil, column=3, sticky=W)
                Label(self.__f, text=registro[4]).grid(row=fil, column=4, sticky=W)
                Label(self.__f, text=registro[5]).grid(row=fil, column=5, sticky=W)
                Label(self.__f, text=registro[6]).grid(row=fil, column=6, sticky=W)

                fil += fil
        else:
            Label(self.__f, text="No existen registros").grid(row=9, column=0, sticky=E+W)

    def __limpiarRecargasPer(self):
        self.__txtTelPer.delete(0, END)
        self.__txtCiaPer.delete(0, END)

    def __InformeVentaCia(self):
        self.__frame()

        Label(self.__f, text="Recargas por Compania", borderwidth=6).grid(row=0, columnspan=3, sticky=W+E)
        Label(self.__f, text="").grid(row=1, column=0, rowspan=3, columnspan=2)

        Label(self.__f, text="Compania: ").grid(row=3, column=1, sticky=E+W)
        self.__txtCiaCia = Entry(self.__f)
        self.__txtCiaCia.grid(row=3, column=2, sticky=E+W)
        Label(self.__f, text="").grid(row=4, column=3, rowspan=2, columnspan=2)

        Button(self.__f, text="Buscar", width=6, command=self.__BusRecargasCia).grid(row=6, column=1)
        Button(self.__f, text="Limpiar", width=6, command=self.__limpiarRecargasCia).grid(row=6, column=2)
        Label(self.__f, text="").grid(row=7, column=0, rowspan=2, columnspan=6, sticky=E+W+N+S)

    def __BusRecargasCia(self):
        cia = self.__txtCiaCia.get()

        Label(self.__f, text="Compania").grid(row=8, column=0)
        Label(self.__f, text="Cantidad").grid(row=8, column=1)
        Label(self.__f, text="Monto").grid(row=8, column=2)

        con_cur = self.__con.cursor()
        sql_query = "SELECT c.nombre, COUNT(r.id_telefono), SUM(r.monto)"
        sql_query += " FROM recargas r"
        sql_query += " JOIN cia c ON r.id_cia = c.id_cia"
        sql_query += " WHERE c.nombre = CASE WHEN '" + cia + "' = '' Then c.nombre ELSE '" + cia + "' END"
        sql_query += " GROUP BY r.id_cia "
        sql_query += " ORDER BY r.fecha_ingreso;"

        if con_cur.execute(sql_query) > 0:
            resultados = con_cur.fetchall()

            fil = 9
            for registro in resultados:
                Label(self.__f, text=registro[0]).grid(row=fil, column=0, sticky=W)
                Label(self.__f, text=registro[1]).grid(row=fil, column=1, sticky=W)
                Label(self.__f, text=registro[2]).grid(row=fil, column=2, sticky=W)

                fil += fil
        else:
            Label(self.__f, text="No existen registros").grid(row=9, column=0, sticky=E+W)

    def __limpiarRecargasCia(self):
        self.__txtCiaCia.delete(0, END)

    def __DatosCFG(self,dir_cfg):
        datos=[]
        datos = self.__U.leerCFG(dir_cfg)

        for dat in datos:
            d = dat.split("|")

            if d[0] == "host":
                self.__host = d[1]

            if d[0] == "user":
                self.__user = d[1]

            if d[0] == "pass":
                self.__pass = d[1]


            if d[0] == "bd":
                self.__bd = d[1]