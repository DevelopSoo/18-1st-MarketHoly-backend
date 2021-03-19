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