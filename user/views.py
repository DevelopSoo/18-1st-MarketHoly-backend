import json, re, bcrypt
from json.decoder import JSONDecodeError

from django.views import View 
from django.http  import JsonResponse

from user.models import User, Address


# 문제점
# 1. email과 같은 key 값이 2개 이상 들어올 때는??
# 2. 이벤트 SNS, 메시지 수신 여부
class SignUpView(View):
    def post(self, request):    
        try:
            data = json.loads(request.body)
            
            # 회원 개인 정보
            email         = data["email"]
            password      = data["password"]
            password2     = data["password2"]
            name          = data["name"]
            phone_number  = data["phone_number"]
            date_of_birth = data.get("date_of_birth") # null True

            # 주소 관련 정보
            zip_code       = data["zip_code"]
            address        = data["address"]
            detail_address = data.get("detail_address") # null True

            # 이메일 정규식 검사
            regex_for_email = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

            if not email:
                return JsonResponse({"message": "이메일을 입력해주세요."}, status=400)

            if not regex_for_email.match(email):
                return JsonResponse({"message": "이메일 형식이 적절하지 않습니다."}, status=400)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({"message": "이미 존재하는 이메일입니다."}, status=400)
            
            # 비밀번호 검사
            if not password:
                return JsonResponse({"message": "비밀번호를 입력해주세요."}, status=400)

            if password != password2:
                return JsonResponse({"message": "비밀번호가 일치하지 않습니다."}, status=400)

            if len(password) < 10:
                return JsonResponse({"message": "비밀번호 길이는 10자 이상으로 해주세요."}, status=400)

            # 비밀번호 암호화
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_hashed_pw = hashed_password.decode('utf-8') 
            
            if not name:
                return JsonResponse({"message": "이름을 입력해주세요."}, status=400)
            
            if not phone_number:
                return JsonResponse({"message": "휴대폰 번호를 입력해주세요."}, status=400) 
            
            if not zip_code and not address:
                return JsonResponse({"message": "주소를 입력해주세요."}, status=400) 
        
            # 전화 번호 정규식 찾아보기 
            # regex_for_phone_number = re.compile('\d{9}')
            
            User.objects.create(email=email, 
                                password=decoded_hashed_pw, 
                                name=name, 
                                phone_number=phone_number, 
                                date_of_birth=date_of_birth)
            
            user = User.objects.get(email=email)

            Address.objects.create(user=user,
                                   zip_code=zip_code, 
                                   address=address, 
                                   detail_address=detail_address)
                

            return JsonResponse({"message": "Sign Up SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "필요한 값이 누락되었거나 key값이 잘못 입력되었습니다."}, status=500)

        except JSONDecodeError:
            return JsonResponse({"message": "아무 정보도 보내지 않았습니다."}, status=500)


