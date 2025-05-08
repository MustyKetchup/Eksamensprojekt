from flask import Flask, g, render_template, request, redirect, url_for, flash, session
import sqlite3


app = Flask(__name__)

app.secret_key = 'your-secret-key' 



@app.route("/")
def home():
    return render_template("home.html")


@app.route("/Create", methods= ["POST","GET"])
def create():
    if request.method == "POST":
        try:    
            username = request.form.get("username")
            password = request.form.get("password")
            #Eksempel på en execution. 
            #connects tao the dattabase
            con = sqlite3.connect("database.db")
            #In order to execute SQL commands, we need to have a database cursor.
            cur = con.cursor()

            cur.execute('''
                        INSERT OR IGNORE INTO User (UserName, UserPassword) VALUES (?, ?)
                ''', (f"{username}", f"{password}"))
            #Commits the changes.
            con.commit()
        #Error handeling  
        except sqlite3.Error as e:
            flash(f"Database error: {e}", "error")
        except Exception as e:
                flash(f"An error occurred: {e}", "error")
                return render_template("Create.html")
        return render_template("Login.html")
    

    return render_template("Create.html")

@app.route("/Login", methods = ["GET","POST"])
def login():
    if request.method == "POST":
        try:
            #Get the data from the html file, ("name atribute")
            username = request.form.get("username")
            password = request.form.get("password")

            #If no username or password are provided, render the same html file. 
            if not username or not password:
                flash("Username and passsword is required","Error")
                return render_template("Login.html")
            
            con = sqlite3.connect("database.db")
            #In order to execute SQL commands, we need to have a database cursor.
            cur = con.cursor()
            #Check of user is in databse
            cur.execute("SELECT UserID, UserName, UserPassword from User WHERE UserName = ? AND UserPassword = ?",
            (username,password)
                        )
            
            #Is this line of code beneath needed? 
            user = cur.fetchone()

            if user:
                session['user_id'] = user[0]
                return redirect(url_for("shop"))
                
            
        #Error handeling  
        except sqlite3.Error as e:
                flash(f"Database error: {e}", "error")
                return render_template("Login.html")


    return render_template("Login.html")


#Fix code
@app.route("/shop", methods=["POST","GET"])
def shop():

    con = sqlite3.connect("database.db")
    cur = con.cursor()

    cur.execute("SELECT ProductID, ProductName, Price, Quantity FROM Stock")
    #En liste der indehoider en touple med produkternes information
    Products = cur.fetchall()



    return render_template("shop.html",Products = Products)


@app.route("/kurv", methods=["GET","POST"])
def kurv():
    ProductID =request.form.get("product_id")


    con = sqlite3.connect("database.db")
    cur = con.cursor()

    user_id = session.get("user_id") 
    print(user_id)

    quantity = 1 #adding 1 item

    cur.execute("SELECT Quantity From Stock WHERE ProductID = ?",(ProductID))

    Stock = cur.fetchone()

    #if a given product with a product ID, is out of stock, redirect to shop page. 
    if Stock[0] < quantity: 
        flash("Sorry, this item is out of stock")   
        return redirect(url_for("shop"))


    #Update4 the Stock tabel, and for a product with the ID,, decrease the value by 1. 
    cur.execute("UPDATE Stock SET Quantity = Quantity - ? WHERE ProductID = ?", (quantity,ProductID))

    #Put stuff inside the Basket
    cur.execute("INSERT INTO Basket (UserID, ProductID, ProductQuantity) VALUES (? , ?, ?)", (user_id, ProductID , quantity ))  
    con.commit()


    # Fetch basket contents with ProductName
    cur.execute("""
        SELECT b.ProductQuantity, s.ProductName 
        FROM Basket b 
        JOIN Stock s ON b.ProductID = s.ProductID 
        WHERE b.UserID = ?
    """, (user_id,))
    User_basket = cur.fetchall()

    return render_template("kurv.html",User_basket = User_basket)



if __name__ == "__main__":
    app.run(debug=True)