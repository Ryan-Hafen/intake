from srs_intake import db
from srs_intake import Facility, User, Referral

fac = Facility.query.first()
user = User.query.first()
ref = Referral.query.first()

print(fac)
print(user)
print(ref)

print(fac.submitter)
print(user.user_loc)
print(ref.referral_loc)
print(fac.loc_ref)
print(user.user_ref)

