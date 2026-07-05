from app.extensions import db
class Attendance(db.Model):
    __tablename__='attendances'
    attendance_id=db.Column()