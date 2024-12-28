from StudentManage.models import QuyDinh, MonHoc
from StudentManage import app, dao, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, AdminIndexView
from flask_login import logout_user, current_user
from flask import redirect, request, render_template

admin = Admin(app=app, name='Quản lý học sinh', template_mode='bootstrap4')

class MySubjectView(ModelView):
    column_list = ['monHoc_id', 'tenMH']
    column_searchable_list = ['tenMH']

admin.add_view(ModelView(QuyDinh, db.session))
admin.add_view(MySubjectView(MonHoc, db.session))