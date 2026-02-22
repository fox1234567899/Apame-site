from .models import Item,Cart,CartItem,Transaction,Order,OrderItem
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from .serializers import ItemSerializer
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import DetailSerializer,CartItemSerializer,CartSerializer,NumCartItemsSerializer,UserSerializer,RegisterSerializer,UploadPicture
from django.dispatch import receiver
from decimal import Decimal
import uuid 
import requests
from django.conf import settings
from rest_framework import status



BASE_URL = "http://localhost:5173"

def get_or_create_cart(request):
    cart=None
   
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user).first()
        if not cart:
            cart= Cart.objects.create(user=request.user)
    
        
                    
    else:
        
        if not request.session.session_key:
            request.session.create()
        cart=Cart.objects.filter(session_id=request.session.session_key).first()
        if not cart:
            cart=Cart.objects.create(session_id=request.session.session_key,)
    return cart
            



@api_view(["GET"])
def itemView(request):
    items = Item.objects.all()
    serializer= ItemSerializer(items,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def detail_item_view(request,slug):
    item = Item.objects.get(slug=slug)
    serializer= DetailSerializer(item)
    return Response(serializer.data)


@api_view(['POST'])
def add_item(request):
    try:
        item_id = request.data.get("item_id")
        cart=get_or_create_cart(request)
        
        item = Item.objects.get(id=item_id)


        cartitem,created = CartItem.objects.get_or_create(cart=cart, item=item)
        cartitem.quantity =1
        cartitem.save()
        serializer = CartItemSerializer(cartitem)
        return Response({"data":serializer.data,"message":"Cart item created successfully"},status=200)
    except Exception as e: 
        return Response({"error":str(e)}, status=400)
    

@api_view(['GET'])
def item_in_cart(request):
    item_id = request.query_params.get("item_id")
    cart = get_or_create_cart(request)
        
    item = Item.objects.get(id=item_id)

    item_exists_in_cart = CartItem.objects.filter(cart=cart , item=item).exists()
    return Response({"item_in_cart":item_exists_in_cart})


@api_view(['GET'])
def get_cart_stat(request):
    cart = get_or_create_cart(request)

   
    serializer = NumCartItemsSerializer(cart)
    return Response(serializer.data)



@api_view(['GET'])
def get_cart(request):


    cart = get_or_create_cart(request)
        
    serializer = CartSerializer(cart)
    return Response(serializer.data)
    


@api_view(['PATCH'])
def update_quantity(request):
    try:
        cartitem_id = request.data.get("item_id")
        quantity= request.data.get("quantity")
        quantity = int(quantity)
        cartitem = CartItem.objects.get(id=cartitem_id)
        cartitem.quantity = quantity 
        cartitem.save()
        serializer = CartItemSerializer(cartitem)
        return Response({"data":serializer.data,"message":"cartitem updated successfully!"})
    except Exception as e:
        return Response({'error':str(e)}, status=400)
    


@api_view(['POST'])
def delete_CartItem(request):
    cartitem_id= request.data.get('item_id')
    cartitem = CartItem.objects.get(id=cartitem_id)
    cartitem.delete()
    return Response({"message":"Item successfully deleted from your cart"},status=status.HTTP_204_NO_CONTENT)





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_information(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_username(request):
    user = request.user
    return Response({"username": user.username})




@api_view(['GET'])
def search(request):
    query=request.GET.get('q', '')
    items = Item.objects.filter(name__istartswith=query)
    serializer= ItemSerializer(items, many=True)
    return Response(serializer.data) 


@api_view(['POST'])
def registerPart(request):
    serializer=RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user= serializer.save()
        return Response({'message':'the account made successfully','user':{'id':user.id,'email':user.email,'username':user.username}},status=status.HTTP_201_CREATED)
    

    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def changeProfilePicture(request):
    serializer=UploadPicture(request.user,data=request.data,partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



def get_or_create_cart_for_user(user):
    cart=Cart.objects.filter(user=user).first()
    if not cart:
        cart=Cart.objects.create(user=user)
    return cart



@api_view(['POST'])
def token_login(request):
    username=request.data.get('username')
    password=request.data.get('password')
    user = authenticate(username=username,password=password)
    if not user:
        return Response({"error":"Invalid Credentials"},status=400)
    
    guest_cart=None
    if request.session.session_key:
        guest_cart=Cart.objects.filter(session_id=request.session.session_key,user__isnull=True).first()
    user_cart=get_or_create_cart_for_user(user)

    if guest_cart:
        with transaction.atomic():
            for i in guest_cart.things.all():
                cartitem,created=CartItem.objects.get_or_create(cart=user_cart,item=i.item)
                cartitem.quantity=(
                    i.quantity if created
                    else cartitem.quantity + i.quantity)
                cartitem.save()
            guest_cart.delete()
    refresh=RefreshToken.for_user(user)
    user_data = UserSerializer(user).data
    return Response({
        "access": str(refresh.access_token),
        "refresh":str(refresh),
        'user':str(user_data)
    })
               

    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apame_payment(request):
    if request.user.is_authenticated:
        try:
            user=request.user

            tx_ref = str(uuid.uuid4())
            cart = Cart.objects.get(user=user)
            amount = sum([item.quantity * item.item.price for item in cart.things.all()])
            order=Order.objects.create(user=user,status="pending")
            for cartitem in cart.things.all():
                OrderItem.objects.create(
                    order=order,
                    item=cartitem.item,
                    quantity=cartitem.quantity,
                    price=cartitem.item.price
                )
            tax= Decimal("4.00")
            shipping=Decimal("10.00")
            total_amount=amount + tax + shipping
            currency= "USD"
            redirect_url= f"{BASE_URL}/payment-status/"
            phone = str(user.phone) if user.phone else ""
            phone = phone.replace("+", "").replace(" ","")
            transaction = Transaction.objects.create(
                ref=tx_ref,
                order=order,
                amount= total_amount,
                currency = currency,
                user=user,
                status='pending'
            )

            flutterwave_payload = {
                "tx_ref" : tx_ref,
                'amount': int(total_amount),
                'currency':currency,
                'redirect_url':redirect_url,
                'customer':{
                    'email':user.email,
                    'phonenumber':phone,
                    
                    'name':user.username,
                },
                'customizations':{
                    'title':'Apame Payment'
                }
            }

            headers = {
                "Authorization":f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}",
                "Content-Type":'application/json'
            }


            response =requests.post(
                'https://api.flutterwave.com/v3/payments',
                json = flutterwave_payload,
                headers=headers

            )

            if response.status_code == 200:
                return Response(response.json(),status=status.HTTP_200_OK)
            else:
                return Response(response.json(),status=response.status_code)
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['POST'])
def payment_callback(request):
    status= request.GET.get('status')
    tx_ref = request.GET.get('tx_ref')
    transaction_id = request.GET.get('transaction_id')


    user= request.user 


    if status == 'successful':
        headers = {
            'Authorization': f'Bearer {settings.FLUTTERWAVE_SECRET_KEY}'
        }
        response = requests.get(f'https://api.flutterwave.com/v3/transactions/{transaction_id}/verify', headers = headers)
        response_data = response.json() 

        if response_data['status'] == 'success':
            transaction = Transaction.objects.get(ref=tx_ref)
            if(response_data['data']['status'] == 'successful'
            and float(response_data['data']['amount']) == float(transaction.amount)
            and response_data['data']['currency'] == transaction.currency):
               transaction.status = 'completed'
               transaction.save()

               order = transaction.order 
               order.status = 'completed'
               order.save()
               Cart.objects.filter(user=order.user).delete()
               return Response({'message': 'Payment successful', 'subMessage':'you have made payment successfully'}, status=200)
            else:
                return Response({'message': 'Payment Verification failed', 'subMessage':'Your payment verification failed'}, status =400)
        else:
            return Response({'message': 'failed to verify transaction with Flutterwave', 'subMessage':'we could not verify transaction with flutterwave'}, status =400)
    else:
        return Response({'message': 'Payment was not successful', },status=400)

               
               
               
