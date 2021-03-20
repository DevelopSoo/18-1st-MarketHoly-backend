import json, re, bcrypt, jwt
from json.decoder import JSONDecodeError

from django.views            import View 
from django.http             import JsonResponse
from django.db               import transaction
from django.core.exceptions  import ValidationError

from user.models import User, Address
from my_settings import SECRET_KEY


# 문제점
# 1. email과 같은 key 값이 2개 이상 들어올 때는??
# 2. 이벤트 SNS, 메시지 수신 여부
class SignUpView(View):
    @transaction.atomic
    def post(self, request):    
        try:
            data = json.loads(request.body)
            
            # 회원 개인 정보
            email         = data["email"]
            password      = data["password"]
            name          = data["name"]
            phone_number  = data["phone_number"]
            date_of_birth = data.get("date_of_birth") # null True

            # 주소 관련 정보
            zip_code       = data["zip_code"]
            address        = data["address"]
            detail_address = data.get("detail_address") # null True

            # 이메일 정규식 검사
            regex_for_email = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

            
            signup_fail_response = JsonResponse({"message": "Bad Request"}, status=400)

            if not email:
                return signup_fail_response

            if not regex_for_email.match(email):
                return signup_fail_response
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({"message": "Conflict"}, status=409)
            
            # 비밀번호 검사
            if not password:
                return signup_fail_response

            if len(password) < 10:
                return signup_fail_response

            # 비밀번호 암호화
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_hashed_pw = hashed_password.decode('utf-8') 
            
            if not name:
                return signup_fail_response
            
            if not phone_number:
                return signup_fail_response
            
            if not zip_code and not address:
                return signup_fail_response
        
            # 전화 번호 정규식 찾아보기 
            # regex_for_phone_number = re.compile('\d{9}')
            
            user = User.objects.create(email=email, 
                                        password=decoded_hashed_pw, 
                                        name=name, 
                                        phone_number=phone_number, 
                                        date_of_birth=date_of_birth)

            Address.objects.create(user=user,
                                   zip_code=zip_code, 
                                   address=address, 
                                   detail_address=detail_address)
                

            return JsonResponse({"message": "Sign Up SUCCESS"}, status=200)

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

