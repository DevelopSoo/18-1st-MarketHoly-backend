import json, re, bcrypt, jwt
from json.decoder import JSONDecodeError

from django.views            import View 
from django.http             import JsonResponse
from django.db               import transaction
from django.core.exceptions  import ValidationError

from utils.decorator import login_required
from user.models     import User, Address
from my_settings     import SECRET_KEY

MIN_PASSWORD_LENGTH = 10


class SignUpView(View):
    @transaction.atomic
    def post(self, request):    
        try:
            data = json.loads(request.body)
            
            email         = data["email"]
            password      = data["password"]
            name          = data["name"]
            phone_number  = data["phone_number"]
            date_of_birth = data.get("date_of_birth")


            zip_code       = data["zip_code"]
            address        = data["address"]
            detail_address = data.get("detail_address")


            regex_for_email = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')


            if not email or not regex_for_email.match(email):
                return JsonResponse({"message": "INVALID_EMAIL"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"message": "EMAIL_ALREADY_EXIST"}, status=409)
            

            if not password or len(password) < MIN_PASSWORD_LENGTH:
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=400)


            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_hashed_pw = hashed_password.decode('utf-8') 
            
            if not name or not phone_number:
                return JsonResponse({"message": "INVALID_USER_INFO"}, status=400)
            
            if not zip_code and not address:
                return JsonResponse({"message": "INVALID_ADDRESS"}, status=400)
        

            user = User.objects.create(email=email, 
                                        password=decoded_hashed_pw, 
                                        name=name, 
                                        phone_number=phone_number, 
                                        date_of_birth=date_of_birth)

            Address.objects.create(user=user,
                                   zip_code=zip_code, 
                                   address=address, 
                                   detail_address=detail_address)
                

            return JsonResponse({"message": "Sign Up SUCCESS","status": 200}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=500)

        except JSONDecodeError:
            return JsonResponse({"message": "JSONDecodeError"}, status=500)

        except ValidationError:
            return JsonResponse({"message": "INVALID_VALUE"}, status=400)


class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email    = data['email']
            password = data['password']

            exist_user = User.objects.filter(email=email).exists()
            if not exist_user:
                return JsonResponse({'message':'INVALID_USER'}, status = 400)
            
            user_info      = User.objects.get(email=email)
            check_password = bcrypt.checkpw(password.encode('utf-8'), user_info.password.encode('utf-8'))

            if not check_password:
                return JsonResponse({'message':'INVALID_USER'}, status = 400)

            access_token = jwt.encode({'user_id':user_info.id}, SECRET_KEY, algorithm='HS256')
            return JsonResponse({'message':'SUCCESS', 'access_token':access_token}, status=200)

        except KeyError:
            return JsonResponse({'message':'KeyError'}, status=400)
        
        except json.decoder.JSONDecodeError:
            return JsonResponse({'message':'JSONDecodeError'}, status=400)

class NameView(View):
    @login_required
    def get(self, request):
        user = request.user
        name = user.name
        return JsonResponse({'name': name}, status=200)
