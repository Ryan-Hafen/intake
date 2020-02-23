from srs_intake import db

db.create_all()

from srs_intake import Facility, User, Referral

facility_1=Facility(name='Facility 1',address1='123 Main',address2='',city='Lincoln', state='CA', zip_code='95648',source='alf')
facility_2=Facility(name='Facility 2',address1='123 Main',address2='',city='Lincoln', state='CA', zip_code='95648',source='hospital')
facility_3=Facility(name='Facility 3',address1='123 Main',address2='',city='Lincoln', state='CA', zip_code='95648',source='pcp')
facility_4=Facility(name='Facility 4',address1='123 Main',address2='',city='Lincoln', state='CA', zip_code='95648',source='snf')
facility_5=Facility(name='Facility 5',address1='123 Main',address2='',city='Lincoln', state='CA', zip_code='95648',source='specialist')
facility_6=Facility(name='Facility 6',address1='123 Main',address2='',city='Lincoln', state='CA', zip_code='95648',source='alf')
facility_7=Facility(name='Facility 7',address1='123 Main',address2='',city='Lincoln', state='CA', zip_code='95648',source='hospital')
facility_8=Facility(name='Facility 8',address1='123 Main',address2='',city='Lincoln', state='CA', zip_code='95648',source='pcp')
facility_9=Facility(name='Facility 9',address1='123 Main',address2='',city='Lincoln', state='CA', zip_code='95648',source='snf')
facility_10=Facility(name='Facility 10',address1='123 Main',address2='',city='Lincoln', state='CA', zip_code='95648',source='specialist')
facility_11=Facility(name='Facility 11',address1='123 Main',address2='',city='Lincoln', state='CA', zip_code='95648',source='alf')
facility_12=Facility(name='Facility 12',address1='123 Main',address2='',city='Lincoln', state='CA', zip_code='95648',source='hospital')
facility_13=Facility(name='Facility 13',address1='123 Main',address2='',city='Lincoln', state='CA', zip_code='95648',source='pcp')
facility_14=Facility(name='Facility 14',address1='123 Main',address2='',city='Lincoln', state='CA', zip_code='95648',source='snf')
facility_15=Facility(name='Facility 15',address1='123 Main',address2='',city='Lincoln', state='CA', zip_code='95648',source='specialist')
facility_16=Facility(name='Facility 16',address1='123 Main',address2='',city='Lincoln', state='CA', zip_code='95648',source='alf')
facility_17=Facility(name='Facility 17',address1='123 Main',address2='',city='Lincoln', state='CA', zip_code='95648',source='hospital')
facility_18=Facility(name='Facility 18',address1='123 Main',address2='',city='Lincoln', state='CA', zip_code='95648',source='pcp')
facility_19=Facility(name='Facility 19',address1='123 Main',address2='',city='Lincoln', state='CA', zip_code='95648',source='snf')
facility_20=Facility(name='Facility 20',address1='123 Main',address2='',city='Lincoln', state='CA', zip_code='95648',source='specialist')