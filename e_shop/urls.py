from django.urls import path, include
from e_shop.views import *
from django.contrib.auth import views as auth_views

from userauths.views import CustomPasswordResetForm


urlpatterns = [
    path("", index, name= "index"),
    path("products/", product_list_view, name= "product-list"),
    path("product/<pid>/", product_detail_view, name= "product-detail"),

    path("category/", category_list_view, name= "category-list"),
    path("category/<cid>/", category_product_list_view, name= "category-product-list"),
    
    path("vendors/", vendor_list_view, name= "vendor-list"),
    path("vendor/<vid>/", vendor_detail_view, name= "vendor-detail"),
    
    #tag
    path("products/tag/<slug:tag_slug>/", tag_list, name= "tags"),
    #add review
    path("add-review/<int:pid>/", ajax_add_review, name="add-review"),
    
    #search
    path("search/", search_view, name= "search"),
    #filter_products
    path("filter-products/", filter_product, name= "filter-product"),
    #add-to-cart
    path("add-to-cart/", add_to_cart, name="add-to-cart"),
    #cart_view
    path("cart/", cart_view, name="cart"),
    #delete product from cart
    path("delete-from-cart/", delete_product_from_cart, name="delete-from-cart"),
    path("update-cart/", update_cart, name="update-cart"),
    #checkout view
    path("checkout/", checkout_view, name="checkout"),
    #paypal
    #path("paypal/", include("paypal.standard.ipn.urls")),
    
    path("payment-completed/", payment_completed_view, name="payment-completed"),
    path("payment-failed/", payment_failed_view, name="payment-failed"),

    
    path("my-account/", user_account_view, name= "user-account"),
    path("contact/", contact, name= "contact"),
    path("deals/", deals, name= "deals"),

#bkash
    path('bkash/payment/create/', create_payment, name='bkash-create-payment'),
    path('bkash/payment/execute/', execute_payment, name='bkash-execute-payment'),
    path('bkash/payment/query/', query_payment, name='bkash-query-payment'),

    # Password reset views
    path('password-reset/', 
        auth_views.PasswordResetView.as_view(
            template_name='userauths/password_reset.html', 
            form_class=CustomPasswordResetForm
        ), 
        name='password_reset'
    ),
    path('password-reset/done/', 
        auth_views.PasswordResetDoneView.as_view(
            template_name='userauths/password_reset_done.html'
        ), 
        name='password_reset_done'
    ),
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            template_name='userauths/password_reset_confirm.html'
        ), 
        name='password_reset_confirm'
    ),
    path('reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(
            template_name='userauths/password_reset_complete.html'
        ), 
        name='password_reset_complete'
    ),


] 
