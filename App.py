from flask import Flask, flash, render_template, request,redirect,url_for
import bcrypt
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'T3ntramitr0z0n'
app.config['MYSQL_DB'] = 'crudbd'
app.config['MYSQL_PORT'] = 3307

mysql = MySQL(app)

app.secret_key='mysecretkey'

@app.route('/')
def sesion():
    return render_template('sesion.html')

#inicio de sesuib
@app.route('/login', methods=['POST'])
def login():
    email = request.form['usuario']
    contraseña = request.form['contraseña']

    # Consulta a la base de datos
    cursor = mysql.connection.cursor()
    sql = "SELECT * FROM sesiones WHERE usuario = %s"
    cursor.execute(sql, (email,))
    user = cursor.fetchone()  # Obtiene el primer resultado
    #print(user)
   
    if user:
        hashed_password=user[2]
        #print(email)
        #print(contraseña)
        #print(f'{hashed_password}')
        if  bcrypt.checkpw(contraseña.encode('utf-8'), hashed_password.encode('utf-8')):
            flash('Inicio de sesion correctamente')
            return  redirect(url_for('Index'))
        else:
            flash('Credenciales incorrectas, intente nuevamente')
            return  redirect(url_for('sesion')) 
    else:
        flash('Credenciales incorrectas, intente nuevamente')
        return  redirect(url_for('sesion'))



   # Verificar si el usuario existe y la contraseña es correcta
    ''' if user and user[2] == contraseña.strip():
        print(user)  # Asegúrate de que el índice sea el correcto
        flash('Inicio de sesión exitoso', 'success')
        return redirect(url_for('Index'))  # Asegúrate de tener esta ruta
    else:
        flash('Credenciales inválidas, intenta nuevamente.', 'danger')
        return redirect(url_for('crear'))'''
    #termina query de inicio de sesion

#creamos cuenta desde aqui
#creamos aqui la ruta para ir a pagina creaCuenta
@app.route('/crear_cuenta')
def crear():
    return render_template('crearcuenta.html')#seria la direccion del html

#aqui es donde creamos  la cuenta de sql
@app.route('/creandocuenta', methods=['POST'])
def creardocuenta():
    email = request.form['usuario']
    contraseña = request.form['contraseña']
    confirmar_contraseña = request.form['confirmar_contraseña']

    # Verifica que las contraseñas coincidan
    if contraseña != confirmar_contraseña:
        flash('Las contraseñas no coinciden', 'danger')
        return redirect(url_for('crear'))

    # Inicializa el cursor
    cursor = mysql.connection.cursor()

    try:
        # Verifica si el usuario ya existe
        cursor.execute("SELECT COUNT(*) FROM sesiones WHERE usuario = %s", (email,))
        user_count = cursor.fetchone()[0]

        if user_count > 0:
            flash('El usuario ya existe', 'danger')
            return redirect(url_for('crear'))

        # Hashea la contraseña
        hashed_password = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())

        # Inserta el nuevo usuario
        sql = "INSERT INTO sesiones (usuario, contraseña) VALUES (%s, %s)"
        values = (email, hashed_password.decode('utf-8'))
        
        cursor.execute(sql, values)
        mysql.connection.commit()
        flash('Cuenta creada correctamente..!!')
        return redirect(url_for('sesion'))
    
    except Exception as e:
        flash('Error al crear la cuenta: {}'.format(str(e)), 'danger')
        return redirect(url_for('crear')) 
    finally:
        try:
            cursor.close()  # Cierra el cursor si se inicializó
        except Exception as e:
            print('Error al cerrar el cursor: {}'.format(str(e)))


#termina la creacion de cuenta hasta aqui

@app.route('/tabla')
def Index():

    cursor= mysql.connection.cursor()
    cursor.execute('SELECT * FROM crud1')
    data = cursor.fetchall()
   
    return render_template('Index.html',contactos=data)

@app.route('/add_contact', methods=['POST'])
def add_contact():    
    if request.method == 'POST':
        name = request.form['nombre']
        email = request.form['email']
        phone = request.form['phone']

        cursor = mysql.connection.cursor()
        
       
        sql = "INSERT INTO crud1 (name, email, phone) VALUES (%s, %s, %s)"
        values = (name, email, phone)  
        
        try:
            cursor.execute(sql, values)  
            mysql.connection.commit() 
            flash('Contacto agregado existosamente!!!')
  
            return  redirect(url_for('Index'))
        except Exception as e:
            return f'Error al agregar contacto: {str(e)}'
        finally:
            cursor.close() 

@app.route('/edit/<id>')
def get_contact(id):
    cursor = mysql.connection.cursor()
    sql= ('SELECT * FROM crud1 where id= %s')
    values =(id,)
    cursor.execute(sql,values)
    data= cursor.fetchall()
    return  render_template('edit-contact.html',contact=data[0])

@app.route('/update/<id>',methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
      name = request.form['nombre']
      email = request.form['email']
      phone = request.form['phone']

      cursor = mysql.connection.cursor()
      sql = 'UPDATE crud1 SET name=%s, email=%s,phone=%s WHERE id=%s'
      values = (name, email, phone, id) 
      cursor.execute(sql,values)
      cursor= mysql.connection.commit()
      flash('Contacto actualizado')
     
      return redirect(url_for('Index'))
    

@app.route('/delete_contact/<string:id>') 
def delete_contact(id):
  cursor=mysql.connection.cursor()
  sql= "DELETE FROM crud1 where id = %s"
  values =(id,)
  cursor.execute(sql,values)
  mysql.connection.commit() 

  flash('Contacto removido existosamente!!!')
  return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run(port=3000, debug=True)