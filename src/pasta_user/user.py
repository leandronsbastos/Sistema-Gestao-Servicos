from flask import Blueprint,render_template,request,redirect,session,url_for
from bd.db import mysql

user_blueprint= Blueprint('user', __name__ , template_folder='templates')
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
@user_blueprint.route('/perfil',methods=['POST'])
def perfil():
    pk_user = session['id_user']
    Details = request.form
    nome_troca = Details['nome']
    email_troca = Details ['troca_email']
    troca_senha = Details ['troca_senha']
    session['nome_user'] = nome_troca
    session['email_user'] = email_troca

    with mysql.cursor()as Cursor:
        Cursor.execute("UPDATE user SET nome_user = %s, email_user=%s, pass_user = %s WHERE id_user = %s ",(nome_troca,email_troca,troca_senha,pk_user,))
        mysql.commit()
        Cursor.close()    
    return redirect(url_for('user.home'))

@user_blueprint.route('/usuario/menu',methods=['GET','POST'])
def home():
    if not 'loggedin' in session:
        return redirect ('/login')
    pk_user = session['id_user']
    nome = session['nome_user']
    email = session['email_user']
    with mysql.cursor()as Cursor:
        Cursor.execute("SELECT pass_user FROM user WHERE id_user =%s",(pk_user,))
        senha = Cursor.fetchone()
        Cursor.execute("SELECT id_user FROM user WHERE id_user = %s", (pk_user,))
        conta = Cursor.fetchone()
        cont_Cadastro=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Cadastro' and id_user= %s",(pk_user,))
        cont_Clientes=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Clientes' and id_user= %s",(pk_user,))
        cont_Produtos=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Produtos' and id_user= %s",(pk_user,))
        cont_Financeiro=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Financeiro' and id_user= %s",(pk_user,))
        cont_Compras=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Compras' and id_user= %s",(pk_user,))
        cont_Vendas=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Vendas' and id_user= %s",(pk_user,))
        cont_Documentos=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Documentos Fiscais' and id_user= %s",(pk_user,))
        cont_SPED=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='SPED' and id_user= %s",(pk_user,))
        cont_Parametros=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Parâmetros' and id_user= %s",(pk_user,))
        cont_Relatorios=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Relatórios' and id_user= %s",(pk_user,))
        cont_Banco=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Banco de Dados' and id_user= %s",(pk_user,))
        cont_Liberacao=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Liberação de Licenças' and id_user= %s",(pk_user,))
        cont_Outros=Cursor.execute("SELECT * FROM solicitacao WHERE type_problem='Outros' and id_user= %s",(pk_user,))
        leitoraberto= Cursor.execute("SELECT * FROM solicitacao WHERE status_sol='Aberta' and id_user =%s",(pk_user,))
        leitorfechado= Cursor.execute ("SELECT * FROM solicitacao WHERE status_sol='Fechada' and id_user =%s",(pk_user,))
        Values = Cursor.execute("SELECT * FROM solicitacao WHERE id_user= %s order by id_sol DESC",(pk_user,))
        if Values > 0:
            Details = Cursor.fetchall()
            return render_template('/home-user.html', Details=Details,Values=Values,cont_Cadastro=cont_Cadastro,cont_Clientes=cont_Clientes,cont_Produtos=cont_Produtos,cont_Financeiro=cont_Financeiro,cont_Compras=cont_Compras,cont_Vendas=cont_Vendas,cont_Documentos=cont_Documentos,cont_SPED=cont_SPED,cont_Parametros=cont_Parametros,cont_Relatorios=cont_Relatorios,cont_Banco=cont_Banco,cont_Liberacao=cont_Liberacao,cont_Outros=cont_Outros,leitoraberto=leitoraberto,leitorfechado=leitorfechado,conta=conta,nome=nome,email=email,pk_user=pk_user,senha=senha)
        else:
            return render_template('/home-user.html', Values=Values,cont_Cadastro=cont_Cadastro,cont_Clientes=cont_Clientes,cont_Produtos=cont_Produtos,cont_Financeiro=cont_Financeiro,cont_Compras=cont_Compras,cont_Vendas=cont_Vendas,cont_Documentos=cont_Documentos,cont_SPED=cont_SPED,cont_Parametros=cont_Parametros,cont_Relatorios=cont_Relatorios,cont_Banco=cont_Banco,cont_Liberacao=cont_Liberacao,cont_Outros=cont_Outros,pk_user=pk_user,conta=conta,nome=nome,email=email,senha=senha)

@user_blueprint.route('/avaliar/<id>', methods=['POST'])
def avaliacao(id):
    if not 'loggedin' in session:
        return redirect ('/login')
    pessimo = request.form.get('pes')
    ruim = request.form.get('ruim')
    mediano = request.form.get('med')
    otimo = request.form.get('otimo')
    bom = request.form.get('bom')
    
    comentario_avaliacao= request.form['avaliacao']
    x = [pessimo,ruim,mediano,bom,otimo]
    for i in x:
        if str(i) in "12345":
            with mysql.cursor()as Cursor:
                Cursor.execute("UPDATE solicitacao SET avaliacao =%s WHERE id_sol = %s ",(i,id,))
                mysql.commit()
                Cursor.close()
    with mysql.cursor()as Cursor:
        Cursor.execute("UPDATE solicitacao SET coment_avaliacao=%s WHERE id_sol = %s",(comentario_avaliacao,id,))
        mysql.commit()
        Cursor.close()
    with mysql.cursor()as Cursor:
        Cursor.execute("SELECT id_user from solicitacao WHERE id_sol=%s",(id,))
        a= Cursor.fetchone()
        Cursor.execute("SELECT type_user from user WHERE id_user= %s",(a,))
        teste = Cursor.fetchone()
        Cursor.close()
        if teste[0] == 'user':
            return redirect ('/usuario/menu')
        elif teste[0] == 'exec':
            return redirect ('/executor/menu')
        else:
            return redirect ('/adm/menu')

            
        
@user_blueprint.route('/usuario/<id>', methods=['POST'])
def delete(id):
    if not 'loggedin' in session:
        return redirect ('/login')
    with mysql.cursor()as Cursor:
        Cursor.execute("DELETE FROM solicitacao WHERE id_sol=%s",(id,))
        mysql.commit()
        Cursor.close()
    return redirect('/usuario/menu')




