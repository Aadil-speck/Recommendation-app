from App.models import NotificationRequest
from App.database import db

# Notification request code

def send_notif(staffID, requestBody):
    newnotif = NotificationRequest(sentToStaffID=staffID, requestBody = requestBody)
    db.session.add(newnotif)
    db.session.commit()
    return newnotif
