import hashlib
import math
from datetime import datetime

from core_lib.codes import NO_DATA_FOUND
from core_lib.models import User, db
from core_lib.utils import BusinessException


def user_list(bag):
    if not bag.get('page'):
        bag['page'] = 1
    if not bag.get('count'):
        bag['count'] = 50
    user_query = db.session.query(User)

    if bag.get('username'):
        user_query = user_query.filter(User.f_username.ilike('%{}%'.format(bag['username'])))
    if bag.get('name'):
        user_query = user_query.filter(User.f_name.ilike('%{}%'.format(bag['name'])))
    if bag.get('position'):
        user_query = user_query.filter(User.f_position.ilike('%{}%'.format(bag['position'])))

    total_count = user_query.count()
    user_query = user_query.order_by(User.f_name.asc())
    user_query = user_query.paginate(bag['page'], bag['count'], False).items
    result_list = []
    for u in user_query:
        user_json = {
            'id': u.id,
            'name': u.f_name,
            'username': u.f_username,
            'email': u.f_email,
            'phone': u.f_phone,
            'position': u.f_position,
        }

        result_list.append(user_json)

    return {'list': result_list, 'total': total_count, 'page_count': math.ceil(total_count / bag['count'])}


def add_user(bag):
    if bag.get('password'):
        m = hashlib.sha256()
        m.update(bag['password'].encode('utf-8'))
        bag['password'] = m.hexdigest()
    user = User()
    user.f_name = bag['name']
    user.f_password = bag.get('password')
    user.f_phone = bag.get('phone')
    user.f_email = bag.get('email')
    user.f_date_create = datetime.now()
    user.f_blocked = False
    user.f_position = bag.get('position')
    user.f_username = bag['username']

    db.session.add(user)
    db.session.commit()

    return {'id': user.id}


def edit_user(bag):
    user = db.session.query(User).filter(User.id == bag['id']).first()
    if not user:
        raise BusinessException(NO_DATA_FOUND, 'Пользователь не найден по ID: {}'.format(bag['id']))
    if bag.get('password'):
        m = hashlib.sha256()
        m.update(bag['password'].encode('utf-8'))
        bag['password'] = m.hexdigest()
        user.f_password = bag.get('password')
    user.f_name = bag['name']
    user.f_phone = bag.get('phone')
    user.f_position = bag.get('position')
    user.f_email = bag.get('email')
    user.f_username = bag['username']

    db.session.add(user)
    db.session.commit()

    return {'id': user.id}


def delete_user(bag):
    user = db.session.query(User).filter(User.id == bag['id']).first()
    if not user:
        raise BusinessException(NO_DATA_FOUND, 'Пользователь не найден по ID: {}'.format(bag['id']))

    db.session.delete(user)

    return {}
