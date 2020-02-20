from srs_intake import db

db.create_all()

from srs_intake import Facility, User, Referral

fac_1 = Facility(name='test_facility',address1='123Main',address2='',city='Lincoln',state='CA',zip_code='95648',source='SLA')
user_1 = User(firstname='ryan',lastname='hafen',email='ryan.hafen@icloud.com',phone='9164729612',fax='111111111',role='admin',username='ryan',password='password',facility_id=1)
ref_1 = Referral(firstname='test',lastname='patient',address1='',address2='123Main',city='Lincoln',state='CA',zip_code='95648',email='test@test.com',phone='1234567891',fax='1234567891',ssn='123456789',medicare='123123123',secondary='123123132',notes='',treat_other_desc='',med_firstname='test',med_lastname='med',med_address1='123Main',med_address2='',med_city='Lincoln',med_state='CA',med_zip_code='95648',med_email='test@test.com',med_phone='1234567891',med_fax='',med_npi='123456789',user_id=1,facility_id=1)

db.session.add(fac_1)
db.session.add(user_1)
db.session.add(ref_1)

db.session.commit()



