from drf_yasg import openapi

from ..utils.response import *

# manual_parameters: page
pageManualParameters = [
    openapi.Parameter(
        name='page',
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_INTEGER,
        description='分頁號碼',
    ),
    openapi.Parameter(
        name='page_size',
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_INTEGER,
        description='每頁顯示的數據項目數量',
    ),
]