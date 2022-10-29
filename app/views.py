from email import message
from functools import total_ordering
from locale import currency
from django.shortcuts import render
from django.http import HttpResponse
from .serializers import *
# Create your views here.
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db.models import Sum


class Trade(APIView):
    def post(self, request):
        try:
            tradetype = request.data['tradetype']
            quantity = request.data['quantity']
            ordertype = request.data['ordertype']
            id = request.data['id']
            user = User.objects.get(id=id)

            if (tradetype == 'sell'):
                if (ordertype == 'limit'):
                    price = request.data['price']
                    if (user.stocks < quantity):
                        return Response({'message': 'insufficient stocks'}, status=400)
                    else:
                        user.stocks -= quantity
                        user.save()
                        limitorder = LimitOrder.objects.create(
                            type=tradetype, user=user, quantity=quantity, price=price)
                        limitorder.save()
                        return Response({'message': 'order placed'})
                else:
                    if (user.stocks < quantity):
                        return Response({'message': 'insufficient stocks'}, status=400)
                    else:
                        limitbuyers = LimitOrder.objects.filter(
                            type='buy').order_by('price', 'time')
                        total_buy_quantity = limitbuyers.aggregate(Sum('quantity'))[
                            'quantity__sum']
                        if (limitbuyers.count() == 0):
                            return Response({'message': 'order cannot be placed'}, status=400)
                        elif (total_buy_quantity < quantity):
                            for x in limitbuyers:
                                user.fiat += x.price*x.quantity
                                x.user.stocks += x.quantity
                                transaction = TradeHistory.objects.create(
                                    type='sell', quantity=x.quantity, price=x.price, user1=x.user, user2=user)
                                transaction.save()
                                cmp = CurrentMarketPrice.objects.create(
                                    price=x.price, quantity=x.quantity)
                                cmp.save()
                                x.user.save()
                                x.delete()
                            user.stocks -= total_buy_quantity
                            user.save()
                            return Response({'message': 'order partially filled'})
                        else:
                            total_quantity = quantity
                            for x in limitbuyers:
                                if (x.quantity < quantity):
                                    user.fiat += x.price*x.quantity
                                    x.user.stocks += x.quantity
                                    transaction = TradeHistory.objects.create(
                                        type='sell', quantity=x.quantity, price=x.price, user1=x.user, user2=user)
                                    transaction.save()
                                    cmp = CurrentMarketPrice.objects.create(
                                        price=x.price, quantity=x.quantity)
                                    cmp.save()
                                    quantity -= x.quantity
                                    x.user.save()
                                    x.delete()
                                    if (quantity == 0):
                                        break
                                else:
                                    user.fiat += x.price*quantity
                                    x.user.stocks += quantity
                                    transaction = TradeHistory.objects.create(
                                        type='sell', quantity=quantity, price=x.price, user1=x.user, user2=user)
                                    transaction.save()
                                    cmp = CurrentMarketPrice.objects.create(
                                        price=x.price, quantity=quantity)
                                    cmp.save()
                                    x.user.save()
                                    x.quantity -= quantity
                                    x.save()
                                    break
                            user.stocks -= total_quantity
                            user.save()
                            return Response({'message': 'order filled'})

            else:
                limitsellers = LimitOrder.objects.filter(
                    type='sell').order_by('price', 'time')
                if (ordertype == 'limit'):
                    price = request.data['price']
                    if (user.fiat < price*quantity):
                        return Response({'message': 'insufficient funds'}, status=400)
                    else:
                        user.fiat -= price*quantity
                        user.save()
                        limitorder = LimitOrder.objects.create(
                            type=tradetype, user=user, quantity=quantity, price=price)
                        limitorder.save()
                        return Response({'message': 'order placed'})
                else:
                    limitsellers=LimitOrder.objects.filter(type='sell').order_by('-price','time')
                    if(ordertype=='limit'):
                        price = request.data['price']
                        if(user.fiat<price*quantity):
                            return Response({'message':'insufficient funds'})
                        else:
                            user.fiat-=price*quantity
                            user.save()
                            limitorder = LimitOrder.objects.create(type=tradetype, user=user, quantity=quantity, price=price)
                            limitorder.save()
                            return Response({'message':'order placed'})
                    else:
                        current_quantity = quantity
                        total_price = 0
                        for x in limitsellers:
                            if (x.quantity < current_quantity):
                                total_price += x.price*x.quantity
                                current_quantity -= x.quantity
                            else:
                                total_price += x.price*current_quantity
                                current_quantity = 0
                                break
                        if (user.fiat < total_price):
                            return Response({'message': 'insufficient funds'}, status=400)
                        else:
                            if (current_quantity > 0):
                                for x in limitsellers:
                                    x.user.fiat += x.price*x.quantity
                                    user.stocks += x.quantity
                                    user.fiat -= x.price*x.quantity
                                    x.user.save()
                                    user.save()
                                    x.delete()
                                    cmp = CurrentMarketPrice.objects.create(
                                        price=x.price, quantity=x.quantity)
                                    cmp.save()
                                    transaction_history = TradeHistory.objects.create(
                                        type='buy', quantity=x.quantity, price=x.price, user1=user, user2=x.user)
                                    transaction_history.save()
                                return Response({'message': 'order partially filled'})
                            else:
                                for x in limitsellers:
                                    if (x.quantity <= quantity):
                                        x.user.fiat += x.price*x.quantity
                                        user.stocks += x.quantity
                                        user.fiat -= x.price*x.quantity
                                        x.user.save()
                                        user.save()
                                        cmp = CurrentMarketPrice.objects.create(
                                            price=x.price, quantity=x.quantity)
                                        cmp.save()
                                        transaction_history = TradeHistory.objects.create(
                                            type='buy', quantity=x.quantity, price=x.price, user1=user, user2=x.user)
                                        transaction_history.save()
                                        quantity -= x.quantity
                                        x.delete()
                                        if (quantity == 0):
                                            break
                                    else:
                                        x.user.fiat += x.price*quantity
                                        user.stocks += quantity
                                        x.user.save()
                                        user.fiat -= x.price*quantity
                                        user.save()
                                        x.quantity -= quantity
                                        x.save()
                                        cmp = CurrentMarketPrice.objects.create(
                                            price=x.price, quantity=quantity)
                                        cmp.save()
                                        transaction_history = TradeHistory.objects.create(
                                            type='buy', quantity=quantity, price=x.price, user1=user, user2=x.user)
                                        transaction_history.save()
                                        break
                                return Response({'message': 'order filled'})
        except Exception as e:
            return Response({'message': str(e)}, status=400)


class LimitOrderViewSet(viewsets.ModelViewSet):
    queryset = LimitOrder.objects.all()
    serializer_class = LimitOrderSerializer

    # def create(self, request):
    #     serializer = LimitOrderSerializer(data=request.data)
    #     user = request.data['user']
    #     user
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors)

    def list(self, request):
        try:
            queryset = LimitOrder.objects.order_by('price', 'time')
            serializer = LimitOrderSerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': str(e)})

    def destroy(self, request, pk=None):
        try:
            queryset = LimitOrder.objects.all()
            order = get_object_or_404(queryset, pk=pk)
            order.delete()
            return Response({'message': 'Order Deleted'})
        except Exception as e:
            return Response({'message': str(e)})


class TradeHistoryViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            queryset = TradeHistory.objects.all().order_by('price', '-time')
            serializer = TradeHistorySerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': str(e)})


class CurrentMarketPriceViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            queryset = CurrentMarketPrice.objects.all()
            serializer = CurrentMarketPriceSerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': str(e)})


class UserViewSet(viewsets.ViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """

    def list(self, request):
        try:
            queryset = User.objects.all()
            serializer = UserSerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': str(e)})

    def create(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Exception as e:
            return Response({'message': str(e)})

    def retrieve(self, request, pk=None):
        try:
            queryset = User.objects.all()
            user = get_object_or_404(queryset, pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': str(e)})

    def update(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Exception as e:
            return Response({'message': str(e)})
    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass
