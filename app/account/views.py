import logging

from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q

from rest_framework import generics, viewsets, mixins, status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema

from .serializers import AccountSerializer, LoginAccountSerializer, \
    MobileCarrierSerializer, ResetPasswordSerializer
from .models import Account, MobileCarrier
from certification.models import PhoneCertificationLog
from core.utils.response_format import base_api_response
from core.utils.validate import check_validate

logger = logging.getLogger('account')


class SignUpView(generics.GenericAPIView):
    """
       회원가입 API

       ---
        * 전화번호 인증 후에 사용
       ---
        1. 전화번호 인증이 되었는지 체크
        2. 입력된 email, password에 대해 검증
        3. nick_name, email, phone_number에 대해 계정이 존재하는지 체크
        4. password 암호화
        5. mobile_carrier_code로 통신사 모델 조회
        6. 계정 생성
        7. 전화번호 인증 로그 삭제
       ---
       # Request Param
           - log_id : 전화번호 인증 로그 아이디
           - name : 이름
           - nick_name : 닉네임
           - email : 이메일 (이메일 형식)
           - password : 비밀번호 (8자 이상, 숫자+영문)
           - mobile_carrier_code : 통신사 코드
           - phone_number : 휴대폰 번호
           - date_of_birth : 생년월일
           - gender : 성별

       # Response Param
           - result: 성공 여부
           - message: 내용
           - data: 사용자 닉네임
    """
    serializer_class = AccountSerializer

    @swagger_auto_schema(tags=['계정'])
    def post(self, request, *args, **kwargs):
        try:
            try:
                log_id = request.data["log_id"]
                name = request.data["name"]
                nick_name = request.data["nick_name"]
                email = request.data["email"]
                password = request.data["password"]
                mobile_carrier_code = request.data["mobile_carrier_code"]
                phone_number = request.data["phone_number"]
                date_of_birth = request.data["date_of_birth"]
                gender = request.data["gender"]

                # check phone number certification
                try:
                    log = PhoneCertificationLog.objects.get(id=log_id)
                    if not log.is_certificated:
                        raise Exception
                except Exception as log_e:
                    log_e_str = log_e.__str__()
                    logger.error(log_e_str)
                    return base_api_response(False, status.HTTP_400_BAD_REQUEST, message="not authenticated")

                # check validate
                if check_validate("email", email) is False:
                    return base_api_response(False, status.HTTP_400_BAD_REQUEST, message="email is not valid")
                if check_validate("password", password) is False:
                    return base_api_response(False, status.HTTP_400_BAD_REQUEST, message="password is not valid")

                # check unique fields
                if Account.objects.filter(nick_name=nick_name).exists():
                    return base_api_response(False, status.HTTP_400_BAD_REQUEST,
                                             message=f"nick name '{nick_name}' is already exist")
                if Account.objects.filter(email=email).exists():
                    return base_api_response(False, status.HTTP_400_BAD_REQUEST,
                                             message=f"email '{email}' is already exist")
                if Account.objects.filter(phone_number=phone_number).exists():
                    return base_api_response(False, status.HTTP_400_BAD_REQUEST,
                                             message=f"phone_number '{phone_number}' is already exist")

                # encryption password
                password = make_password(password)

                # get mobile_carrier model
                mobile_carrier = MobileCarrier.objects.get(code=mobile_carrier_code)
                if mobile_carrier is None:
                    return base_api_response(False, status.HTTP_400_BAD_REQUEST,
                                             message="mobile carrier code is not valid")

            except Exception as request_e:
                request_e_str = request_e.__str__()
                logger.error(request_e_str)
                return base_api_response(False, status.HTTP_400_BAD_REQUEST, message=request_e_str)

            # save account
            try:
                account = Account(
                    name=name,
                    nick_name=nick_name,
                    email=email,
                    password=password,
                    mobile_carrier_code=mobile_carrier,
                    phone_number=phone_number,
                    date_of_birth=date_of_birth,
                    gender=gender
                )
                account.save()
            except Exception as func_e:
                func_e_str = func_e.__str__()
                logger.error(func_e_str)
                return base_api_response(False, status.HTTP_400_BAD_REQUEST, message=func_e_str)

            # delete phone certification log
            log.delete()

            return base_api_response(True, status.HTTP_201_CREATED, data=str(account))

        except Exception as e:
            e_str = e.__str__()
            logger.error(e_str)
            return base_api_response(False, status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(generics.GenericAPIView):
    """
       로그인 API

       ---
        1. id(email 또는 phone_number), password를 가진 계정 검색
        2. jwt 토큰 생성
       ---
       # Request Param
           - id : 아이디 (email or phone_number)
           - password : 비밀번호

       # Response Param
           - result: 성공 여부
           - message: 내용
           - data
               ㄴ token : 로그인 토큰
               ㄴ user : 사용자 닉네임
    """
    serializer_class = LoginAccountSerializer

    @swagger_auto_schema(tags=['계정'])
    def post(self, request, *args, **kwargs):
        try:
            try:
                id = request.data["id"]
                password = request.data["password"]
            except Exception as request_e:
                request_e_str = request_e.__str__()
                logger.error(request_e_str)
                return base_api_response(False, status.HTTP_400_BAD_REQUEST, message=request_e_str)

            # 계정 검색
            try:
                account = Account.objects.get(Q(email=id) | Q(phone_number=id))
                if not check_password(password, account.password):
                    return base_api_response(False, status.HTTP_401_UNAUTHORIZED, message="password incorrect")
            except Exception as exist_e:
                exist_e_str = exist_e.__str__()
                logger.error(exist_e_str)
                return base_api_response(False, status.HTTP_401_UNAUTHORIZED, message="account does not exist")

            # 토큰 발급
            token = TokenObtainPairSerializer.get_token(account)
            refresh_token = str(token)
            access_token = str(token.access_token)

            return base_api_response(
                True,
                status.HTTP_200_OK,
                data={
                    "token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token
                    },
                    "user": str(account)
                }
            )
        except Exception as e:
            e_str = e.__str__()
            logger.error(e_str)
            return base_api_response(False, status.HTTP_500_BAD_REQUEST)


class AccountView(generics.GenericAPIView):
    """
       유저 정보 조회 API

       ---
        * 로그인 후에 사용
       ---
        1. 유효한 토큰인지 조회
        2. 토큰에서 user_id 추출
        3. user_id에 해당하는 id를 가진 user 정보 추출

       ---
       # HEAD
           - HTTP_AUTHORIZATION : 유저 access 토큰

       # Response Param
           - name : 이름
           - nick_name : 닉네임
           - email : 이메일
           - mobile_carrier_code : 통신사 코드
           - phone_number : 휴대폰 번호
           - date_of_birth : 생년월일
           - gender : 성별
    """
    serializer_class = AccountSerializer
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(tags=['계정'])
    def get(self, request):
        try:
            # get token
            token = request.META.get("HTTP_AUTHORIZATION")
            access_token_obj = AccessToken(token)

            # token에서 user_id 추출
            user_id = access_token_obj['user_id']

            # 계정 검색
            account = Account.objects.get(id=user_id)
            serializer = AccountSerializer(account)
            return base_api_response(True, status.HTTP_200_OK, data=serializer.data)
        except Exception as e:
            e_str = e.__str__()
            logger.error(e_str)
            return base_api_response(False, status.HTTP_401_UNAUTHORIZED)


class ResetPasswordView(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    """
       비밀번호 변경 API

       ---
        * 전화번호 인증 후에 사용
       ---
        1. phone number에 대해 계정 검색
        2. 입력된 password에 대해 검증
        3. log_id에 대하 인증 로그 조회 및 인증여부 검증, 인증 로그가 없거나 인증이 되지 않았을 경우 return Error
        4. password 암호화
        5. 계정에 대해 password 변경
        6. 전화번호 인증 로그 삭제
       ---
       # Request Param
           - log_id : 전화번호 인증 로그 아이디
           - phone_number : 전화 번호
           - new_password : 변경할 비밀번호 (8자 이상, 숫자+영문)

       # Response Param
           - result: 성공 여부
           - message: 내용
           - data: 사용자 닉네임
    """
    serializer_class = ResetPasswordSerializer

    @swagger_auto_schema(tags=['계정'])
    def partial_update(self, request, *args, **kwargs):
        try:
            try:
                phone_number = request.data["phone_number"]
                log_id = request.data["log_id"]
                new_password = request.data["new_password"]
            except Exception as request_e:
                request_e_str = request_e.__str__()
                logger.error(request_e_str)
                return base_api_response(False, status.HTTP_400_BAD_REQUEST, message=request_e_str)

            # 계정 검색
            try:
                account = Account.objects.get(phone_number=phone_number)
            except Exception as exist_e:
                exist_e_str = exist_e.__str__()
                logger.error(exist_e_str)
                return base_api_response(False, status.HTTP_401_UNAUTHORIZED, message="account does not exist")

            # 비밀번호 검증
            if check_validate("password", new_password) is False:
                return base_api_response(False, status.HTTP_400_BAD_REQUEST, message="password is not valid")

            try:
                # 인증 로그 조회
                log = PhoneCertificationLog.objects.filter(id=log_id).latest('updated_at')

                # 인증 검증
                if not log.is_certificated:
                    raise Exception
            except Exception as exist_e:
                exist_e_str = exist_e.__str__()
                logger.error(exist_e_str)
                return base_api_response(False, status.HTTP_401_UNAUTHORIZED, message="not authenticated")

            # 비밀번호 암호화
            new_password = make_password(new_password)

            # 비밀번호 변경
            account.password = new_password
            account.save()

            # 인증 로그 삭제
            log.delete()

            return base_api_response(True, status.HTTP_200_OK, data=str(account))
        except Exception as e:
            e_str = e.__str__()
            logger.error(e_str)
            return base_api_response(False, status.HTTP_500_INTERNAL_SERVER_ERROR)


class RetrieveMobileCarrierView(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
       통신사 조회 API

       ---
        1. ModelCarrier 조회

       ---
       # Response Param
           - result: 성공 여부
           - message: 내용
           - data: 통신사 리스트
                   ㄴ code : 통신사 고유 코드
                   ㄴ user : 통신사 명
    """
    queryset = MobileCarrier.objects.all()
    serializer_class = MobileCarrierSerializer

    def get_queryset(self):
        """Return objects for the mobile carrier"""
        return self.queryset.filter().order_by('-created_at')

    @method_decorator(name='list', decorator=swagger_auto_schema(tags=['통신사']))
    def list(self, request):
        serializer = MobileCarrierSerializer(self.get_queryset(), many=True)
        return base_api_response(True, status.HTTP_200_OK, data=serializer.data)
