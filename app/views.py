from email import message
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
        ordertype = request.data['ordertype']
        tradetype = request.data['tradetype']
        quantity = request.data['quantity']
        id = request.data['id']

        user = User.objects.get(id=id)

        if (ordertype == 'limit'):
            order = LimitOrder.objects.create(
                type=tradetype, user=user, price=request.data['price'], quantity=request.data['quantity'])
            order.save()
            serializer = LimitOrderSerializer(order)
            return Response(serializer.data)

        if (ordertype == 'market'):
            searchtype = 'sell'
            if (tradetype == 'sell'):
                searchtype = 'buy'

            Limit = LimitOrder.objects.filter(
                type=searchtype).order_by('price', 'time')
            # print(Limit)
            totalquantity = Limit.aggregate(Sum('quantity'))['quantity__sum']
            if (totalquantity == None):
                totalquantity = 0
            print(totalquantity)
            if quantity <= totalquantity:

                current_quantity = quantity
                current_price = 0
                allhistory = []
                orderdelete = []
                ordersave = []

                while current_quantity > 0:
                    order = Limit[0]
                    if order.quantity >= current_quantity:
                        order.quantity -= current_quantity
                        # order.save()
                        ordersave.append(order)
                        current_price += order.price * quantity
                        current_quantity = 0
                        tradehistory = TradeHistory.objects.create(
                            quantity=current_quantity, price=order.price, buyer=user, seller=order.user)
                        # tradehistory.save()
                        allhistory.append(tradehistory)
                    else:
                        current_quantity -= order.quantity
                        current_price += order.price * order.quantity

                        tradehistory = TradeHistory.objects.create(
                            quantity=order.quantity, price=order.price, buyer=user, seller=order.user)
                        # tradehistory.save()
                        allhistory.append(tradehistory)

                        # order.delete()
                        orderdelete.append(order)

                        Limit = Limit[1:]

                if (user.fiat >= current_price):

                    user.fiat -= current_price
                    user.stocks += quantity
                    for x in ordersave:
                        x.save()
                    for x in orderdelete:
                        x.delete()
                    for x in allhistory:
                        x.save()

                    user.save()
                    return Response({'message': 'success'})
                else:
                    return Response({'message': 'insufficient funds'})

            else:
                return Response({'message': 'Buy orders Cant be fulfilled'})

        return Response({'message': 'Hello, world!'})


class LimitOrderViewSet(viewsets.ModelViewSet):
    queryset = LimitOrder.objects.all()
    serializer_class = LimitOrderSerializer

    def create(self, request):
        serializer = LimitOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def list(self, request):
        queryset = LimitOrder.objects.all()
        serializer = LimitOrderSerializer(queryset, many=True)
        return Response(serializer.data)


class TradeHistoryViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = TradeHistory.objects.all()
        serializer = TradeHistorySerializer(queryset, many=True)
        return Response(serializer.data)


class CurrentMarketOrderViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = CurrentMarketOrder.objects.all()
        serializer = CurrentMarketOrderSerializer(queryset, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass
