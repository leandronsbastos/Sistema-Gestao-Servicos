from re import M
from zlib import DEF_BUF_SIZE
from flask import Blueprint,render_template,request,redirect,session, flash,url_for
from bd.db import mysql
admin = Blueprint('admin', __name__, template_folder='templates')
import datetime


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def P(ANO, MES, DIA, PERIODO):
    M31 = [1, 3, 5, 7, 8, 10, 12]

    day = int(DIA) + PERIODO
    month = int(MES)
    year = int(ANO)
    DATA_FINAL = None
    print(day, month, year)

    if year % 4 == 0:
        if month == 2:
            if day + PERIODO > 28:
                day = day - 28
                month = month + 1
    elif year % 4 != 0:
        if month == '02':
            if day + PERIODO > 29:
                day = day - 29
                month = month + 1
    else:
        if day + PERIODO >31 and month in M31:
            day = day - 31
            month = month + 1
        elif day + PERIODO > 30 and month not in M31:
            day = day - 30
            month = month + 1

    if day < 10:
        if month < 10:
            DATA_FINAL = f'{year}-0{month}-0{day}'
        else:
            DATA_FINAL = f'{year}-{month}-0{day}'
    else:
        if month < 10:
            DATA_FINAL = f'{year}-0{month}-{day}'
        else:
            DATA_FINAL = f'{year}-{month}-{day}'
    return DATA_FINAL

@admin.route('/perfil_adm',methods=['POST'])
def perfil():
    pk_user = session['id_admin']
    Details = request.form
    nome_troca = Details['nome']
    email_troca = Details ['troca_email']
    troca_senha = Details ['troca_senha']
    session['nome_admin'] = nome_troca
    session['email_admin'] = email_troca

    with mysql.cursor()as Cursor:
        Cursor.execute("UPDATE user SET nome_user = %s, email_user=%s, pass_user = %s WHERE id_user = %s ",(nome_troca,email_troca,troca_senha,pk_user,))
        mysql.commit()
            
    return redirect(url_for('admin.adm'))


@admin.route('/adm')
def adm():
    if not 'loggedin' in session:
        return redirect ('/login')
    c = 'user'
    pk_user = session['id_admin']
    nome = session['nome_admin']
    email = session['email_admin']
    with mysql.cursor()as Cursor:
        Cursor.execute("SELECT pass_user FROM user WHERE id_user =%s",(pk_user,))
        senha = Cursor.fetchone()
        Values = Cursor.execute("SELECT * FROM user")
        if Values > 0:
            Details = Cursor.fetchall()
            return render_template('/Controle-adm.html',Details=Details,Values=Values,c=c,senha = senha , email=email, nome = nome)
        else:
            return render_template('/Controle-adm.html', Values=Values,c=c,senha = senha , email=email, nome = nome)
    # return render_template('adm.html')


@admin.route('/adm/menu',methods=['GET','POST'])
def home():
    if not 'loggedin' in session:
        return redirect ('/login')
    pk_user = session['id_admin']
    nome = session['nome_admin']
    email = session['email_admin']
    with mysql.cursor()as Cursor:
        Cursor.execute("SELECT pass_user FROM user WHERE id_user =%s",(pk_user,))
        senha = Cursor.fetchone()
        pk_user = session["id_admin"]
        Cursor.execute("SELECT id_user FROM solicitacao WHERE id_user = %s", (pk_user,))
        conta = Cursor.fetchone()
        cont_Cadastro=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Cadastro' and id_user= %s",(pk_user,))
        cont_Clientes=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Clientes' and id_user= %s",(pk_user,))
        cont_Produtos=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Produtos' and id_user= %s",(pk_user,))
        cont_Financeiro=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Financeiro' and id_user= %s",(pk_user,))
        cont_Compras=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Compras' and id_user= %s",(pk_user,))
        cont_Vendas=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Vendas' and id_user= %s",(pk_user,))
        cont_Documentos=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Documentos Fiscais' and id_user=%s",(pk_user,))
        cont_SPED=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='SPED' and id_user= %s",(pk_user,))
        cont_Parametros=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Parâmetros' and id_user= %s",(pk_user,))
        cont_Relatorios=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Relatórios' and id_user= %s",(pk_user,))
        cont_Banco=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Banco de Dados' and id_user= %s",(pk_user,))
        cont_Liberacao=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Liberação de Licenças' and id_user= %s",(pk_user,))
        cont_Outros=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Outros' and id_user= %s",(pk_user,))
        leitoraberto= Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and id_user =%s",(pk_user,))
        leitorfechado= Cursor.execute ("SELECT * FROM solicitacao WHERE status_sol='Fechada' and id_user =%s",(pk_user,))
        
        Values = Cursor.execute("SELECT * FROM solicitacao WHERE id_user= %s  order by id_sol DESC",(pk_user))
        if Values > 0:
            Details = Cursor.fetchall()
            return render_template('/home-adm.html',Details=Details,Values=Values,cont_Cadastro=cont_Cadastro,cont_Clientes=cont_Clientes,cont_Produtos=cont_Produtos,cont_Financeiro=cont_Financeiro,cont_Compras=cont_Compras,cont_Vendas=cont_Vendas,cont_Documentos=cont_Documentos,cont_SPED=cont_SPED,cont_Parametros=cont_Parametros,cont_Relatorios=cont_Relatorios,cont_Banco=cont_Banco,cont_Liberacao=cont_Liberacao,cont_Outros=cont_Outros,leitoraberto=leitoraberto,leitorfechado=leitorfechado,conta=conta,senha=senha,email=email, nome=nome)
        else:
            return render_template('/home-adm.html', Values=Values,cont_Cadastro=cont_Cadastro,cont_Clientes=cont_Clientes,cont_Produtos=cont_Produtos,cont_Financeiro=cont_Financeiro,cont_Compras=cont_Compras,cont_Vendas=cont_Vendas,cont_Documentos=cont_Documentos,cont_SPED=cont_SPED,cont_Parametros=cont_Parametros,cont_Relatorios=cont_Relatorios,cont_Banco=cont_Banco,cont_Liberacao=cont_Liberacao,cont_Outros=cont_Outros,pk_user=pk_user,senha=senha,email=email,nome =nome)

@admin.route("/adm/requisicoes",methods=["GET"])
def requisicoes():
    if not 'loggedin' in session:
        return redirect ('/login')
    pk_user = session['id_admin']
    nome = session['nome_admin']
    email = session['email_admin']
    with mysql.cursor()as Cursor:
        Cursor.execute("SELECT pass_user FROM user WHERE id_user =%s",(pk_user,))
        senha = Cursor.fetchone()
        cont_Cadastro=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Cadastro'")
        cont_Clientes=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Clientes'")
        cont_Produtos=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Produtos'")
        cont_Financeiro=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Financeiro'")
        cont_Compras=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Compras'")
        cont_Vendas=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Vendas'")
        cont_Documentos=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Documentos Fiscais'")
        cont_SPED=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='SPED'")
        cont_Parametros=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Parâmetros'")
        cont_Relatorios=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Relatórios'")
        cont_Banco=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Banco de Dados'")
        cont_Liberacao=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Liberação de Licenças'")
        cont_Outros=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Outros'")
        leitoraberto= Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta'")
        leitorfechado= Cursor.execute ("SELECT * FROM solicitacao WHERE status_sol='Fechada'")
        leitorandamento= Cursor.execute ("SELECT * FROM solicitacao WHERE status_sol='Andamento'")
        Values=Cursor.execute("SELECT * FROM solicitacao order by id_sol DESC")
        if Values > 0:
            Details = Cursor.fetchall()
            
            return render_template('/requisicoes.html', Details=Details,Values=Values,cont_Cadastro=cont_Cadastro,cont_Clientes=cont_Clientes,cont_Produtos=cont_Produtos,cont_Financeiro=cont_Financeiro,cont_Compras=cont_Compras,cont_Vendas=cont_Vendas,cont_Documentos=cont_Documentos,cont_SPED=cont_SPED,cont_Parametros=cont_Parametros,cont_Relatorios=cont_Relatorios,cont_Banco=cont_Banco,cont_Liberacao=cont_Liberacao,cont_Outros=cont_Outros,leitoraberto = leitoraberto ,leitorfechado = leitorfechado ,leitorandamento=leitorandamento,senha = senha , email=email, nome = nome)
        return render_template('/requisicoes.html',Values=Values,cont_Cadastro=cont_Cadastro,cont_Clientes=cont_Clientes,cont_Produtos=cont_Produtos,cont_Financeiro=cont_Financeiro,cont_Compras=cont_Compras,cont_Vendas=cont_Vendas,cont_Documentos=cont_Documentos,cont_SPED=cont_SPED,cont_Parametros=cont_Parametros,cont_Relatorios=cont_Relatorios,cont_Banco=cont_Banco,cont_Liberacao=cont_Liberacao,cont_Outros=cont_Outros,senha = senha , email=email, nome = nome)

@admin.route("/adm/estatisticas",methods=['GET'])
def estatisticas():
    if not 'loggedin' in session:
        return redirect ('/login')
    pk_user = session['id_admin']
    nome = session['nome_admin']
    email = session['email_admin']
    with mysql.cursor()as Cursor:
        Cursor.execute("SELECT pass_user FROM user WHERE id_user =%s",(pk_user,))
        senha = Cursor.fetchone()
        # pegando infos do html    
        dias_select = request.args.get('days')
        dataaa = request.args.get('dataaa')
        # Conta
        DATA_ATUAL = dataaa
             # checking days
        if dataaa == '' or dataaa is None:
            DATA_ATUAL = str(datetime.date.today())
            ANO = DATA_ATUAL[:4]
            MES = DATA_ATUAL[5:7]
            DIA = int(DATA_ATUAL[8:])
            if dias_select == '1':
                DATA_FINAL = P(ANO, MES, DIA, 1)
                tipo_Cadastro=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Cadastro' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Clientes=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Clientes' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Produtos=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Produtos' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Financeiro=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Financeiro' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Compras=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Compras' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Vendas=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Vendas' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Documentos=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Documentos Fiscais' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_SPED=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='SPED' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Parametros=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Parâmetros' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Relatorios=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Relatórios' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Banco=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Banco de Dados' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Liberacao=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Liberação de Licenças' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Outros=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Outros' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_user=Cursor.execute("SELECT * FROM user WHERE type_user='user'")
                num_exec=Cursor.execute("SELECT * FROM user WHERE type_user='exec'")
                totaluser = Cursor.execute("SELECT id_user from user WHERE type_user = 'user' ")
                totalexec = Cursor.execute("SELECT id_user from user WHERE type_user = 'exec' ")
                num_analise=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_andamento=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_fechada=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                seila2 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Aberta'")
                seila3 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Fechada'")
                oi=Cursor.execute("Select * from solicitacao")
                if oi>0: 
                    somatotal = num_exec + num_user
                    porcentoUser = str((num_user/somatotal)*100)
                    porcentoExec = str((num_exec/somatotal)*100)
                    aporcentoUser = porcentoUser[:2]
                    aporcentoExec = porcentoExec[:2]

                    seila = seila2 + seila3
                    porcentoUsera = str((seila2/seila)*100)
                    porcentoExeca = str((seila3/seila)*100)
                    aporcentoUsers = porcentoUsera[:]
                    aporcentoExecs = porcentoExeca[:]
                else:
                    aporcentoUser=0
                    aporcentoExec=0
                    aporcentoExecs=0
                    aporcentoUsers=0
                avaliacao_pessima=Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='1' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_ruim = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='2' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_mediana =Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='3' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_bom = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='4' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_otimo = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='5' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta'")
                aaaaaaaa= Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento'")
                num_andamentoo = Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada'")
                num_fechadaa = Cursor.fetchall()

                aberta=[]
                fecha=[]

                Cursor.execute("SELECT data_inicio FROM solicitacao where not data_inicio is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_inicio = Cursor.fetchall()
                Cursor.execute("SELECT data_final FROM solicitacao where not data_final is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_final = Cursor.fetchall()

                lista=[]
                listaa=[]
                listaaa=[]

                for x in data_inicio:
                    if x not in lista :
                        lista.append(x)
                        Cursor.execute("SELECT count(data_inicio) FROM solicitacao where data_inicio= %s and status_sol='Aberta'",(x,))
                        sei=Cursor.fetchone()
                        listaa.append(sei)
                        Cursor.execute("SELECT count(data_final) FROM solicitacao where data_final= %s and status_sol='Fechada'",(x,))
                        seia=Cursor.fetchone()
                        listaaa.append(seia)
                print(lista)
            elif dias_select == '7':
                DATA_FINAL = P(ANO, MES, DIA, 7)
                tipo_Cadastro=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Cadastro' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Clientes=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Clientes' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Produtos=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Produtos' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Financeiro=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Financeiro' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Compras=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Compras' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Vendas=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Vendas' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Documentos=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Documentos Fiscais' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_SPED=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='SPED' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Parametros=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Parâmetros' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Relatorios=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Relatórios' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Banco=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Banco de Dados' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Liberacao=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Liberação de Licenças' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Outros=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Outros' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_user=Cursor.execute("SELECT * FROM user WHERE type_user='user'")
                num_exec=Cursor.execute("SELECT * FROM user WHERE type_user='exec'")
                totaluser = Cursor.execute("SELECT id_user from user WHERE type_user = 'user' ")
                totalexec = Cursor.execute("SELECT id_user from user WHERE type_user = 'exec' ")
                num_analise=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_andamento=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_fechada=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                seila2 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Aberta'")
                seila3 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Fechada'")
                oi=Cursor.execute("Select * from solicitacao")
                if oi>0: 
                    somatotal = num_exec + num_user
                    porcentoUser = str((num_user/somatotal)*100)
                    porcentoExec = str((num_exec/somatotal)*100)
                    aporcentoUser = porcentoUser[:2]
                    aporcentoExec = porcentoExec[:2]

                    seila = seila2 + seila3
                    porcentoUsera = str((seila2/seila)*100)
                    porcentoExeca = str((seila3/seila)*100)
                    aporcentoUsers = porcentoUsera[:]
                    aporcentoExecs = porcentoExeca[:]
                else:
                    aporcentoUser=0
                    aporcentoExec=0
                    aporcentoExecs=0
                    aporcentoUsers=0
                avaliacao_pessima=Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='1' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_ruim = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='2' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_mediana =Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='3' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_bom = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='4' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_otimo = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='5' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta'")
                aaaaaaaa= Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento'")
                num_andamentoo = Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada'")
                num_fechadaa = Cursor.fetchall()

                aberta=[]
                fecha=[]

                Cursor.execute("SELECT data_inicio FROM solicitacao where not data_inicio is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_inicio = Cursor.fetchall()
                Cursor.execute("SELECT data_final FROM solicitacao where not data_final is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_final = Cursor.fetchall()

                lista=[]
                listaa=[]
                listaaa=[]

                for x in data_inicio:
                    if x not in lista :
                        lista.append(x)
                        Cursor.execute("SELECT count(data_inicio) FROM solicitacao where data_inicio= %s and status_sol='Aberta'",(x,))
                        sei=Cursor.fetchone()
                        listaa.append(sei)
                        Cursor.execute("SELECT count(data_final) FROM solicitacao where data_final= %s and status_sol='Fechada'",(x,))
                        seia=Cursor.fetchone()
                        listaaa.append(seia)
                print(lista)
            elif dias_select == '15':
                DATA_FINAL = P(ANO, MES, DIA, 15)
                tipo_Cadastro=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Cadastro' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Clientes=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Clientes' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Produtos=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Produtos' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Financeiro=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Financeiro' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Compras=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Compras' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Vendas=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Vendas' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Documentos=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Documentos Fiscais' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_SPED=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='SPED' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Parametros=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Parâmetros' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Relatorios=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Relatórios' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Banco=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Banco de Dados' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Liberacao=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Liberação de Licenças' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Outros=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Outros' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_user=Cursor.execute("SELECT * FROM user WHERE type_user='user'")
                num_exec=Cursor.execute("SELECT * FROM user WHERE type_user='exec'")
                totaluser = Cursor.execute("SELECT id_user from user WHERE type_user = 'user' ")
                totalexec = Cursor.execute("SELECT id_user from user WHERE type_user = 'exec' ")
                num_analise=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_andamento=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_fechada=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                seila2 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Aberta'")
                seila3 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Fechada'")
                oi=Cursor.execute("Select * from solicitacao")
                if oi>0: 
                    somatotal = num_exec + num_user
                    porcentoUser = str((num_user/somatotal)*100)
                    porcentoExec = str((num_exec/somatotal)*100)
                    aporcentoUser = porcentoUser[:2]
                    aporcentoExec = porcentoExec[:2]

                    seila = seila2 + seila3
                    porcentoUsera = str((seila2/seila)*100)
                    porcentoExeca = str((seila3/seila)*100)
                    aporcentoUsers = porcentoUsera[:]
                    aporcentoExecs = porcentoExeca[:]
                else:
                    aporcentoUser=0
                    aporcentoExec=0
                    aporcentoExecs=0
                    aporcentoUsers=0
                avaliacao_pessima=Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='1' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_ruim = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='2' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_mediana =Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='3' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_bom = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='4' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_otimo = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='5' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta'")
                aaaaaaaa= Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento'")
                num_andamentoo = Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada'")
                num_fechadaa = Cursor.fetchall()

                aberta=[]
                fecha=[]

                Cursor.execute("SELECT data_inicio FROM solicitacao where not data_inicio is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_inicio = Cursor.fetchall()
                Cursor.execute("SELECT data_final FROM solicitacao where not data_final is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_final = Cursor.fetchall()

                lista=[]
                listaa=[]
                listaaa=[]

                for x in data_inicio:
                    if x not in lista :
                        lista.append(x)
                        Cursor.execute("SELECT count(data_inicio) FROM solicitacao where data_inicio= %s and status_sol='Aberta'",(x,))
                        sei=Cursor.fetchone()
                        listaa.append(sei)
                        Cursor.execute("SELECT count(data_final) FROM solicitacao where data_final= %s and status_sol='Fechada'",(x,))
                        seia=Cursor.fetchone()
                        listaaa.append(seia)
                print(lista)
            elif dias_select == '30':
                DATA_FINAL = P(ANO, MES, DIA, 30)
                tipo_Cadastro=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Cadastro' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Clientes=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Clientes' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Produtos=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Produtos' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Financeiro=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Financeiro' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Compras=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Compras' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Vendas=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Vendas' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Documentos=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Documentos Fiscais' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_SPED=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='SPED' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Parametros=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Parâmetros' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Relatorios=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Relatórios' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Banco=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Banco de Dados' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Liberacao=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Liberação de Licenças' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Outros=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Outros' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_user=Cursor.execute("SELECT * FROM user WHERE type_user='user'")
                num_exec=Cursor.execute("SELECT * FROM user WHERE type_user='exec'")
                totaluser = Cursor.execute("SELECT id_user from user WHERE type_user = 'user' ")
                totalexec = Cursor.execute("SELECT id_user from user WHERE type_user = 'exec' ")
                num_analise=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_andamento=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_fechada=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                seila2 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Aberta'")
                seila3 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Fechada'")
                oi=Cursor.execute("Select * from solicitacao")
                if oi>0: 
                    somatotal = num_exec + num_user
                    porcentoUser = str((num_user/somatotal)*100)
                    porcentoExec = str((num_exec/somatotal)*100)
                    aporcentoUser = porcentoUser[:2]
                    aporcentoExec = porcentoExec[:2]

                    seila = seila2 + seila3
                    porcentoUsera = str((seila2/seila)*100)
                    porcentoExeca = str((seila3/seila)*100)
                    aporcentoUsers = porcentoUsera[:]
                    aporcentoExecs = porcentoExeca[:]
                else:
                    aporcentoUser=0
                    aporcentoExec=0
                    aporcentoExecs=0
                    aporcentoUsers=0
                avaliacao_pessima=Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='1' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_ruim = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='2' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_mediana =Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='3' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_bom = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='4' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_otimo = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='5' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta'")
                aaaaaaaa= Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento'")
                num_andamentoo = Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada'")
                num_fechadaa = Cursor.fetchall()

                aberta=[]
                fecha=[]

                Cursor.execute("SELECT data_inicio FROM solicitacao where not data_inicio is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_inicio = Cursor.fetchall()
                Cursor.execute("SELECT data_final FROM solicitacao where not data_final is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_final = Cursor.fetchall()

                lista=[]
                listaa=[]
                listaaa=[]

                for x in data_inicio:
                    if x not in lista :
                        lista.append(x)
                        Cursor.execute("SELECT count(data_inicio) FROM solicitacao where data_inicio= %s and status_sol='Aberta'",(x,))
                        sei=Cursor.fetchone()
                        listaa.append(sei)
                        Cursor.execute("SELECT count(data_final) FROM solicitacao where data_final= %s and status_sol='Fechada'",(x,))
                        seia=Cursor.fetchone()
                        listaaa.append(seia)
                print(lista)
            else:
                tipo_Cadastro=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Cadastro'")
                tipo_Clientes=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Clientes'")
                tipo_Produtos=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Produtos'")
                tipo_Financeiro=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Financeiro'")
                tipo_Compras=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Compras'")
                tipo_Vendas=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Vendas'")
                tipo_Documentos=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Documentos Fiscais'")
                tipo_SPED=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='SPED'")
                tipo_Parametros=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Parâmetros'")
                tipo_Relatorios=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Relatórios'")
                tipo_Banco=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Banco de Dados'")
                tipo_Liberacao=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Liberação de Licenças'")
                tipo_Outros=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Outros'")
                num_user=Cursor.execute("SELECT * FROM user WHERE type_user='user'")
                num_exec=Cursor.execute("SELECT * FROM user WHERE type_user='exec'")
                num_analise=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta'")
                num_andamento=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento'")
                num_fechada=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada'")
                seila2 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Aberta'")
                seila3 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Fechada'")
                oi=Cursor.execute("Select * from solicitacao")
                if oi>0: 
                    somatotal = num_exec + num_user
                    porcentoUser = str((num_user/somatotal)*100)
                    porcentoExec = str((num_exec/somatotal)*100)
                    aporcentoUser = porcentoUser[:2]
                    aporcentoExec = porcentoExec[:2]

                    seila = seila2 + seila3
                    porcentoUsera = str((seila2/seila)*100)
                    porcentoExeca = str((seila3/seila)*100)
                    aporcentoUsers = porcentoUsera[:]
                    aporcentoExecs = porcentoExeca[:]
                else:
                    aporcentoUser=0
                    aporcentoExec=0
                    aporcentoExecs=0
                    aporcentoUsers=0
                avaliacao_pessima=Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='1'")
                avaliacao_ruim = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='2'")
                avaliacao_mediana =Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='3'")
                avaliacao_bom = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='4'")
                avaliacao_otimo = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='5'")
                Cursor.execute("SELECT data_inicio FROM solicitacao where not data_inicio is null")
                data_inicio = Cursor.fetchall()
                Cursor.execute("SELECT data_final FROM solicitacao where not data_final is null")
                data_final = Cursor.fetchall()
                lista=[]
                listaa=[]
                listaaa=[]
                for x in data_inicio:
                    if x not in lista :
                        lista.append(x)
                        Cursor.execute("SELECT count(data_inicio) FROM solicitacao where data_inicio= %s and status_sol='Aberta'",(x,))
                        sei=Cursor.fetchone()
                        listaa.append(sei)
                        Cursor.execute("SELECT count(data_final) FROM solicitacao where data_final= %s and status_sol='Fechada'",(x,))
                        seia=Cursor.fetchone()
                        listaaa.append(seia)
                print(lista)
        else:
            ANO = DATA_ATUAL[:4]
            MES = DATA_ATUAL[5:7]
            DIA = int(DATA_ATUAL[8:])
            if dias_select == '1':
                DATA_FINAL = P(ANO, MES, DIA, 1)
                tipo_Cadastro=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Cadastro' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Clientes=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Clientes' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Produtos=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Produtos' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Financeiro=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Financeiro' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Compras=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Compras' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Vendas=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Vendas' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Documentos=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Documentos Fiscais' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_SPED=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='SPED' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Parametros=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Parâmetros' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Relatorios=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Relatórios' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Banco=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Banco de Dados' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Liberacao=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Liberação de Licenças' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Outros=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Outros' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_user=Cursor.execute("SELECT * FROM user WHERE type_user='user'")
                num_exec=Cursor.execute("SELECT * FROM user WHERE type_user='exec'")
                totaluser = Cursor.execute("SELECT id_user from user WHERE type_user = 'user' ")
                totalexec = Cursor.execute("SELECT id_user from user WHERE type_user = 'exec' ")
                num_analise=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_andamento=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_fechada=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                seila2 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Aberta'")
                seila3 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Fechada'")
                oi=Cursor.execute("Select * from solicitacao")
                if oi>0: 
                    somatotal = num_exec + num_user
                    porcentoUser = str((num_user/somatotal)*100)
                    porcentoExec = str((num_exec/somatotal)*100)
                    aporcentoUser = porcentoUser[:2]
                    aporcentoExec = porcentoExec[:2]

                    seila = seila2 + seila3
                    porcentoUsera = str((seila2/seila)*100)
                    porcentoExeca = str((seila3/seila)*100)
                    aporcentoUsers = porcentoUsera[:]
                    aporcentoExecs = porcentoExeca[:]
                else:
                    aporcentoUser=0
                    aporcentoExec=0
                    aporcentoExecs=0
                    aporcentoUsers=0
                avaliacao_pessima=Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='1' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_ruim = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='2' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_mediana =Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='3' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_bom = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='4' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_otimo = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='5' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta'")
                aaaaaaaa= Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento'")
                num_andamentoo = Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada'")
                num_fechadaa = Cursor.fetchall()

                aberta=[]
                fecha=[]

                Cursor.execute("SELECT data_inicio FROM solicitacao where not data_inicio is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_inicio = Cursor.fetchall()
                Cursor.execute("SELECT data_final FROM solicitacao where not data_final is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_final = Cursor.fetchall()

                lista=[]
                listaa=[]
                listaaa=[]

                for x in data_inicio:
                    if x not in lista :
                        lista.append(x)
                        Cursor.execute("SELECT count(data_inicio) FROM solicitacao where data_inicio= %s and status_sol='Aberta'",(x,))
                        sei=Cursor.fetchone()
                        listaa.append(sei)
                        Cursor.execute("SELECT count(data_final) FROM solicitacao where data_final= %s and status_sol='Fechada'",(x,))
                        seia=Cursor.fetchone()
                        listaaa.append(seia)
                print(lista)
            elif dias_select == '7':
                DATA_FINAL = P(ANO, MES, DIA, 7)
                tipo_Cadastro=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Cadastro' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Clientes=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Clientes' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Produtos=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Produtos' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Financeiro=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Financeiro' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Compras=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Compras' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Vendas=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Vendas' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Documentos=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Documentos Fiscais' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_SPED=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='SPED' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Parametros=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Parâmetros' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Relatorios=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Relatórios' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Banco=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Banco de Dados' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Liberacao=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Liberação de Licenças' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Outros=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Outros' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_user=Cursor.execute("SELECT * FROM user WHERE type_user='user'")
                num_exec=Cursor.execute("SELECT * FROM user WHERE type_user='exec'")
                totaluser = Cursor.execute("SELECT id_user from user WHERE type_user = 'user' ")
                totalexec = Cursor.execute("SELECT id_user from user WHERE type_user = 'exec' ")
                num_analise=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_andamento=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_fechada=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                seila2 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Aberta'")
                seila3 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Fechada'")
                oi=Cursor.execute("Select * from solicitacao")
                if oi>0: 
                    somatotal = num_exec + num_user
                    porcentoUser = str((num_user/somatotal)*100)
                    porcentoExec = str((num_exec/somatotal)*100)
                    aporcentoUser = porcentoUser[:2]
                    aporcentoExec = porcentoExec[:2]

                    seila = seila2 + seila3
                    porcentoUsera = str((seila2/seila)*100)
                    porcentoExeca = str((seila3/seila)*100)
                    aporcentoUsers = porcentoUsera[:]
                    aporcentoExecs = porcentoExeca[:]
                else:
                    aporcentoUser=0
                    aporcentoExec=0
                    aporcentoExecs=0
                    aporcentoUsers=0
                avaliacao_pessima=Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='1' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_ruim = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='2' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_mediana =Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='3' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_bom = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='4' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_otimo = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='5' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta'")
                aaaaaaaa= Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento'")
                num_andamentoo = Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada'")
                num_fechadaa = Cursor.fetchall()

                aberta=[]
                fecha=[]

                Cursor.execute("SELECT data_inicio FROM solicitacao where not data_inicio is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_inicio = Cursor.fetchall()
                Cursor.execute("SELECT data_final FROM solicitacao where not data_final is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_final = Cursor.fetchall()

                lista=[]
                listaa=[]
                listaaa=[]

                for x in data_inicio:
                    if x not in lista :
                        lista.append(x)
                        Cursor.execute("SELECT count(data_inicio) FROM solicitacao where data_inicio= %s and status_sol='Aberta'",(x,))
                        sei=Cursor.fetchone()
                        listaa.append(sei)
                        Cursor.execute("SELECT count(data_final) FROM solicitacao where data_final= %s and status_sol='Fechada'",(x,))
                        seia=Cursor.fetchone()
                        listaaa.append(seia)
                print(lista)
            elif dias_select == '15':
                DATA_FINAL = P(ANO, MES, DIA, 15)
                tipo_Cadastro=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Cadastro' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Clientes=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Clientes' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Produtos=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Produtos' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Financeiro=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Financeiro' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Compras=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Compras' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Vendas=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Vendas' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Documentos=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Documentos Fiscais' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_SPED=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='SPED' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Parametros=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Parâmetros' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Relatorios=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Relatórios' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Banco=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Banco de Dados' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Liberacao=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Liberação de Licenças' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Outros=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Outros' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_user=Cursor.execute("SELECT * FROM user WHERE type_user='user'")
                num_exec=Cursor.execute("SELECT * FROM user WHERE type_user='exec'")
                totaluser = Cursor.execute("SELECT id_user from user WHERE type_user = 'user' ")
                totalexec = Cursor.execute("SELECT id_user from user WHERE type_user = 'exec' ")
                num_analise=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_andamento=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_fechada=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                seila2 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Aberta'")
                seila3 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Fechada'")
                oi=Cursor.execute("Select * from solicitacao")
                if oi>0: 
                    somatotal = num_exec + num_user
                    porcentoUser = str((num_user/somatotal)*100)
                    porcentoExec = str((num_exec/somatotal)*100)
                    aporcentoUser = porcentoUser[:2]
                    aporcentoExec = porcentoExec[:2]

                    seila = seila2 + seila3
                    porcentoUsera = str((seila2/seila)*100)
                    porcentoExeca = str((seila3/seila)*100)
                    aporcentoUsers = porcentoUsera[:]
                    aporcentoExecs = porcentoExeca[:]
                else:
                    aporcentoUser=0
                    aporcentoExec=0
                    aporcentoExecs=0
                    aporcentoUsers=0
                avaliacao_pessima=Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='1' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_ruim = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='2' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_mediana =Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='3' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_bom = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='4' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_otimo = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='5' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta'")
                aaaaaaaa= Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento'")
                num_andamentoo = Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada'")
                num_fechadaa = Cursor.fetchall()

                aberta=[]
                fecha=[]

                Cursor.execute("SELECT data_inicio FROM solicitacao where not data_inicio is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_inicio = Cursor.fetchall()
                Cursor.execute("SELECT data_final FROM solicitacao where not data_final is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_final = Cursor.fetchall()

                lista=[]
                listaa=[]
                listaaa=[]

                for x in data_inicio:
                    if x not in lista :
                        lista.append(x)
                        Cursor.execute("SELECT count(data_inicio) FROM solicitacao where data_inicio= %s and status_sol='Aberta'",(x,))
                        sei=Cursor.fetchone()
                        listaa.append(sei)
                        Cursor.execute("SELECT count(data_final) FROM solicitacao where data_final= %s and status_sol='Fechada'",(x,))
                        seia=Cursor.fetchone()
                        listaaa.append(seia)
                print(lista)
            elif dias_select == '30':
                DATA_FINAL = P(ANO, MES, DIA, 30)
                print(DATA_FINAL)
                tipo_Cadastro=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Cadastro' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Clientes=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Clientes' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Produtos=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Produtos' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Financeiro=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Financeiro' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Compras=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Compras' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Vendas=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Vendas' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Documentos=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Documentos Fiscais' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_SPED=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='SPED' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Parametros=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Parâmetros' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Relatorios=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Relatórios' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Banco=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Banco de Dados' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Liberacao=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Liberação de Licenças' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                tipo_Outros=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Outros' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_user=Cursor.execute("SELECT * FROM user WHERE type_user='user'")
                num_exec=Cursor.execute("SELECT * FROM user WHERE type_user='exec'")
                totaluser = Cursor.execute("SELECT id_user from user WHERE type_user = 'user' ")
                totalexec = Cursor.execute("SELECT id_user from user WHERE type_user = 'exec' ")
                num_analise=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_andamento=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                num_fechada=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                seila2 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Aberta'")
                seila3 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Fechada'")
                oi=Cursor.execute("Select * from solicitacao")
                if oi>0: 
                    somatotal = num_exec + num_user
                    porcentoUser = str((num_user/somatotal)*100)
                    porcentoExec = str((num_exec/somatotal)*100)
                    aporcentoUser = porcentoUser[:2]
                    aporcentoExec = porcentoExec[:2]

                    seila = seila2 + seila3
                    porcentoUsera = str((seila2/seila)*100)
                    porcentoExeca = str((seila3/seila)*100)
                    aporcentoUsers = porcentoUsera[:]
                    aporcentoExecs = porcentoExeca[:]
                else:
                    aporcentoUser=0
                    aporcentoExec=0
                    aporcentoExecs=0
                    aporcentoUsers=0
                avaliacao_pessima=Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='1' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_ruim = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='2' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_mediana =Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='3' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_bom = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='4' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                avaliacao_otimo = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='5' and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta'")
                aaaaaaaa= Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento'")
                num_andamentoo = Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada'")
                num_fechadaa = Cursor.fetchall()

                aberta=[]
                fecha=[]

                Cursor.execute("SELECT data_inicio FROM solicitacao where not data_inicio is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_inicio = Cursor.fetchall()
                Cursor.execute("SELECT data_final FROM solicitacao where not data_final is null and data_inicio between %s and %s", (DATA_ATUAL, DATA_FINAL,))
                data_final = Cursor.fetchall()

                lista=[]
                listaa=[]
                listaaa=[]

                for x in data_inicio:
                    if x not in lista :
                        lista.append(x)
                        Cursor.execute("SELECT count(data_inicio) FROM solicitacao where data_inicio= %s and status_sol='Aberta'",(x,))
                        sei=Cursor.fetchone()
                        listaa.append(sei)
                        Cursor.execute("SELECT count(data_final) FROM solicitacao where data_final= %s and status_sol='Fechada'",(x,))
                        seia=Cursor.fetchone()
                        listaaa.append(seia)
                print(lista)
                print(type(DATA_ATUAL), DATA_ATUAL, DATA_FINAL)
            else:
                tipo_Cadastro=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Cadastro'")
                tipo_Clientes=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Clientes'")
                tipo_Produtos=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Produtos'")
                tipo_Financeiro=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Financeiro'")
                tipo_Compras=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Compras'")
                tipo_Vendas=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Vendas'")
                tipo_Documentos=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Documentos Fiscais'")
                tipo_SPED=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='SPED'")
                tipo_Parametros=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Parâmetros'")
                tipo_Relatorios=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Relatórios'")
                tipo_Banco=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Banco de Dados'")
                tipo_Liberacao=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Liberação de Licenças'")
                tipo_Outros=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Outros'")
                num_user=Cursor.execute("SELECT * FROM user WHERE type_user='user'")
                num_exec=Cursor.execute("SELECT * FROM user WHERE type_user='exec'")
                num_analise=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta'")
                num_andamento=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento'")
                num_fechada=Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada'")
                seila2 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Aberta'")
                seila3 = Cursor.execute("SELECT id_sol from solicitacao where status_sol = 'Fechada'")
                oi=Cursor.execute("Select * from solicitacao")
                if oi>0: 
                    somatotal = num_exec + num_user
                    porcentoUser = str((num_user/somatotal)*100)
                    porcentoExec = str((num_exec/somatotal)*100)
                    aporcentoUser = porcentoUser[:2]
                    aporcentoExec = porcentoExec[:2]

                    seila = seila2 + seila3
                    porcentoUsera = str((seila2/seila)*100)
                    porcentoExeca = str((seila3/seila)*100)
                    aporcentoUsers = porcentoUsera[:]
                    aporcentoExecs = porcentoExeca[:]
                else:
                    aporcentoUser=0
                    aporcentoExec=0
                    aporcentoExecs=0
                    aporcentoUsers=0
                avaliacao_pessima=Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='1'")
                avaliacao_ruim = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='2'")
                avaliacao_mediana =Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='3'")
                avaliacao_bom = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='4'")
                avaliacao_otimo = Cursor.execute("SELECT * FROM solicitacao WHERE avaliacao='5'")
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta'")
                aaaaaaaa= Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Andamento'")
                num_andamentoo = Cursor.fetchall()
                Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Fechada'")
                num_fechadaa = Cursor.fetchall()
                aberta=[]
                fecha=[]
                Cursor.execute("SELECT data_inicio FROM solicitacao where not data_inicio is null")
                data_inicio = Cursor.fetchall()
                Cursor.execute("SELECT data_final FROM solicitacao where not data_final is null")
                data_final = Cursor.fetchall()
                lista=[]
                listaa=[]
                listaaa=[]
                for x in data_inicio:
                    if x not in lista :
                        lista.append(x)
                        Cursor.execute("SELECT count(data_inicio) FROM solicitacao where data_inicio= %s and status_sol='Aberta'",(x,))
                        sei=Cursor.fetchone()
                        listaa.append(sei)
                        Cursor.execute("SELECT count(data_final) FROM solicitacao where data_final= %s and status_sol='Fechada'",(x,))
                        seia=Cursor.fetchone()
                        listaaa.append(seia)
                print(lista)
        
        with mysql.cursor()as Cursor:
            oi=Cursor.execute("Select * from solicitacao where not avaliacao is null")
            if oi>0: 
                Cursor.execute("SELECT avg(avaliacao) from solicitacao where not avaliacao is null")
                final=Cursor.fetchone()
                final=round(final[0],1)
            else:
                final=0
        return render_template("char.html",tipo_Cadastro=tipo_Cadastro,tipo_Clientes=tipo_Clientes,tipo_Produtos=tipo_Produtos,tipo_Financeiro=tipo_Financeiro,tipo_Compras=tipo_Compras,tipo_Vendas=tipo_Vendas,tipo_Documentos=tipo_Documentos,tipo_SPED=tipo_SPED,tipo_Parametros=tipo_Parametros,tipo_Relatorios=tipo_Relatorios,tipo_Banco=tipo_Banco,tipo_Liberacao=tipo_Liberacao,tipo_Outros=tipo_Outros,num_exec=aporcentoExec,num_analise=num_analise,num_andamento=num_andamento,num_fechada=num_fechada,avaliacao_otimo=avaliacao_otimo,avaliacao_bom=avaliacao_bom,num_user=aporcentoUser,avaliacao_ruim=avaliacao_ruim,avaliacao_pessima=avaliacao_pessima,avaliacao_mediana=avaliacao_mediana,senha = senha , email=email, nome = nome, dataaa=dataaa,aporcentoUsers=aporcentoUsers,aporcentoExecs=aporcentoExecs,data_final=data_final,data_inicio=data_inicio,lista=lista,listaa=listaa,listaaa=listaaa)


@admin.route("/historico-avaliacao<id>")
def avaliacao(id):
    if not 'loggedin' in session:
        return redirect ('/login')
    pk_user = session['id_admin']
    nome = session['nome_admin']
    email = session['email_admin']
    with mysql.cursor()as Cursor:
        Cursor.execute("SELECT pass_user FROM user WHERE id_user =%s",(pk_user,))
        senha = Cursor.fetchone()
        leitorfechado= Cursor.execute ("SELECT * FROM solicitacao WHERE status_sol='Fechada' and id_fechador =%s and avaliacao!=0 ",(id,))
        cont_Cadastro_adm=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Cadastro'and and id_fechador =%s and avaliacao != 0 ",(id,))
        cont_Clientes_adm=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Clientes'and and id_fechador =%s and avaliacao != 0 ",(id,))
        cont_Produtos_adm=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Produtos'and and id_fechador =%s and avaliacao != 0 ",(id,))
        cont_Financeiro_adm=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Financeiro'and and id_fechador =%s and avaliacao != 0 ",(id,))
        cont_Compras_adm=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Compras'and and id_fechador =%s and avaliacao != 0 ",(id,))
        cont_Vendas_adm=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Vendas'and and id_fechador =%s and avaliacao != 0 ",(id,))
        cont_Documentos_adm=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Documentos Fiscais'and and id_fechador =%s and avaliacao != 0 ",(id,))
        cont_SPED_adm=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='SPED'and and id_fechador =%s and avaliacao != 0 ",(id,))
        cont_Parametros_adm=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Parâmetros'and and id_fechador =%s and avaliacao != 0 ",(id,))
        cont_Relatorios_adm=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Relatórios'and and id_fechador =%s and avaliacao != 0 ",(id,))
        cont_Banco_adm=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Banco de Dados'and and id_fechador =%s and avaliacao != 0 ",(id,))
        cont_Liberacao_adm=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Liberação de Licenças'and and id_fechador =%s and avaliacao != 0 ",(id,))
        cont_Outros_adm=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Outros'and and id_fechador =%s and avaliacao != 0 ",(id,))
        
        Cursor.execute("SELECT id_user FROM user WHERE id_user= %s ",(id))
        vai = Cursor.fetchone()
        Cursor.execute("SELECT nome_user FROM user WHERE id_user= %s ",(id))
        nomeuser = Cursor.fetchone()
        oi=Cursor.execute("Select * from solicitacao where id_fechador =%s and not avaliacao is null",(id,))
        if oi>0:
            Cursor.execute("SELECT avg(avaliacao) from solicitacao where id_fechador =%s",(id,))
            media=Cursor.fetchone()
            media=round(media[0],1)
        else:
            media=0
        Cursor.execute("SELECT * FROM solicitacao WHERE id_fechador = %s",(id,))
        Details = Cursor.fetchall()
        Values=Cursor.execute("SELECT * FROM solicitacao WHERE id_fechador = %s",(id,))
        if Values > 0:
            Details = Cursor.fetchall()
    return render_template("/Historico-avaliacao.html",Values=Values,Details=Details,cont_Cadastro_adm=cont_Cadastro_adm,cont_Clientes_adm=cont_Clientes_adm,cont_Produtos_adm=cont_Produtos_adm,cont_Financeiro_adm=cont_Financeiro_adm,cont_Compras_adm=cont_Compras_adm,cont_Vendas_adm=cont_Vendas_adm,cont_Documentos_adm=cont_Documentos_adm,cont_SPED_adm=cont_SPED_adm,cont_Parametros_adm=cont_Parametros_adm,cont_Relatorios_adm=cont_Relatorios_adm,cont_Banco_adm=cont_Banco_adm,cont_Liberacao_adm=cont_Liberacao_adm,cont_Outros_adm=cont_Outros_adm,leitorfechado=leitorfechado,vai=vai,nome=nome,email=email,senha=senha,nomeuser=nomeuser,media=media)


@admin.route("/cargo<id>")
def cargo(id):
    if not 'loggedin' in session:
        return redirect ('/login')
    with mysql.cursor()as Cursor:
        Cursor.execute("SELECT type_user FROM user WHERE id_user =%s",(id,))
        eounaoe = Cursor.fetchone()
        if eounaoe[0] == "user":
            Cursor.execute("UPDATE user set type_user = 'exec' WHERE id_user = %s",(id,))
            mysql.commit()
            
        else:
            Cursor.execute("UPDATE user set type_user = 'user' WHERE id_user = %s",(id,))
            mysql.commit()
            Cursor.execute("SELECT id_sol FROM solicitacao WHERE id_fechador =%s and status_sol = 'Andamento'",(id,))
            solicitacaoAndamento = Cursor.fetchall()
            Cursor.execute("SELECT id_user FROM user WHERE type_user = 'exec'") 
            allExec = Cursor.fetchall()
            x = 0
            for z in range(len(solicitacaoAndamento)):
                Cursor.execute("UPDATE solicitacao SET status_sol ='Aberta' WHERE id_sol = %s",(solicitacaoAndamento[z]))
                mysql.commit()
            Cursor.execute("SELECT id_sol FROM solicitacao WHERE id_fechador =%s and status_sol = 'Aberta'",(id,))
            solicitacaoExe = Cursor.fetchall()
            for i in range (len(solicitacaoExe)):

                if len(allExec) == 0:
                    Cursor.execute("UPDATE solicitacao set id_fechador = NULL WHERE id_sol = %s",(solicitacaoExe[i][0],))
                    mysql.commit()
                elif len (allExec) == 1:
                    Cursor.execute("UPDATE solicitacao set id_fechador = %s WHERE id_sol = %s",(allExec[0][0],solicitacaoExe[i][0],))
                    mysql.commit()
                else:
                    if allExec.index(allExec[x]) == 0:
                        a = allExec[0]
                        x += 1
                    elif allExec.index(allExec[x]) + 1 < len(allExec):
                        a = allExec[x+1]
                        x += 1
                    elif allExec.index(allExec[x]) + 1 == len(allExec):
                        a = allExec[-1]
                        x = 0
            
                    Cursor.execute("UPDATE solicitacao set id_fechador = %s WHERE id_sol = %s",(a,solicitacaoExe[i][0]))
                    mysql.commit()

            
    return redirect(url_for("admin.adm"))

    
@admin.route("/view<id>")
def vizu(id):
    if not 'loggedin' in session:
        return redirect ('/login')
    pk_user = session['id_admin']
    nome = session['nome_admin']
    email = session['email_admin']
    with mysql.cursor()as Cursor:
        Cursor.execute("SELECT pass_user FROM user WHERE id_user =%s",(pk_user,))
        senha = Cursor.fetchone()
        leitoraberto= Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and id_user =%s",(id,))
        leitorfechado= Cursor.execute ("SELECT * FROM solicitacao WHERE status_sol='Fechada' and id_user =%s",(id,))
        leitorandamento= Cursor.execute ("SELECT * FROM solicitacao WHERE status_sol='Andamento' and id_user =%s",(id,))
        cont_Cadastro_adm=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Cadastro'and and id_user =%s",(id,))
        cont_Clientes_adm=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Clientes'and and id_user =%s",(id,))
        cont_Produtos_adm=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Produtos'and and id_user =%s",(id,))
        cont_Financeiro_adm=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Financeiro'and and id_user =%s",(id,))
        cont_Compras_adm=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Compras'and and id_user =%s",(id,))
        cont_Vendas_adm=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Vendas'and and id_user =%s",(id,))
        cont_Documentos_adm=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Documentos Fiscais'and and id_user =%s",(id,))
        cont_SPED_adm=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='SPED'and and id_user =%s",(id,))
        cont_Parametros_adm=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Parâmetros'and and id_user =%s",(id,))
        cont_Relatorios_adm=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Relatórios'and and id_user =%s",(id,))
        cont_Banco_adm=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Banco de Dados'and and id_user =%s",(id,))
        cont_Liberacao_adm=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Liberação de Licenças'and and id_user =%s",(id,))
        cont_Outros_adm=Cursor.execute("SELECT type_problem FROM solicitacao WHERE type_problem='Outros'and and id_user =%s",(id,))
        
        Cursor.execute("SELECT id_user FROM user WHERE id_user= %s ",(id))
        vai = Cursor.fetchone()


        Cursor.execute("SELECT nome_user FROM user WHERE id_user= %s ",(id))
        nomeuser = Cursor.fetchone()

        Cursor.execute("SELECT * FROM solicitacao WHERE id_user= %s",(id,))
        Details = Cursor.fetchall()

        Values=Cursor.execute("SELECT * FROM solicitacao WHERE id_user= %s",(id,))
        if Values > 0:
            Details = Cursor.fetchall()
            
    return render_template("/view_solicit_user.html",Values=Values,nome=nome,Details=Details,leitoraberto=leitoraberto,leitorfechado=leitorfechado,leitorandamento=leitorandamento,vai=vai,cont_Cadastro_adm=cont_Cadastro_adm,cont_Clientes_adm=cont_Clientes_adm,cont_Produtos_adm=cont_Produtos_adm,cont_Financeiro_adm=cont_Financeiro_adm,cont_Compras_adm=cont_Compras_adm,cont_Vendas_adm=cont_Vendas_adm,cont_Documentos_adm=cont_Documentos_adm,cont_SPED_adm=cont_SPED_adm,cont_Parametros_adm=cont_Parametros_adm,cont_Relatorios_adm=cont_Relatorios_adm,cont_Banco_adm=cont_Banco_adm,cont_Liberacao_adm=cont_Liberacao_adm,cont_Outros_adm=cont_Outros_adm,email=email,senha=senha, nomeuser=nomeuser)

@admin.route('/aceitando_adm/<id>', methods=['POST'])
def aceitar(id):
    pk_user = session['id_admin']
    if not 'loggedin' in session:
        return redirect ('/login')
    with mysql.cursor()as Cursor:
        Cursor.execute("UPDATE solicitacao SET status_sol ='Andamento',id_fechador=%s WHERE id_sol = %s",(pk_user,id,))
        mysql.commit()
        
    return redirect ('/adm/requisicoes')

@admin.route('/recusando_adm/<id>', methods=['POST'])
def recusando(id):
    pk_user = session['id_admin']
    if not 'loggedin' in session:
        return redirect ('/login')
    formulario= request.form
    comentario= formulario['codigo']
    hora= datetime.datetime.now()

    if comentario != None:
        with mysql.cursor()as Cursor:
            Cursor.execute("UPDATE solicitacao SET status_sol ='Fechada',data_final=%s,comentario=%s,id_fechador=%s WHERE id_sol = %s",(hora,comentario,pk_user,id,))
            mysql.commit()
            
    return redirect ('/adm/requisicoes')

@admin.route('/andamento_adm/<id>', methods=['POST'])
def fechamento(id):
    pk_user = session['id_admin']
    if not 'loggedin' in session:
        return redirect ('/login')
    formulario= request.form
    comentario = formulario['comentario']
    hora= datetime.datetime.now()
    if comentario != None:
        with mysql.cursor()as Cursor:
            Cursor.execute("UPDATE solicitacao SET status_sol ='Fechada',data_final=%s,comentario=%s,id_fechador=%s WHERE id_sol = %s",(hora,comentario,pk_user,id,))
            mysql.commit()
            
    return redirect ('/adm/requisicoes')


@admin.route('/adm/<id>', methods=['POST'])
def delete(id):
    if not 'loggedin' in session:
        return redirect ('/login')
    with mysql.cursor()as Cursor:
        Cursor.execute("DELETE FROM solicitacao WHERE id_sol=%s",(id,))
        mysql.commit()
        Cursor.close()
    return redirect('/adm/menu')

@admin.route("/adm/clientes", methods=["GET", "POST"])
def inserirClientes():
    if request.method == "POST":
        codigo = request.form.get("codigo_cli")
        nome = request.form.get("nome_cli")
        
        if codigo and nome:
            cur = mysql.cursor()
            codigodb=cur.execute("SELECT codigo_cli FROM clientes WHERE codigo_cli= %s",(codigo,))
            if codigodb:
               flash('Código de Cliente já registrado')
            # Conectar ao banco de dados e inserir o cliente
            cur.execute("INSERT INTO clientes(codigo_cli, nome_cli) VALUES(%s, %s)", (codigo, nome))
            mysql.commit()  # Confirma a transação
            cur.close()  # Fecha o cursor
            
            # Redireciona para a página principal após inserir
            return redirect(url_for('/adm/clientes'))
    
    # Consultar clientes cadastrados no banco de dados
    cur = mysql.cursor()
    cur.execute("SELECT codigo_cli, nome_cli FROM clientes")
    clientes = cur.fetchall()  # Retorna todos os clientes
    cur.close()

    return render_template("/clientes.html", clientes=clientes)

"""@admin.route('/adm/clientes')
def inserirCliente():
    return render_template('/clientes.html')

@admin.route('/adm/clientes', methods=['GET','POST'])
def cadastro():
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
    return redirect ('/adm')"""