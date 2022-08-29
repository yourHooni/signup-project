import logging
import random

from django.db.models import Q

from rest_framework import generics, viewsets, mixins, status
from drf_yasg.utils import swagger_auto_schema

from .models import PhoneCertification, PhoneCertificationLog
from .serializers import PhoneCertificationSerializer, CheckCertificationCodeSerializer
from core.utils.response_format import base_api_response

logger = logging.getLogger('certification')


# Create your views here.
class PhoneCertificationViewSet(generics.GenericAPIView):
    """
       휴대폰 인증 API

       ---
       휴대폰 인증 테이블과 입력된 개인 정보를 비교하여 매치가 되면 인증 로그 테이블에 인증 코드 생성 및 row 생성,
       존재하지 않으면 인증 실패 에러 출력

       ---
       # Request Param
           - name : 이름
           - mobile_carrier_code : 통신사 코드
           - phone_number : 휴대폰 번호
           - date_of_birth : 생년월일
           - gender : 성별

       # Response Param
           - result: 성공 여부
           - message: 내용
           - data: 인증 코드 로그 아이디
    """
    serializer_class = PhoneCertificationSerializer

    @swagger_auto_schema(tags=['전화번호 인증'])
    def post(self, request, *args, **kwargs):
        try:
            try:
                name = request.data["user_name"]
                mobile_carrier_code = request.data["mobile_carrier_code"]
                phone_number = request.data["phone_number"]
                date_of_birth = request.data["date_of_birth"]
                gender = request.data["gender"]
            except Exception as request_e:
                request_e_str = request_e.__str__()
                logger.error(request_e_str)
                return base_api_response(False, status.HTTP_400_BAD_REQUEST, message=request_e_str)

            query = Q(user_name=name) & Q(mobile_carrier_code=mobile_carrier_code) & Q(phone_number=phone_number) \
                & Q(date_of_birth=date_of_birth) & Q(gender=gender)
            try:
                certification = PhoneCertification.objects.get(query)
            except Exception as exist_e:
                exist_e_str = exist_e.__str__()
                logger.error(exist_e_str)
                return base_api_response(False, status.HTTP_401_UNAUTHORIZED, message="account does not exist")

            try:
                code_list = []
                for i in range(10):
                    code_list.append(str(i))

                log = PhoneCertificationLog(
                    phone_certification_id=certification,
                    code=''.join(random.sample(code_list, 6))
                )
                log.save()
            except Exception as func_e:
                func_e_str = func_e.__str__()
                logger.error(func_e_str)
                return base_api_response(False, status.HTTP_400_BAD_REQUEST, message=func_e_str)

            return base_api_response(True, status.HTTP_200_OK, data=log.id)

        except Exception as e:
            e_str = e.__str__()
            logger.error(e_str)
            return base_api_response(False, status.HTTP_500_INTERNAL_SERVER_ERROR)


class CheckCertificationCodeViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    """
       인증 코드 체크 API

       ---
        로그의 인증 코드와 입력된 인증 코드를 비교하여 같으면 인증여부에 True로 수정, 틀릴시에 에러 출력

       ---
       # Request Param
           - id : 인증 로그 아이디
           - code : 인증 코드

       # Response Param
           - result: 성공 여부
           - message: 내용
           - data: 인증 코드 로그 아이디
    """
    serializer_class = CheckCertificationCodeSerializer

    @swagger_auto_schema(tags=['전화번호 인증'])
    def partial_update(self, request, *args, **kwargs):
        try:
            try:
                log_id = request.data["id"]
                code = request.data["code"]
            except Exception as request_e:
                request_e_str = request_e.__str__()
                logger.error(request_e_str)
                return base_api_response(False, status.HTTP_400_BAD_REQUEST, message=request_e_str)

            try:
                log = PhoneCertificationLog.objects.filter(id=log_id).latest('updated_at')
                if log.code != str(code):
                    raise Exception
            except Exception as exist_e:
                exist_e_str = exist_e.__str__()
                logger.error(exist_e_str)
                return base_api_response(False, status.HTTP_400_BAD_REQUEST)

            try:
                log.is_certificated = True
                log.save()
            except Exception as func_e:
                func_e_str = func_e.__str__()
                logger.error(func_e_str)
                return base_api_response(False, status.HTTP_400_BAD_REQUEST, message=func_e_str)

            return base_api_response(True, status.HTTP_200_OK, data=log.id)

        except Exception as e:
            e_str = e.__str__()
            logger.error(e_str)
            return base_api_response(False, status.HTTP_500_INTERNAL_SERVER_ERROR)
