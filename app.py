from flask import Flask, render_template, request, redirect
import mysql.connector
from datetime import datetime

now = datetime.now()
formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234",
  database="fuel_delivery_app"
)
mycursor = mydb.cursor()

app=Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin_register", methods=["POST", "GET"])
def admin_register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        sql = "INSERT INTO admin_detail (username, email, password) VALUES (%s, %s, %s)"
        val = (username, email, password)
        mycursor.execute(sql, val)
        mydb.commit()
        if mycursor.rowcount == 1:
           return render_template("admin_login.html") 

    return render_template("admin_register.html")

@app.route("/admin_login", methods=["POST", "GET"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        sql = "select * from admin_detail where username=%s and password=%s"
        val = (username, password)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        print(mycursor.rowcount)
        if int(mycursor.rowcount) == 1:
           return redirect("admin_dashboard") 
        
    return render_template("admin_login.html")

@app.route("/admin_dashboard", methods=["POST", "GET"])
def admin_dashboard():
    mycursor.execute("SELECT id, gas_type, location, quantity_available FROM gas_inventory")
    myresult = mycursor.fetchall()
    print(list(myresult))
    return render_template("admin_dashboard.html", myresult=list(myresult))

@app.route("/admin_order", methods=["POST", "GET"])
def admin_order():
    mycursor.execute("SELECT * FROM order_detail")
    myresult = mycursor.fetchall()
    print(list(myresult))
    return render_template("admin_order.html", myresult=list(myresult))




@app.route("/admin_view_user", methods=["POST", "GET"])
def admin_view_user():
    mycursor.execute("SELECT id, username, email FROM user_detail")
    myresult = mycursor.fetchall()
    print(list(myresult))
    return render_template("admin_view_user.html", myresult=list(myresult))


@app.route("/inv_update", methods=["POST", "GET"], endpoint='inv_update')
def inv_update():
    id = request.args.get("id")
    
    return render_template("inv_update_submit.html", id=id)


@app.route("/inv_update_submit", methods=["POST", "GET"])
def inv_update_submit():
    id = request.args.get("id")
    gas_type = request.args.get("gas_type")
    gas_location = request.args.get("gas_location")
    gas_available_quant = request.args.get("gas_available_quant")
    mycursor.execute("UPDATE gas_inventory SET gas_type=%s, location=%s, quantity_available=%s where id=%s",(gas_type,gas_location,gas_available_quant,id))
    mydb.commit()
    
    return redirect("admin_dashboard")

@app.route("/inv_add", methods=["POST", "GET"])
def inv_add():
    return render_template("inv_add.html")

@app.route("/inv_add_submit", methods=["POST", "GET"])
def inv_add_submit():
    gas_type = request.args.get("gas_type")
    gas_location = request.args.get("gas_location")
    gas_available_quant = request.args.get("gas_available_quant")
    mycursor.execute("INSERT INTO gas_inventory (gas_type, location, quantity_available) VALUES (%s,%s,%s)",(gas_type,gas_location,gas_available_quant))
    mydb.commit()
    
    return redirect("admin_dashboard")


@app.route("/inv_delete", methods=["POST", "GET"], endpoint='inv_delete')
def inv_delete():
    id = request.args.get("id")
    mycursor.execute("DELETE FROM gas_inventory where id=%s",(id,))
    mydb.commit()
    
    return redirect("admin_dashboard")


@app.route("/gas_station_register", methods=["POST", "GET"])
def gas_station_register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        sql = "INSERT INTO gas_station_detail (username, email, password) VALUES (%s, %s, %s)"
        val = (username, email, password)
        mycursor.execute(sql, val)
        mydb.commit()
        if mycursor.rowcount == 1:
           return render_template("gas_station_login.html") 

    return render_template("gas_station_register.html")

@app.route("/gas_station_login", methods=["POST", "GET"])
def gas_station_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        sql = "select * from gas_station_detail where username=%s and password=%s"
        val = (username, password)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        print(mycursor.rowcount)
        if int(mycursor.rowcount) == 1:
           return redirect("gas_station_dashboard") 
        
    return render_template("gas_station_login.html")

@app.route("/gas_station_dashboard", methods=["POST", "GET"])
def gas_station_dashboard():
    mycursor.execute("SELECT id, gas_type, location, quantity_available FROM gas_inventory")
    myresult = mycursor.fetchall()
    print(list(myresult))
    return render_template("gas_station_dashboard.html", myresult=myresult)

@app.route("/gas_inv_update", methods=["POST", "GET"], endpoint='gas_inv_update')
def gas_inv_update():
    id = request.args.get("id")
    
    return render_template("gas_inv_update_submit.html", id=id)


@app.route("/gas_inv_update_submit", methods=["POST", "GET"])
def gas_inv_update_submit():
    id = request.args.get("id")
    gas_type = request.args.get("gas_type")
    gas_location = request.args.get("gas_location")
    gas_available_quant = request.args.get("gas_available_quant")
    mycursor.execute("UPDATE gas_inventory SET gas_type=%s, location=%s, quantity_available=%s where id=%s",(gas_type,gas_location,gas_available_quant,id))
    mydb.commit()
    
    return redirect("gas_station_dashboard")

@app.route("/gas_inv_delete", methods=["POST", "GET"], endpoint='gas_inv_delete')
def gas_inv_delete():
    id = request.args.get("id")
    mycursor.execute("DELETE FROM gas_inventory where id=%s",(id,))
    mydb.commit()
    
    return redirect("gas_station_dashboard")

@app.route("/gas_order", methods=["POST", "GET"])
def gas_order():
    mycursor.execute("SELECT * FROM order_detail")
    myresult = mycursor.fetchall()
    print(list(myresult))
    return render_template("gas_station_orders.html", myresult=myresult)



@app.route("/user_register", methods=["POST", "GET"])
def user_register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        sql = "INSERT INTO user_detail (username, email, password) VALUES (%s, %s, %s)"
        val = (username, email, password)
        mycursor.execute(sql, val)
        mydb.commit()
        if mycursor.rowcount == 1:
           return render_template("user_login.html") 

    return render_template("user_register.html")

@app.route("/user_login", methods=["POST", "GET"])
def user_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        global client_user
        client_user = username
        
        sql = "select * from user_detail where username=%s and password=%s"
        val = (username, password)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        print(mycursor.rowcount)
        if int(mycursor.rowcount) == 1:
           return redirect("user_dashboard") 
        
    return render_template("user_login.html")

@app.route("/user_dashboard", methods=["POST", "GET"])
def user_dashboard():
    return render_template("user_dashboard.html", client_user=client_user)

@app.route("/user_order", methods=["POST", "GET"])
def user_order():
    user_id = request.args.get("user_id")
    gas_id = request.args.get("gas_id")
    gas_quant = request.args.get("gas_quant")
    gas_status = request.args.get("gas_status")

    mycursor.execute("INSERT INTO order_detail (user_id, gas_id, quantity, status, date) VALUES (%s,%s,%s,%s,%s)",(user_id, gas_id, gas_quant, gas_status, formatted_date))
    mydb.commit()


    # mycursor.execute("SELECT gas_id, quantity, date, status FROM order_detail where user_id=%s",(user_id,))
    # myresult = mycursor.fetchall()
    # print(list(myresult))
    return redirect("user_order_all")

@app.route("/user_order_all", methods=["POST", "GET"])
def user_order_all():
    mycursor.execute("SELECT gas_id, quantity, date, status FROM order_detail where user_id=%s",(client_user,))
    myresult = mycursor.fetchall()
    print(list(myresult))
    return render_template("user_order.html", myresult=myresult)

@app.route("/user_gas_available", methods=["POST", "GET"])
def user_gas_available():
    mycursor.execute("SELECT gas_type, location, quantity_available FROM gas_inventory")
    myresult = mycursor.fetchall()
    print(list(myresult))
    return render_template("user_gas_available.html", myresult=myresult)



if __name__=="__main__":
    app.run(debug=True)