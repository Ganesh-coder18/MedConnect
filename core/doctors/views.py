from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

import random
from cryptography.fernet import Fernet

from .models import DoctorModel, DoctorProfileModel, DoctorVerificationModel

from core.emails import sendOTP

class EmailView(APIView):

    def post(self, request):
        email = request.data.get("email")
        try:
            isRegistered = DoctorModel.objects.get(email=email)
            print(isRegistered)
        except:
            doctor = DoctorModel.objects.create(email=email)
            DoctorProfileModel.objects.create(doctor=doctor)
        doctor = DoctorModel.objects.get(email=email)
        otp = random.randint(1000,9999)
        print(otp)
        # sendOTP(email,otp)
        doctor.otp = otp
        strKey = "YdgkXWwdxycqNAkJ-_9OfOtLaPCZW2DO0WGTazVKsYs="
        key = strKey.encode()
        fernet = Fernet(key)
        mix = email + str(otp)
        encrypted = fernet.encrypt(mix.encode())
        doctor.token = encrypted.decode()
        doctor.save()
        response = {
            "message": "OTP Sent Successfully"
        }
        return Response(response, status=status.HTTP_200_OK)

class VerifyEmailView(APIView):

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")
        doctor = DoctorModel.objects.get(email=email)
        try:
            doctor_verificaion = DoctorVerificationModel.objects.get(doctor=doctor)
            hasReq = doctor_verificaion.id
        except:
            hasReq = 0
        if doctor.otp != int(otp):
            response = {
                "message": "Incorrect OTP"
            }
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        response = {
            "email": email,
            "token": doctor.token,
            "verified": doctor.verified,
            "hasReq": hasReq
        }
        return Response(response, status=status.HTTP_200_OK)

class DoctorProfileView(APIView):

    def post(self, request):

        email = request.data.get("email")
        # token = request.data.get("token")
        # verify if user is legit
        try:
            doctor = DoctorModel.objects.get(email=email)
        except:
            return Response("Doctor Not Found", status=status.HTTP_404_NOT_FOUND)
        # if(doctor.token != token):
        #     return Response("Invalid Doctor Token", status=status.HTTP_404_NOT_FOUND)

        profile = DoctorProfileModel.objects.get(doctor=doctor)
        print("date",request.data.get("dob"))
        if request.data.get("first_name") is not None:
            first_name = request.data.get("first_name")
            profile.first_name = first_name
        if request.data.get("last_name") is not None:
            last_name = request.data.get("last_name")
            profile.last_name = last_name
        if request.data.get("video") is not None:
            video = request.data.get("video")
            profile.video = video
        if request.data.get("description") is not None:
            description = request.data.get("description")
            profile.description = description
        if request.data.get("title") is not None:
            title = request.data.get("title")
            profile.title = title
        if request.data.get("reg_no") is not None:
            reg_no = request.data.get("reg_no")
            profile.reg_no = reg_no
        if request.data.get("signature") is not None:
            signature = request.data.get("signature")
            profile.signature = signature
        if request.data.get("city") is not None:
            city = request.data.get("city")
            profile.city = city
        if request.data.get("state") is not None:
            state = request.data.get("state")
            profile.state = state
        if request.data.get("files") is not None:
            files = request.data.get("files")
            profile.files = files
        if request.data.get("specialization") is not None:
            specialization = request.data.get("specialization")
            profile.specialization = specialization
        if request.data.get("qualification") is not None:
            qualification = request.data.get("qualification")
            profile.qualification = qualification
        if request.data.get("dob") is not None:
            dob = request.data.get("dob")
            profile.dob = dob
        if request.data.get("gender") is not None:
            gender = request.data.get("gender")
            profile.gender = gender
        if request.data.get("photo") is not None:
            photo = request.data.get("photo")
            profile.photo = photo
        if request.data.get("phone") is not None:
            phone = request.data.get("phone")
            profile.phone = phone
        if request.data.get("address") is not None:
            address = request.data.get("address")
            profile.address = address
        if request.data.get("pincode") is not None:
            pincode = request.data.get("pincode")
            profile.pincode = pincode
        profile.save()
        request_verification = DoctorVerificationModel.objects.create(doctor=doctor)
        return Response("Created Profile", status=status.HTTP_201_CREATED)

class DoctorRequestVerificationView(APIView):

    def post(self, request):
        email = request.data.get("email")
        token = request.data.get("token")
        # verify if user is legit
        try:
            doctor = DoctorModel.objects.get(email=email)
        except:
            return Response("Doctor Not Found", status=status.HTTP_404_NOT_FOUND)
        if (doctor.token != token):
            return Response("Invalid Doctor", status=status.HTTP_404_NOT_FOUND)

        # check if already requested
        try:
            DoctorVerificationModel.objects.get(doctor=doctor)
            return Response("Already requested", status=status.HTTP_400_BAD_REQUEST)
        except:
            pass

        # create request for verification
        request_verification = DoctorVerificationModel.objects.create(doctor=doctor)

        return Response("Requested for Verification", status=status.HTTP_200_OK)

    def get(self, request):
        # doctor will see the remarks of verification.

        email = request.GET["email"]
        # token = request.GET["token"]
        # verify if user is legit
        try:
            doctor = DoctorModel.objects.get(email=email)
        except:
            return Response("Doctor Not Found", status=status.HTTP_404_NOT_FOUND)
        # if (doctor.token != token):
        #     return Response("Invalid Doctor", status=status.HTTP_404_NOT_FOUND)

        # check if already requested
        try:
            request_verification = DoctorVerificationModel.objects.get(doctor=doctor)
        except:
            return Response("No Request", status=status.HTTP_400_BAD_REQUEST)
        status_ = request_verification.status
        remarks = request_verification.remarks

        response = {
            "remarks": remarks,
            "status": status_
        }

        return Response(response, status=status.HTTP_200_OK)



