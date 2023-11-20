from drf_yasg import openapi

from ..serializers import StoreSerializer
from ..utils.response import *

# responses: getAllStore
getAllStoreResponses = {
    200: StoreSerializer,
    404: str(NotFoundResponse('Store'))
}

# request_body: addStore
addStoreRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='商店名稱'
        )
    }
)
# responses: addStore
addStoreResponses = {
    200: StoreSerializer,
    400: '{ "message": "Store already exists.", "store": StoreObject }'
}

# request_body: updateStore
updateStoreRequestBody = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='商店名稱'
        ),
    }
)
# responses: updateStore
updateStoreResponses = {
    200: StoreSerializer,
    404: str(NotFoundResponse('Store'))
}

# responses: deleteStore
deleteStoreResponses = {
    200: '{ "message": "Store deleted successfully." }',
    404: str(NotFoundResponse('Store'))
}
