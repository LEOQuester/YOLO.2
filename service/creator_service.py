from data.creator import Creator

from data.boost import Boost

from repo.FirebaseDriver import FirebaseDriver
import random

from twilio.rest import Client
from datetime import datetime


class CreatorService:

    def __init__(self):

        self.__driver = FirebaseDriver()

        self.__creator = Creator()


    def get_all_creators(self):

        # get users with the role creator set to true

        return self.__driver.find_by_parameter("users", {"creator": True})
    

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


    def get_pending_requests(self):

        # get users with the request flag set to pending

        pendings = self.__driver.find_by_parameter("boosts", {"status": "pending"})

        print(pendings)

        return pendings
            

    def check_otp(self, phone, otp):

        numbers = self.__driver.find_by_parameter("creator_validation_otps", {"phone": phone})
        if not numbers:

            return {"success": False, "message": "Phone Number changed or not found"}

        if numbers[0]["otp"] == otp:

            return {"success": True, "message": "OTP validated successfully"}



    def signup_for_creator(self, email, type, link, business_email, description):

        #find user by email, add this info there, and set a flag for request as pending

        user = self.__driver.find_by_parameter("users", {"email": email})

        print(email, user)
        if not user:

            return {"success": False, "message": "User not found"}

        user = user[0]

        print(user)

        if self.__driver.update_document("users", user["doc_id"], {"type": type, "link": link, "business_email": business_email, "description": description, "role": "creator"}):

            return {"success": True, "message": "Request added successfully"}
        else:

            return {"success": False, "message": "Request failed to add"}


    def place_boost_request(self, email, title, link, keywords):

        # add a new document to the boost collection with the request flag set to pending

        new_boost = Boost()
        new_boost.email = email
        new_boost.title = title
        new_boost.content_url = link
        new_boost.keywords = keywords
        new_boost.status = "pending"

        new_boost.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(new_boost.to_dict())

        self.__driver.create_document("boosts", new_boost.to_dict())

        return {"success": True, "message": "Request added successfully"}, 200


    def approve_boost(doc_id):
            
        # update the status of the boost request to approved
        return self.__driver.update_document("boosts", doc_id, {"status": "approved"})

    def reject_boost(doc_id):
                
            # update the status of the boost request to rejected
            return self.__driver.update_document("boosts", doc_id, {"status": "rejected"})
