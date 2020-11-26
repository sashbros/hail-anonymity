from flask import Flask, render_template, request, flash
import mysql.connector

# mydb = mysql.connector.connect(host="",
#                                 user="",
#                                 password="",
#                                 database="",
#                                 auth_plugin='')

mydb = mysql.connector.connect(host="",
                                user="",
                                password="",
                                database="",
                                auth_plugin='')
mycursor = mydb.cursor()

# mycursor.execute("create table posts(p_id int(5) primary key, p_des varchar(200))")
# mycursor.execute("insert into posts values(1, "First Post")")

app = Flask(__name__)
app.secret_key = "sashbros is god"


curr_sub = ""

# @app.route('/')
# def signUp():
#     return render_template("homepage.html")


@app.route('/', methods = ['POST', 'GET'])
def home():
    if request.method == 'POST':
        
        post = request.form["comment"]
        post = post.strip()
        
        
        stopwords = [] #words we do not want in posts
        
        for word in stopwords:
            if word in post:
                post = post.replace(word, "**")


        myquery = "select p_id from posts order by p_id desc limit 1"
        mycursor.execute(myquery)

        new_p_id = mycursor.fetchone()[0] + 1
        
        myquery = "select exists(select * from posts where p_des=%s)"
        rec_tup = (post,)
        mycursor.execute(myquery, rec_tup)
        if mycursor.fetchone()[0]==0:
            myquery = "insert into posts values(%s, %s)"
            rec_tup = (new_p_id, post)
            mycursor.execute(myquery, rec_tup)
            mydb.commit()
        else:
            flash("Looks like you want to REFRESH or REPEAT posts!! Type something unique please!!")
        
        mycursor.execute("select distinct p_des from posts order by p_id desc")
        data = mycursor.fetchall()
            
        return render_template("homePage.html", data=data)
    
    mycursor.execute("select distinct p_des from posts order by p_id desc")
    data = mycursor.fetchall()    
    return render_template("homePage.html", data=data)


if __name__ == "__main__":
    
    app.run(debug=True, port=3000)
