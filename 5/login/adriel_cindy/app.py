from flask import Flask, render_template, request, redirect, flash
import mongo

app = Flask(__name__)
app.secret_key = 'secret'

@app.route("/")
def home():
    user = request.args.get("user")
    password = request.args.get("pwd")
    login = request.args.get("login")
    register = request.args.get("register")

    if (login == "Login" and user != "" and password != ""):
        print mongo.get_password(user)
        if (password == mongo.get_password(user)):
            mongo.login_user(user)
            return redirect("/page/"+user)
        else:
            flash("Username or password is not valid.")
            return redirect("/")
        #return login
    elif (register == "r"):
        return redirect("/register")
    else:
        return render_template("home.html")

@app.route("/page")
@app.route("/page/<user>")
def page(user=None):
    if (user!=None and mongo.logged_in(user)=="y"):
        return render_template("user.html", user=user)
    return redirect("/")

@app.route("/profile")
@app.route("/profile/<user>")
def profile(user=None):
    if (user!=None and mongo.logged_in(user)=="y"):
        return render_template("profile.html", user=user)
    return redirect("/")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/logout/<user>")
def logout(user=None):
    mongo.logout_user(user)
    flash("Logged out successfully")
    return redirect("/")

@app.route("/register")
def register():
    user = request.args.get("user")
    password = request.args.get("pwd")
    pcheck = request.args.get("pwdcheck")
    register = request.args.get("register")

    if (user != None and password != None and pcheck != None):
        if (password == pcheck and not(mongo.exists_user(user))):
            mongo.add_user(user,password)
            return redirect("/page/"+user)
        if (mongo.exists_user(user)):
            flash("This username is taken.")
            return redirect("/register")
            #return login
        if (password != pcheck):
            flash("The passwords do not match.")
            return redirect("/register")
    else:
        return render_template("register.html")

    
if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')

    
