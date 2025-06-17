# -*- coding: utf-8 -*-
# 表单定义文件，包含所有WTForms表单类

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length

# 登录表单
class Login(FlaskForm):
    account = StringField(u'账号', validators=[DataRequired()])  # 账号字段
    password = PasswordField(u'密码', validators=[DataRequired()])  # 密码字段
    submit = SubmitField(u'登录')  # 登录按钮

# 修改密码表单
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(u'原密码', validators=[DataRequired()])  # 原密码
    password = PasswordField(u'新密码', validators=[DataRequired(), EqualTo('password2', message=u'两次密码必须一致！')])  # 新密码
    password2 = PasswordField(u'确认新密码', validators=[DataRequired()])  # 确认新密码
    submit = SubmitField(u'确认修改')  # 提交按钮

# 修改个人信息表单
class EditInfoForm(FlaskForm):
    name = StringField(u'用户名', validators=[Length(1, 32)])  # 用户名
    submit = SubmitField(u'提交')  # 提交按钮

# 图书查询表单
class SearchBookForm(FlaskForm):
    methods = [('book_name', '书名'), ('author', '作者'), ('class_name', '类别'), ('isbn', 'ISBN')]
    method = SelectField(choices=methods, validators=[DataRequired()], coerce=str)  # 查询方式
    content = StringField(validators=[DataRequired()])  # 查询内容
    submit = SubmitField('搜索')  # 搜索按钮

# 学生查询表单
class SearchStudentForm(FlaskForm):
    card = StringField(validators=[DataRequired()])  # 借书证号
    submit = SubmitField('搜索')  # 搜索按钮

# 入库表单
class StoreForm(FlaskForm):
    barcode = StringField(validators=[DataRequired(), Length(6)])  # 馆藏条码
    isbn = StringField(validators=[DataRequired(), Length(13)])  # ISBN
    location = StringField(validators=[DataRequired(), Length(1, 32)])  # 馆藏位置
    submit = SubmitField(u'提交')  # 提交按钮

# 新书信息登记表单
class NewStoreForm(FlaskForm):
    isbn = StringField(validators=[DataRequired(), Length(13)])  # ISBN
    book_name = StringField(validators=[DataRequired(), Length(1, 64)])  # 书名
    press = StringField(validators=[DataRequired(), Length(1, 32)])  # 出版社
    author = StringField(validators=[DataRequired(), Length(1, 64)])  # 作者
    class_name = StringField(validators=[DataRequired(), Length(1, 64)])  # 类别
    submit = SubmitField(u'提交')  # 提交按钮

# 借书表单
class BorrowForm(FlaskForm):
    card = StringField(validators=[DataRequired()])  # 借书证号
    book_name = StringField(validators=[DataRequired()])  # 书名
    submit = SubmitField(u'搜索')  # 搜索按钮
