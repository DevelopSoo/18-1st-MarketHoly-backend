import json
import jwt
import bcrypt

from my_settings import SECRET_KEY

from django.views import View
from django.http  import JsonResponse

from user.models import User

class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email    = data['email']
            password = data['password']

            user = User.objects.get(email=email)

            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                access_token = jwt.encode({'user_id':user.id}, SECRET_KEY, algorithm='HS256')
                return JsonResponse({'message':'SUCCESS', 'access_token':access_token}, status=200)
            
            return JsonResponse({'message':'아이디 또는 비밀번호 오류입니다.'}, status = 400)

        except KeyError:
            return JsonResponse({'message':'회원정보를 입력하세요.'}, status=400)
        
        except json.decoder.JSONDecodeError:
            return JsonResponse({'message':'회원정보를 입력하세요.'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message':'존재하지 않는 사용자입니다.'}, status=404)