from django.urls import path, include
from .views import (
    GetAllProductsAPIView,
    AddProductAPIView,
    ProductsAPIsView,

    GetAllSuppliersAPIView,
    AddSupplierAPIView,
    SuppliersAPIsView,

    GetAllCustomersAPIView,
    AddCustomerAPIView,
    CustomersAPIsView,

    BuyProductAPIView,
    GetAllOrdersAPIView,
    ClearOrdersData,
    GetAllOrderDetailsAPIView,
    ClearOrderDetailsData
)
# from .Views import (
#     products_views,
#     customers_views,
#     suppliers_views
# )

urlpatterns = [
    # products views
    path('products/get-all', GetAllProductsAPIView.as_view()),
    path('product/add', AddProductAPIView.as_view()),
    path('product/<str:product_id>', ProductsAPIsView.as_view()),

    # suppliers views
    path('suppliers/get-all', GetAllSuppliersAPIView.as_view()),
    path('supplier/add', AddSupplierAPIView.as_view()),
    path('supplier/<str:supplier_id>', SuppliersAPIsView.as_view()),

    # customers views
    path('customers/get-all', GetAllCustomersAPIView.as_view()),
    path('customer/add', AddCustomerAPIView.as_view()),
    path('customer/<str:customer_id>', CustomersAPIsView.as_view()),

    # orders views
    path('orders/get-all', GetAllOrdersAPIView.as_view()),
    path('orders/delete-all', ClearOrdersData.as_view()),

    # order details views
    path('order-details/get-all', GetAllOrderDetailsAPIView.as_view()),
    path('order-details/delete-all', ClearOrderDetailsData.as_view()),

    # actions
    path('actions/buy', BuyProductAPIView.as_view()),

    # orders views
    # path('api/add_student', AddStudentAPIView.as_view()),
    # path('api/<str:student_id>', StudentAPIsView.as_view()),
]