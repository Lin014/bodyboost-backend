from drf_yasg import openapi

from ..serializers import MemberSerializer
from ..utils.response import *

# responses: getMemberByUserId
getMemberByUserIdResponses = {
    200: MemberSerializer,
    404: str(NotFoundResponse('Member'))
}

# request_body: updateMember
updateMemberRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'member_type': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='會員類型，normal, premium'
        ),
        'phone': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='會員手機號碼'
        ),
        'is_trial': openapi.Schema(
            type=openapi.TYPE_BOOLEAN,
            description='會員是否試用過'
        ),
        'payment_type': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='會員付款類型，month(月繳), year(年繳)'
        ),
    }
)
# responses: updateMember
updateMemberResponses = {
    200: MemberSerializer,
    404: str(NotFoundResponse('Member'))
}