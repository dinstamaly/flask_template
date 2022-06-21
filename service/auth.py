import hashlib
import uuid
from datetime import datetime

from core_lib.codes import INVALID_LOGIN_PASS, USER_BLOCKED
from core_lib.models import db, User, Device
from core_lib.utils import BusinessException


def logon(bag):
    # m = hashlib.sha256()
    # m.update(bag['password'].encode('utf-8'))
    # v_pass = m.hexdigest()
    user = db.session.query(User).filter(User.f_username == bag['username'].lower()).first()
    if user.f_password != bag['password']:
        raise BusinessException(INVALID_LOGIN_PASS)
    if user is None:
        raise BusinessException(INVALID_LOGIN_PASS)
    if user.f_blocked:
        raise BusinessException(USER_BLOCKED)

    device = db.session.query(Device) \
        .filter(Device.f_user_id == user.id) \
        .first()
    if device is None:
        device = Device()
    device.f_date = datetime.now()
    device.f_device_id = bag.get('device_id', 'web')
    device.f_device_name = bag.get('device') or bag.get('device_name')
    device.f_language = bag.get('lang', 'ru')
    # device
    device.f_user_id = user.id
    device.f_token = str(uuid.uuid4())  # generate unique token
    db.session.add(device)
    db.session.commit()

    result = {'user_id': user.id, 'session': device.f_token, 'name': user.f_name}
    return result

