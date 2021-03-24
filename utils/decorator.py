import jwt

from django.http import JsonResponse

from my_settings import SECRET_KEY

from user.models import User

def login_required(func):
    def wrapper(self, request, *arg, **kwargs):
        try:
            token   = request.headers.get('Authorization')
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            user = User.objects.get(id=payload['user_id'])
            
            if not user:
                return JsonResponse({'message': 'INVALID_USER'}, status=400)

            request.user = user

            return func(self, request, *arg, **kwargs)
        
        except KeyError:
            return JsonResponse({'message': 'TOKEN_DOES_NOT_EXIST'}, status=400)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'INVALID_TOKEN_TYPE'}, status=400)

        except jwt.exceptions.InvalidSignatureError:
            return JsonResponse({'message': 'SIGNATURE_VERIFICATION_FAILED'}, status=400)

    return wrapper
