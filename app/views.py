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
        price = request.data['price']
        id = request.data['id']

        user = User.objects.get(id=id)

        if (ordertype == 'limit'):
            if tradetype == 'buy' and (user.fiat < price*quantity):
                return Response({'message': 'Insufficient funds'})
            if tradetype == 'sell' and (user.stocks < quantity):
                return Response({'message': 'Insufficient stocks'})
            if tradetype == 'buy':
                user.fiat = user.fiat - price*quantity
            if tradetype == 'sell':
                user.stocks = user.stocks - quantity
            # user.blocked_fiat = user.blocked_fiat + price*quantity

            order = LimitOrder.objects.create(
                type=tradetype, user=user, price=price, quantity=request.data['quantity'])
            order.save()
            serializer = LimitOrderSerializer(order)
            return Response(serializer.data)

        if ordertype == 'market' and tradetype == 'buy':
            searchtype = 'sell'

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
                current_market_price = []
                # obj = CurrentMarketPrice.objects.all().order_by('time')
                # current_market_price=0
                # if obj!=None:
                #     current_market_price=obj.first().price

                counter_limit = 0
                while current_quantity > 0:
                    order = Limit[counter_limit]
                    if order.quantity > current_quantity:
                        order.quantity -= current_quantity
                        # order.save()
                        ordersave.append(order)
                        current_price += order.price * quantity
                        tradehistory = TradeHistory.objects.create(type=tradetype,
                                                                   quantity=current_quantity, price=order.price, buyer=user, seller=order.user)
                        cmp = CurrentMarketPrice.objects.create(
                            price=order.price, quantity=current_quantity)
                        current_market_price.append(cmp)

                        # tradehistory.save()

                        current_quantity = 0
                        allhistory.append(tradehistory)
                        break
                    else:

                        current_quantity -= order.quantity
                        current_price += order.price * order.quantity

                        tradehistory = TradeHistory.objects.create(type=tradetype,
                                                                   quantity=order.quantity, price=order.price, buyer=user, seller=order.user)
                        # tradehistory.save()
                        allhistory.append(tradehistory)

                        cmp = CurrentMarketPrice.objects.create(
                            price=order.price, quantity=order.quantity)
                        current_market_price.append(cmp)

                        # order.delete()
                        orderdelete.append(order)
                        counter_limit += 1

                if (user.fiat >= current_price):

                    user.fiat -= current_price
                    user.stocks += quantity
                    for x in ordersave:
                        x.save()
                    for x in orderdelete:
                        x.delete()
                    for x in allhistory:
                        x.save()
                    for x in current_market_price:
                        x.save()

                    user.save()
                    return Response({'message': 'success'})
                else:
                    return Response({'message': 'insufficient funds'})

            else:
                return Response({'message': 'Buy orders Cant be fulfilled'})

        if ordertype == 'market' and tradetype == 'sell':
            if user.stocks < quantity:
                return Response({'message': 'insufficient stocks'})

            searchtype = 'buy'
            Limit = LimitOrder.objects.filter(
                type=searchtype).order_by('price', 'time')

            totalquantity = Limit.aggregate(Sum('quantity'))['quantity__sum']
            if (totalquantity == None):
                totalquantity = 0

            print(totalquantity)
            if quantity <= totalquantity:

                current_quantity = quantity
                current_price = 0
                # allhistory = []
                # orderdelete = []
                # ordersave = []

                counter_limit = 0
                while current_quantity > 0:
                    order = Limit[counter_limit]
                    if order.quantity > current_quantity:
                        order.quantity -= current_quantity
                        order.save()
                        current_price += order.price * quantity
                        tradehistory = TradeHistory.objects.create(
                            quantity=current_quantity, price=order.price, seller=user, buyer=order.user)
                        tradehistory.save()
                        cmp = CurrentMarketPrice.objects.create(type=tradetype,
                                                                price=order.price, quantity=current_quantity)
                        cmp.save()

                        current_quantity = 0
                        break
                    else:
                        current_quantity -= order.quantity
                        current_price += order.price * order.quantity
                        tradehistory = TradeHistory.objects.create(type=tradetype,
                                                                   quantity=order.quantity, price=order.price, seller=user, buyer=order.user)
                        tradehistory.save()
                        cmp = CurrentMarketPrice.objects.create(
                            price=order.price, quantity=order.quantity)
                        cmp.save()
                        order.delete()
                        counter_limit += 1

                user.fiat += current_price
                user.stocks -= quantity
                user.save()

            else:
                return Response({'message': 'Sell orders Cant be fulfilled'})

        return Response({'message': 'Hello, world!'})


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
        queryset = LimitOrder.objects.all()
        serializer = LimitOrderSerializer(queryset, many=True)
        return Response(serializer.data)


class TradeHistoryViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = TradeHistory.objects.all()
        serializer = TradeHistorySerializer(queryset, many=True)
        return Response(serializer.data)


class CurrentMarketPriceViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = CurrentMarketPrice.objects.all()
        serializer = CurrentMarketPriceSerializer(queryset, many=True)
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
