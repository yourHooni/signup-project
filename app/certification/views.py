import logging
import random
from datetime import datetime

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
       1. 입력된 개인 정보와 일치하는 인증 정보 조회, 없을 경우에 return error
       2. 인증 정보에 대한 인증 로그가 존재하는지 검색, 삭제
       2. 인증 코드 생성
       3. 인증 로그 생성

       ---
       # Request Param
           - user_name : 이름
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
    def post(self, request):
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

            # 전화번호 인증 조회
            query = Q(user_name=name) & Q(mobile_carrier_code=mobile_carrier_code) & Q(phone_number=phone_number) \
                & Q(date_of_birth=date_of_birth) & Q(gender=gender)
            try:
                certification = PhoneCertification.objects.get(query)
            except Exception as exist_e:
                exist_e_str = exist_e.__str__()
                logger.error(exist_e_str)
                return base_api_response(False, status.HTTP_401_UNAUTHORIZED, message="account does not exist")

            try:
                # 인증 코드 존재 여부 체크
                PhoneCertificationLog.objects.filter(phone_certification_id=certification).delete()
            except Exception as func_e:
                func_e_str = func_e.__str__()
                logger.error(func_e_str)
                return base_api_response(False, status.HTTP_400_BAD_REQUEST, message=func_e_str)

            try:
                # 인증 코드 생성
                code_list = []
                for i in range(10):
                    code_list.append(str(i))

                # 인증 로그 생성
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
        * 휴대폰 인증 후에 사용
       ---
        1. 전달받은 log_id에 대한 인증 로그 조회
        2. 인증 코드와 전달받은 코드가 동일한지 검증, 동일하지 않으면 return error
        3. 인증 여부 체크 (인증 완료)

       ---
       # Request Param
           - log_id : 인증 로그 아이디
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
                log_id = request.data["log_id"]
                code = request.data["code"]
            except Exception as request_e:
                request_e_str = request_e.__str__()
                logger.error(request_e_str)
                return base_api_response(False, status.HTTP_400_BAD_REQUEST, message=request_e_str)

            try:
                # 인증 로그 조회
                log = PhoneCertificationLog.objects.filter(id=log_id).latest('updated_at')
                # 인증 코드 검증
                if log.code != str(code):
                    raise Exception
            except Exception as exist_e:
                exist_e_str = exist_e.__str__()
                logger.error(exist_e_str)
                return base_api_response(False, status.HTTP_400_BAD_REQUEST)

            try:
                # 인증 여부 체크
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
