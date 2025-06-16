from flask import Flask, render_template, session, redirect, url_for, flash, request, jsonify
import os
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell
from forms import Login, SearchBookForm, ChangePasswordForm, EditInfoForm, SearchStudentForm, NewStoreForm, StoreForm, BorrowForm
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
import time, datetime
import pymysql
import random

# Register PyMySQL as the MySQL driver
pymysql.install_as_MySQLdb()

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
manager = Manager(app)

app.config['SECRET_KEY'] = 'hard to guess string'
# MySQL configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@localhost/book_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)


def make_shell_context():
    return dict(app=app, db=db, Admin=Admin, Book=Book)


manager.add_command("shell", Shell(make_context=make_shell_context))

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'basic'
login_manager.login_view = 'login'
login_manager.login_message = u"请先登录。"


class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.String(6), primary_key=True)
    admin_name = db.Column(db.String(32))
    password = db.Column(db.String(24))
    right = db.Column(db.String(32))

    def __init__(self, admin_id, admin_name, password, right):
        self.admin_id = admin_id
        self.admin_name = admin_name
        self.password = password
        self.right = right

    def get_id(self):
        return self.admin_id

    def verify_password(self, password):
        if password == self.password:
            return True
        else:
            return False

    def __repr__(self):
        return '<Admin %r>' % self.admin_name


class Book(db.Model):
    __tablename__ = 'book'
    isbn = db.Column(db.String(13), primary_key=True)
    book_name = db.Column(db.String(64))
    author = db.Column(db.String(64))
    press = db.Column(db.String(32))
    class_name = db.Column(db.String(64))

    def __repr__(self):
        return '<Book %r>' % self.book_name


class Student(db.Model):
    __tablename__ = 'student'
    card_id = db.Column(db.String(8), primary_key=True)
    student_id = db.Column(db.String(9))
    student_name = db.Column(db.String(32))
    sex = db.Column(db.String(2))
    telephone = db.Column(db.String(11), nullable=True)
    enroll_date = db.Column(db.String(13))
    valid_date = db.Column(db.String(13))
    loss = db.Column(db.Boolean, default=False)  # 是否挂失
    debt = db.Column(db.Boolean, default=False)  # 是否欠费

    def __repr__(self):
        return '<Student %r>' % self.student_name


class Inventory(db.Model):
    __tablename__ = 'inventory'
    barcode = db.Column(db.String(6), primary_key=True)
    isbn = db.Column(db.ForeignKey('book.isbn'))
    storage_date = db.Column(db.String(13))
    location = db.Column(db.String(32))
    withdraw = db.Column(db.Boolean, default=False)  # 是否注销
    status = db.Column(db.Boolean, default=True)  # 是否在馆
    admin = db.Column(db.ForeignKey('admin.admin_id'))  # 入库操作员

    def __repr__(self):
        return '<Inventory %r>' % self.barcode


class ReadBook(db.Model):
    __tablename__ = 'readbook'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    barcode = db.Column(db.ForeignKey('inventory.barcode'), index=True)
    card_id = db.Column(db.ForeignKey('student.card_id'), index=True)
    start_date = db.Column(db.String(13))
    borrow_admin = db.Column(db.ForeignKey('admin.admin_id'))  # 借书操作员
    end_date = db.Column(db.String(13), nullable=True)
    return_admin = db.Column(db.ForeignKey('admin.admin_id'))  # 还书操作员
    due_date = db.Column(db.String(13))  # 应还日期

    def __repr__(self):
        return '<ReadBook %r>' % self.id


class LibraryInfo(db.Model):
    __tablename__ = 'library_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))  # 图书馆名称
    address = db.Column(db.String(128))  # 图书馆地址
    phone = db.Column(db.String(20))  # 联系电话
    email = db.Column(db.String(64))  # 电子邮箱
    opening_hours = db.Column(db.String(128))  # 开放时间
    description = db.Column(db.Text)  # 图书馆简介

    def __repr__(self):
        return '<LibraryInfo %r>' % self.name


class BookVocabulary(db.Model):
    __tablename__ = 'book_vocabulary'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    word = db.Column(db.String(64), unique=True)  # 词汇
    category = db.Column(db.String(32))  # 分类
    description = db.Column(db.Text)  # 描述

    def __repr__(self):
        return '<BookVocabulary %r>' % self.word


@login_manager.user_loader
def load_user(admin_id):
    return Admin.query.get(int(admin_id))


@app.route('/', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        user = Admin.query.filter_by(admin_id=form.account.data, password=form.password.data).first()
        if user is None:
            flash('账号或密码错误！')
            return redirect(url_for('login'))
        else:
            login_user(user)
            session['admin_id'] = user.admin_id
            session['name'] = user.admin_name
            return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经登出！')
    return redirect(url_for('login'))


@app.route('/index')
@login_required
def index():
    return render_template('index.html', name=session.get('name'))


@app.route('/echarts')
@login_required
def echarts():
    # 生成最近10天的日期
    days = []
    num = []
    today_date = datetime.date.today()
    today_str = today_date.strftime("%Y-%m-%d")
    today_stamp = time.mktime(time.strptime(today_str + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
    ten_ago = int(today_stamp) - 9 * 86400
    
    # 查询最近10天的借书和还书数据
    for i in range(0, 10):
        current_day = ten_ago + i * 86400
        next_day = current_day + 86400
        
        # 查询当天的借书数量
        borrow_count = ReadBook.query.filter(
            ReadBook.start_date >= current_day * 1000,
            ReadBook.start_date < next_day * 1000
        ).count()
        
        # 查询当天的还书数量
        return_count = ReadBook.query.filter(
            ReadBook.end_date >= current_day * 1000,
            ReadBook.end_date < next_day * 1000
        ).count()
        
        total_count = borrow_count + return_count
        
        date_str = time.strftime("%Y-%m-%d", time.localtime(current_day))
        days.append(date_str)
        num.append(total_count)
    
    data = []
    for i in range(0, 10):
        item = {'name': days[i], 'num': num[i]}
        data.append(item)
    return jsonify(data)


@app.route('/user/<id>')
@login_required
def user_info(id):
    user = Admin.query.filter_by(admin_id=id).first()
    return render_template('user-info.html', user=user, name=session.get('name'))


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.password2.data != form.password.data:
        flash(u'两次密码不一致！')
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash(u'已成功修改密码！')
            return redirect(url_for('index'))
        else:
            flash(u'原密码输入错误，修改失败！')
    return render_template("change-password.html", form=form)


@app.route('/change_info', methods=['GET', 'POST'])
@login_required
def change_info():
    form = EditInfoForm()
    if form.validate_on_submit():
        current_user.admin_name = form.name.data
        db.session.add(current_user)
        flash(u'已成功修改个人信息！')
        return redirect(url_for('user_info', id=current_user.admin_id))
    form.name.data = current_user.admin_name
    id = current_user.admin_id
    right = current_user.right
    return render_template('change-info.html', form=form, id=id, right=right)


@app.route('/search_book', methods=['GET', 'POST'])
@login_required
def search_book():  # 这个函数里不再处理提交按钮，使用Ajax局部刷新
    form = SearchBookForm()
    return render_template('search-book.html', name=session.get('name'), form=form)


@app.route('/books', methods=['POST'])
def find_book():

    def find_name():
        return Book.query.filter(Book.book_name.like('%'+request.form.get('content')+'%')).all()

    def find_author():
        return Book.query.filter(Book.author.contains(request.form.get('content'))).all()

    def find_class():
        return Book.query.filter(Book.class_name.contains(request.form.get('content'))).all()

    def find_isbn():
        return Book.query.filter(Book.isbn.contains(request.form.get('content'))).all()

    methods = {
        'book_name': find_name,
        'author': find_author,
        'class_name': find_class,
        'isbn': find_isbn
    }
    books = methods[request.form.get('method')]()
    data = []
    for book in books:
        count = Inventory.query.filter_by(isbn=book.isbn).count()
        available = Inventory.query.filter_by(isbn=book.isbn, status=True).count()
        item = {'isbn': book.isbn, 'book_name': book.book_name, 'press': book.press, 'author': book.author,
                'class_name': book.class_name, 'count': count, 'available': available}
        data.append(item)
    return jsonify(data)


@app.route('/all_books', methods=['GET'])
@login_required
def all_books():
    books = Book.query.all()
    return render_template('all-books.html', name=session.get('name'), books=books)


@app.route('/user/book', methods=['GET', 'POST'])
def user_book():
    form = SearchBookForm()
    return render_template('user-book.html', form=form)


@app.route('/search_student', methods=['GET', 'POST'])
@login_required
def search_student():
    form = SearchStudentForm()
    return render_template('search-student.html', name=session.get('name'), form=form)


def timeStamp(timeNum):
    if timeNum is None:
        return timeNum
    else:
        timeStamp = float(float(timeNum)/1000)
        timeArray = time.localtime(timeStamp)
        print(time.strftime("%Y-%m-%d", timeArray))
        return time.strftime("%Y-%m-%d", timeArray)


@app.route('/student', methods=['POST'])
def find_student():
    stu = Student.query.filter_by(card_id=request.form.get('card')).first()
    if stu is None:
        return jsonify([])
    else:
        valid_date = timeStamp(stu.valid_date)
        return jsonify([{'name': stu.student_name, 'gender': stu.sex, 'valid_date': valid_date, 'debt': stu.debt}])


@app.route('/all_students', methods=['GET'])
@login_required
def all_students():
    students = Student.query.all()
    return render_template('all-students.html', name=session.get('name'), students=students)


@app.route('/record', methods=['POST'])
def find_record():
    records = db.session.query(ReadBook).join(Inventory).join(Book).filter(ReadBook.card_id == request.form.get('card'))\
        .with_entities(ReadBook.barcode, Inventory.isbn, Book.book_name, Book.author, ReadBook.start_date,
                       ReadBook.end_date, ReadBook.due_date).all()  # with_entities啊啊啊啊卡了好久啊
    data = []
    for record in records:
        start_date = timeStamp(record.start_date)
        due_date = timeStamp(record.due_date)
        end_date = timeStamp(record.end_date)
        if end_date is None:
            end_date = '未归还'
        item = {'barcode': record.barcode, 'book_name': record.book_name, 'author': record.author,
                'start_date': start_date, 'due_date': due_date, 'end_date': end_date}
        data.append(item)
    return jsonify(data)


@app.route('/user/student', methods=['GET', 'POST'])
def user_student():
    form = SearchStudentForm()
    return render_template('user-student.html', form=form)


@app.route('/storage', methods=['GET', 'POST'])
@login_required
def storage():
    form = StoreForm()
    if form.validate_on_submit():
        book = Book.query.filter_by(isbn=request.form.get('isbn')).first()
        exist = Inventory.query.filter_by(barcode=request.form.get('barcode')).first()
        if book is None:
            flash(u"添加失败，请注意本书信息是否已录入，若未登记，请在'新书入库'窗口录入信息。")
        else:
            if len(request.form.get('barcode')) != 6:
                flash(u'图书编码长度错误')
            else:
                if exist is not None:
                    flash(u'该编号已经存在！')
                else:
                    item = Inventory()
                    item.barcode = request.form.get('barcode')
                    item.isbn = request.form.get('isbn')
                    item.admin = current_user.admin_id
                    item.location = request.form.get('location')
                    item.status = True
                    item.withdraw = False
                    today_date = datetime.date.today()
                    today_str = today_date.strftime("%Y-%m-%d")
                    today_stamp = time.mktime(time.strptime(today_str + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
                    item.storage_date = int(today_stamp)*1000
                    db.session.add(item)
                    db.session.commit()
                    flash(u'入库成功！')
        return redirect(url_for('storage'))
    return render_template('storage.html', name=session.get('name'), form=form)


@app.route('/new_store', methods=['GET', 'POST'])
@login_required
def new_store():
    form = NewStoreForm()
    if form.validate_on_submit():
        if len(request.form.get('isbn')) != 13:
            flash(u'ISBN长度错误')
        else:
            exist = Book.query.filter_by(isbn=request.form.get('isbn')).first()
            if exist is not None:
                flash(u'该图书信息已经存在，请核对后再录入；或者填写入库表。')
            else:
                book = Book()
                book.isbn = request.form.get('isbn')
                book.book_name = request.form.get('book_name')
                book.press = request.form.get('press')
                book.author = request.form.get('author')
                book.class_name = request.form.get('class_name')
                db.session.add(book)
                db.session.commit()
                flash(u'图书信息添加成功！')
        return redirect(url_for('new_store'))
    return render_template('new-store.html', name=session.get('name'), form=form)


@app.route('/borrow', methods=['GET', 'POST'])
@login_required
def borrow():
    form = BorrowForm()
    return render_template('borrow.html', name=session.get('name'), form=form)


@app.route('/find_stu_book', methods=['GET', 'POST'])
def find_stu_book():
    stu = Student.query.filter_by(card_id=request.form.get('card')).first()
    today_date = datetime.date.today()
    today_str = today_date.strftime("%Y-%m-%d")
    today_stamp = time.mktime(time.strptime(today_str + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
    if stu is None:
        return jsonify([{'stu': 0}])  # 没找到
    if stu.debt is True:
        return jsonify([{'stu': 1}])  # 欠费
    if int(stu.valid_date) < int(today_stamp)*1000:
        return jsonify([{'stu': 2}])  # 到期
    if stu.loss is True:
        return jsonify([{'stu': 3}])  # 已经挂失
    books = db.session.query(Book).join(Inventory).filter(Book.book_name.contains(request.form.get('book_name')),
        Inventory.status == 1).with_entities(Inventory.barcode, Book.isbn, Book.book_name, Book.author, Book.press).\
        all()
    data = []
    for book in books:
        item = {'barcode': book.barcode, 'isbn': book.isbn, 'book_name': book.book_name,
                'author': book.author, 'press': book.press}
        data.append(item)
    return jsonify(data)


@app.route('/out', methods=['GET', 'POST'])
@login_required
def out():
    today_date = datetime.date.today()
    today_str = today_date.strftime("%Y-%m-%d")
    today_stamp = time.mktime(time.strptime(today_str + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
    barcode = request.args.get('barcode')
    card = request.args.get('card')
    book_name = request.args.get('book_name')
    readbook = ReadBook()
    readbook.barcode = barcode
    readbook.card_id = card
    readbook.start_date = int(today_stamp)*1000
    readbook.due_date = (int(today_stamp)+40*86400)*1000
    readbook.borrow_admin = current_user.admin_id
    db.session.add(readbook)
    db.session.commit()
    book = Inventory.query.filter_by(barcode=barcode).first()
    book.status = False
    db.session.add(book)
    db.session.commit()
    bks = db.session.query(Book).join(Inventory).filter(Book.book_name.contains(book_name), Inventory.status == 1).\
        with_entities(Inventory.barcode, Book.isbn, Book.book_name, Book.author, Book.press).all()
    data = []
    for bk in bks:
        item = {'barcode': bk.barcode, 'isbn': bk.isbn, 'book_name': bk.book_name,
                'author': bk.author, 'press': bk.press}
        data.append(item)
    return jsonify(data)


@app.route('/return', methods=['GET', 'POST'])
@login_required
def return_book():
    form = SearchStudentForm()
    return render_template('return.html', name=session.get('name'), form=form)


@app.route('/find_not_return_book', methods=['GET', 'POST'])
def find_not_return_book():
    stu = Student.query.filter_by(card_id=request.form.get('card')).first()
    today_date = datetime.date.today()
    today_str = today_date.strftime("%Y-%m-%d")
    today_stamp = time.mktime(time.strptime(today_str + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
    if stu is None:
        return jsonify([{'stu': 0}])  # 没找到
    if stu.debt is True:
        return jsonify([{'stu': 1}])  # 欠费
    if int(stu.valid_date) < int(today_stamp)*1000:
        return jsonify([{'stu': 2}])  # 到期
    if stu.loss is True:
        return jsonify([{'stu': 3}])  # 已经挂失
    books = db.session.query(ReadBook).join(Inventory).join(Book).filter(ReadBook.card_id == request.form.get('card'),
        ReadBook.end_date.is_(None)).with_entities(ReadBook.barcode, Book.isbn, Book.book_name, ReadBook.start_date,
                                                 ReadBook.due_date).all()
    data = []
    for book in books:
        start_date = timeStamp(book.start_date)
        due_date = timeStamp(book.due_date)
        item = {'barcode': book.barcode, 'isbn': book.isbn, 'book_name': book.book_name,
                'start_date': start_date, 'due_date': due_date}
        data.append(item)
    return jsonify(data)


@app.route('/in', methods=['GET', 'POST'])
@login_required
def bookin():
    barcode = request.args.get('barcode')
    card = request.args.get('card')
    record = ReadBook.query.filter(ReadBook.barcode == barcode, ReadBook.card_id == card, ReadBook.end_date.is_(None)).\
        first()
    today_date = datetime.date.today()
    today_str = today_date.strftime("%Y-%m-%d")
    today_stamp = time.mktime(time.strptime(today_str + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
    record.end_date = int(today_stamp)*1000
    record.return_admin = current_user.admin_id
    db.session.add(record)
    db.session.commit()
    book = Inventory.query.filter_by(barcode=barcode).first()
    book.status = True
    db.session.add(book)
    db.session.commit()
    bks = db.session.query(ReadBook).join(Inventory).join(Book).filter(ReadBook.card_id == card,
        ReadBook.end_date.is_(None)).with_entities(ReadBook.barcode, Book.isbn, Book.book_name, ReadBook.start_date,
                                                 ReadBook.due_date).all()
    data = []
    for bk in bks:
        start_date = timeStamp(bk.start_date)
        due_date = timeStamp(bk.due_date)
        item = {'barcode': bk.barcode, 'isbn': bk.isbn, 'book_name': bk.book_name,
                'start_date': start_date, 'due_date': due_date}
        data.append(item)
    return jsonify(data)


@app.route('/withdraw', methods=['GET', 'POST'])
@login_required
def withdraw():
    form = SearchBookForm()
    return render_template('withdraw.html', name=session.get('name'), form=form)


@app.route('/find_withdraw_book', methods=['POST'])
def find_withdraw_book():
    method = request.form.get('method')
    content = request.form.get('content')
    
    query = db.session.query(Book).join(Inventory).filter(Inventory.withdraw == False)
    
    if method == 'book_name':
        query = query.filter(Book.book_name.contains(content))
    elif method == 'author':
        query = query.filter(Book.author.contains(content))
    elif method == 'class_name':
        query = query.filter(Book.class_name.contains(content))
    elif method == 'isbn':
        query = query.filter(Book.isbn.contains(content))
    
    books = query.with_entities(
        Inventory.barcode, Book.isbn, Book.book_name, 
        Book.author, Book.press, Inventory.location
    ).all()
    
    data = []
    for book in books:
        item = {
            'barcode': book.barcode,
            'isbn': book.isbn,
            'book_name': book.book_name,
            'author': book.author,
            'press': book.press,
            'location': book.location
        }
        data.append(item)
    return jsonify(data)


@app.route('/withdraw_book', methods=['POST'])
@login_required
def withdraw_book():
    barcode = request.form.get('barcode')
    book = Inventory.query.filter_by(barcode=barcode).first()
    if book:
        book.withdraw = True
        book.status = False
        db.session.add(book)
        db.session.commit()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'})


@app.route('/library_info', methods=['GET', 'POST'])
@login_required
def library_info():
    info = LibraryInfo.query.first()
    if request.method == 'POST':
        if info:
            info.name = request.form.get('name')
            info.address = request.form.get('address')
            info.phone = request.form.get('phone')
            info.email = request.form.get('email')
            info.opening_hours = request.form.get('opening_hours')
            info.description = request.form.get('description')
        else:
            info = LibraryInfo(
                name=request.form.get('name'),
                address=request.form.get('address'),
                phone=request.form.get('phone'),
                email=request.form.get('email'),
                opening_hours=request.form.get('opening_hours'),
                description=request.form.get('description')
            )
        db.session.add(info)
        db.session.commit()
        flash('图书馆信息更新成功！')
        return redirect(url_for('library_info'))
    return render_template('library-info.html', info=info, name=session.get('name'))


@app.route('/book_vocabulary', methods=['GET', 'POST'])
@login_required
def book_vocabulary():
    if request.method == 'POST':
        word = request.form.get('word')
        category = request.form.get('category')
        description = request.form.get('description')
        
        vocabulary = BookVocabulary(
            word=word,
            category=category,
            description=description
        )
        db.session.add(vocabulary)
        db.session.commit()
        flash('词汇添加成功！')
        return redirect(url_for('book_vocabulary'))
    
    vocabularies = BookVocabulary.query.all()
    return render_template('book-vocabulary.html', vocabularies=vocabularies, name=session.get('name'))


@app.route('/delete_vocabulary/<int:id>', methods=['POST'])
@login_required
def delete_vocabulary(id):
    vocabulary = BookVocabulary.query.get_or_404(id)
    db.session.delete(vocabulary)
    db.session.commit()
    flash('词汇删除成功！')
    return redirect(url_for('book_vocabulary'))


if __name__ == '__main__':
    manager.run()
