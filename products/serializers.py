from rest_framework import serializers 
from phonenumber_field.serializerfields import PhoneNumberField as DRFPhoneNumberField
from .models import Item,CartItem,Cart,OrderItem,Order
from django.contrib.auth import get_user_model
class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model=Item
        fields=['id','name','description','price','image','category','slug',]



class DetailSerializer(serializers.ModelSerializer):
    similar_items = serializers.SerializerMethodField()
    class Meta:
        model=Item 
        fields=["id","slug","description","price","image","name","similar_items"]
    
    def get_similar_items(self,item):
        items=Item.objects.filter(category=item.category).exclude(id=item.id)
        serializer= ItemSerializer(items,many=True)
        return serializer.data



class CartItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    total = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ["id","item","total","quantity"]
    def get_total(self,cartitem):
        price = cartitem.item.price * cartitem.quantity
        return price 


class CartSerializer(serializers.ModelSerializer):
    cartitems=CartItemSerializer(read_only=True , many=True, source='things')
    sum_total = serializers.SerializerMethodField()
    num_of_items= serializers.SerializerMethodField()

    class Meta:
        model= Cart
        fields = ["id","cartitems",'session_id','sum_total',"num_of_items","created_at","modified_at"]

    def get_sum_total(self,cart):
        cartitems = cart.things.all()
        total = sum([i.item.price * i.quantity for i in cartitems])
        return total
    
    def get_num_of_items(self,cart):
        cartitems = cart.things.all()
        total =sum([item.quantity for item in cartitems])
        return total






class NumCartItemsSerializer(serializers.ModelSerializer):
    num_of_items = serializers.SerializerMethodField()
    class Meta:
        model= Cart
        fields = ['id',"num_of_items"]
    
    def get_num_of_items(self,cart):
        num_of_items = sum([item.quantity for item in cart.things.all()])
        return num_of_items



class CartItemsUserSerializer(serializers.ModelSerializer):
    item= ItemSerializer(read_only=True)
    order_id= serializers.SerializerMethodField()
    order_date = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = ['id','item','quantity','order_id','order_date']


    def get_order_id(self,orderitem):
        order_id= orderitem.order.id
        return order_id
    


    def get_order_date(self,orderitem):
        order_date= orderitem.order.created_at
        return order_date
    


class UserSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    phone = DRFPhoneNumberField()
    class Meta:
        model= get_user_model()
        fields = ['id','username','first_name','last_name','city','phone','email','address','items','avatar']

    def get_items(self,user):
        orders = Order.objects.filter(user=user)
        orderItems=OrderItem.objects.filter(order__in=orders)
        serializer = CartItemsUserSerializer(orderItems, many=True)
        return serializer.data
    


class RegisterSerializer(serializers.ModelSerializer):
    password1=serializers.CharField(write_only=True,required=True,min_length=8)
    password2=serializers.CharField(write_only=True,required=True,min_length=8)
    class Meta:
        model=get_user_model()
        fields=['id','username','password1','password2' ,'first_name','last_name','city','phone','email','address',]
    

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError('passwords do not match')
        return attrs 
    

    def create(self, validated_data):
        password=validated_data.pop('password1')
        validated_data.pop('password2')
        

        user = get_user_model()(**validated_data)
        user.set_password(password)
        user.save()
        return user
    


class UploadPicture(serializers.ModelSerializer):
    class Meta:
        model=get_user_model()
        fields=['avatar']