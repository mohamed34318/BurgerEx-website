# from crypt import methods
from statistics import quantiles
from database import get_db 
from fileinput import filename
from werkzeug.utils import secure_filename
import os
from fileinput import filename
import database
from flask import Flask,render_template,url_for,redirect,request

app=Flask(__name__)

@app.route("/")
def hello_page() :
    return "hello"

@app.route("/home")
def home_page() :
    return render_template("Home.html")

@app.route("/adduser" ,methods=("GET", "POST"))
def add_manage_user() :
    if request.method=="POST" :
        firstname=request.form['firstname']
        gender=request.form['gender']
        age=int(request.form['age'])
        email=request.form['email']
        address_user=request.form['address_user']
        password_user=request.form['password_user']
        con=get_db()
        con.execute(f"insert into customers (firstname, gender,age,email,address_user,password_user) values('{firstname}','{gender}',{age},'{email}','{address_user}','{password_user}')")
        con.commit()
        con.close()
        return redirect(url_for('manage_user'))
    return render_template("add_user.html")


@app.route("/manageuser")
def manage_user() :
    con=get_db().cursor()
    con.execute("select * from customers ;")
    rows=con.fetchall()
    con.close()
    return render_template("Manage_users.html",rows=rows )
 
@app.route("/removeuser/<int:id>")
def remove_user_page(id) :
    con=get_db()
    con.execute(f"delete from customers where id={id}")
    con.commit()
    con.close()   
    return redirect(url_for('manage_user'))



@app.route("/updateuser/<int:id>" ,methods=("GET", "POST"))
def update_user_page(id) :
    if request.method=="POST" :
        firstname=request.form['firstname']
        gender=request.form['gender']
        age=int(request.form['age'])
        email=request.form['email']
        address_user=request.form['address_user']
        password_user=request.form['password_user']
        con=get_db()
        con.execute(f"update customers set firstname='{firstname}', gender='{gender}',age = {age},email='{email}',address_user='{address_user}',password_user='{password_user}' where id={id}")
        con.commit()
        con.close()
        return redirect(url_for('manage_user'))
    con=get_db().cursor()
    con.execute(f"select * from customers where id={id};")
    row=con.fetchone()
    con.close()   
    return render_template("update_user_page.html",row=row)
# ***************************************************************************************
 
@app.route("/managepost")
def manage_post() :
    con=get_db().cursor()
    con.execute("select *  from products  ;")
    rows=con.fetchall()
    con.close()
    return render_template("Manage_posts.html",rows=rows)




@app.route("/addpost" ,methods=("GET" ,"POST"))
def add_post() :
    if request.method=="POST" :
        productname=request.form['productname']
        price=float(request.form['price'])
        stars=int(request.form['stars'])
        quantity=int(request.form['quantity'])
      #uploade files
        if 'imfile' not in request.files :
            # flash("there is no files") 
            return redirect(request.url)   
        file=request.files['imfile']
        filename=secure_filename(file.filename)   
        file.save(os.path.join('static', 'upload' ,filename))
      # insert to data base
        con=get_db()
        con.execute(f"insert into products (productname ,price, stars ,quantity ,image_file)  values('{productname}',{price},{stars}, {quantity} ,'{filename}')")
        con.commit()
        con.close()
        return redirect(url_for('manage_post'),url_for('menu_page'))
    return render_template("add_post.html")


@app.route("/menu")
def menu_page() :
    con=get_db().cursor()
    con.execute("select * from products ;")
    rows=con.fetchall()
    con.close()
    
    return render_template("menu_page.html",rows=rows)



@app.route("/updatepost/<int:id_product>" ,methods=("GET", "POST"))
def update_post_page(id_product) :
    if request.method=="POST" :
        productname=request.form['productname']
        price=float(request.form['price'])
        stars=int(request.form['stars'])
        quantity=int(request.form['quantity'])
      #uploade files
        if 'imfile' not in request.files :
            # flash("there is no files") 
            return redirect(request.url)   
        file=request.files['imfile']
        filename=secure_filename(file.filename)   
        file.save(os.path.join('static', 'upload' ,filename))
# insert to data base
        con=get_db()
        con.execute(f"update products set productname='{productname}', price= {price},stars ={stars},quantity={quantity} ,image_file='{filename}' where id_product={id_product} ")
        con.commit()
        con.close()
        return redirect(url_for('manage_post'),url_for('menu_page'))
    con=get_db().cursor()
    con.execute(f"select * from products where id_product={id_product};")
    rows=con.fetchone()
    con.close()   
    return render_template("update_post_page.html",rows=rows)

@app.route("/removepost/<int:id_product>")
def remove_post_page(id_product) :
    con=get_db()
    con.execute(f"delete from products where id_product={id_product}")
    con.commit()
    con.close()   
    return redirect(url_for('manage_post'),url_for('menu_page'))

# ****************************************************************


@app.route("/manageorder")
def manage_order() :
    con=get_db().cursor()
    con.execute(f"select *  from products, customers ;")    
    rows=con.fetchall()
    con.close()
    return render_template("manage_order.html",rows=rows)



@app.route("/updateorder/<int:id_product>" , methods=("GET" ,"POST"))
def update_order(id_product) :
    if request.method=="POST" :
        productname=request.form['productname']
        address_user=request.form['address_user']
        firstname=request.form['firstname']
        con=get_db()
        con.execute(f"update customers set  firstname='{firstname}' , address_user='{address_user}'  where  id={id_product} ;")
        con.execute(f"update products  set productname='{productname}'  where  id_product={id_product} ;")
        con.commit()
        con.close()
        return redirect(url_for('manage_order'))        
    con=get_db().cursor()
    con.execute(f"select * from products , customers where id_product={id_product};")    
    rows=con.fetchone()
    con.close()
    return render_template("update_order_page.html", rows=rows)


@app.route("/removeorder/<int:id_product>")
def remove_order_page(id_product) :
    con=get_db()
    con.execute(f"delete from products where id_product={id_product}")
    con.execute(f"delete from customers where id={id_product}")
    con.commit()
    con.close()   
    return redirect(url_for('manage_order'))


@app.route("/burgerEx")
def base_page() :
    return render_template("burgerEx.html")

# **********************************************************************





@app.route("/checkout/<int:id_product>",methods=("POST" ,"GET"))
def checkout_page(id_product) :
    if request.method=="POST" :
        quantity=request.form['quantity']
        con=get_db()
        con.execute(f"update products set quantity={quantity} where id_product={id_product}")
        con.commit()
        con.close()
        return redirect(url_for('checkout_page', id_product=id_product) )
    con=get_db().cursor()
    con.execute(f"select * from products where id_product={id_product} ;")
    rows=con.fetchone()
    con.close()
    return render_template("checkout.html",rows=rows )

    
@app.route("/login")
def login_page() :
    return render_template('login.html ')


@app.route("/registry",methods=("POST" ,"GET"))
def registry_page_user() :
    if request.method=="POST" :
        firstname=request.form['firstname']
        gender=request.form['gender']
        age=int(request.form['age'])
        email=request.form['email']
        address_user=request.form['address_user']
        password_user=request.form['password_user']
        con=get_db()
        con.execute(f"insert into customers (firstname, gender,age,email,address_user,password_user) values('{firstname}','{gender}',{age},'{email}','{address_user}','{password_user}')")
        con.commit()
        con.close()
        return redirect(url_for('base_page'),url_for('manage_user'))
    return render_template("registry_page.html")
