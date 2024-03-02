from data.creator import Creator
from data.boost import Boost
from repo.FirebaseDriver import FirebaseDriver
import random
from twilio.rest import Client
import datetime


class CreatorService:
    def __init__(self):
        self.__driver = FirebaseDriver()
        self.__creator = Creator()

    def update_to_creator(self, email):
        creators = self.__driver.find_by_parameter("user", {"email": email})
        if not creators:
            return False
        creator = creators[0]
        # set creator to true in firebase
        if self.__driver.update_document("user", creator["doc_id"], {"creator": True}):
            return {"success": True, "message": "Creator Portal Unlocked Successfully"}
        else:
            return {"success": False}
    
    def get_all_creators(self):
        # get users with the role creator set to true
        return self.__driver.find_by_parameter("user", {"creatr": True})
    
    def send_otp(self, phone):
        account_sid = "ACbd96a0cd59a5ac3fcd2b40cf0a785304"
        auth_token = "1649fba76f6a6ec9a40c1ff6a3ed6de8"
        otp = ''.join(random.choices('0123456789', k=6))
        client = Client(account_sid, auth_token)
        from_whatsapp_number = 'whatsapp:+14155238886'
        to_whatsapp_number = 'whatsapp:'+phone
        message = 'Your OTP CODE : ' + otp

        self.__driver.create_document("creator_validation_otps", {"phone": phone, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "otp": otp})

        # Send message
        message = client.messages.create(
                                    body=message,
                                    from_=from_whatsapp_number,
                                    to=to_whatsapp_number
                                )
        return True
            
    def check_otp(self, phone, otp):
        numbers = self.__driver.find_by_parameter("creator_validation_otps", {"phone": phone})
        if not numbers:
            return {"success": False, "message": "Phone Number changed or not found"}
        if numbers[0]["otp"] == otp:
            return {"success": True, "message": "OTP validated successfully"}


    def add_request(self, email, type, link, business_email, description):
        #find user by email, add this info there, and set a flag for request as pending
        user = self.__driver.find_by_parameter("user", {"email": email})
        print(email)
        if not user:
            return {"success": False, "message": "User not found"}
        user = user[0]
        user["request"] = {"type": type, "link": link, "business_email": business_email, "description": description, "status": "pending"}
        if self.__driver.update_document("user", user.to_dict()):
            return {"success": True, "message": "Request added successfully"}
        else:
            return {"success": False, "message": "Request failed to add"}

