from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy #zarzadzanie baza danych
from datetime import datetime
#tworzenie apki flaska
app=Flask(__name__)
#path to database,przechowuje dane lokalnie w pliku
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
db=SQLAlchemy(app)

#models of posts
class BlogPosts(db.Model):
    id=db.Column(db.Integer,primary_key=True)#id alwayse unique
    title=db.Column(db.String(100),nullable=False,default='non title')#you need to put something into "title",max 100 characters
    content=db.Column(db.Text,nullable=False,default='non content')
    author=db.Column(db.String(20),nullable=False,default='None author')
    date_created=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __repr__(self):#identify every blog
        return "Blog posted" +':'+ str(self.id)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts',methods=['GET','POST'])#allow posting and getiing respond
def posts():
    if request.method=='POST':
        post_title=request.form['title']
        post_content=request.form['content']
        post_author=request.form['author']
        new_post=BlogPosts(title=post_title,content=post_content,author=post_author)
        db.session.add(new_post)#add new posts to database but only for time of session
        db.session.commit()#save database for pernm
        return redirect('/posts')
    else:
        my_posts=BlogPosts.query.order_by(BlogPosts.date_created).all()
        return render_template('posts.html',posts=my_posts)

@app.route('/posts/delete/<int:id>')
def delete(id):
    post=BlogPosts.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')
@app.route('/posts/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    post = BlogPosts.query.get_or_404(id)
    if request.method=='POST':

        post.title=request.form['title']
        post.author=request.form['author']
        post.content=request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html',post=post)




#mowi Ci gdzie jestes na stronei tak naprawde
#puting bettwen the brec name will give your webside this "url" name , if not , you will get a private url there:http://127.0.0.1:5000/http://127.0.0.1:5000/
@app.route('/home/<string:name>')
def hello(name):
    return "hello,"+name
@app.route('/onlyget',methods=['GET'])
def get_req():
    return "only get ale avalible"

if __name__=="__main__":
    app.run(debug=True)
    #pozwala nam zarzadzac serwerem
