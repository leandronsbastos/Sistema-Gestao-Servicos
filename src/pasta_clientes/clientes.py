from flask import Blueprint, render_template, redirect, url_for, request,flash,session
from bd.db import mysql

clientes= Blueprint('clientes',__name__, template_folder='templates')

@clientes.route('/login')
def login():
    return render_template('login.html')

@clientes.route('/clientes')
def inserirCliente():
    return render_template('/clientes.html')

@clientes.route('/clientes', methods=['GET','POST'])
def cadastro ():
    formulario = request.form
    codigo = formulario['codigo_cli']
    nome = formulario['nome_cli']
    
    with mysql.cursor()as Cursor:
        codigodb=Cursor.execute("SELECT codigo_cli FROM clientes WHERE codigo_cli= %s",(codigo,))
        if codigodb:
            flash('Código de Cliente já registrado')
        Cursor.execute("INSERT INTO Clientes (codigo_cli, nome_cli) VALUES(%s, %s)",(codigo, nome))
        mysql.commit()
        Cursor.close()
        
    return redirect (url_for('/adm'))