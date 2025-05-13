from rest_framework.authentication import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User, Comment
from .serializer import UserSerializer, CommentSerializer


@api_view(["POST"])
def signup(request):
    serialize_data = UserSerializer(data=request.data)

    if serialize_data.is_valid():
        serialize_data.save()

        return Response({"data": {"message": "successful registration", "code": 201}})
    return Response({"error": {"message": serialize_data.errors, "code": 403}})


@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if email is None or password is None:
        return Response({"error": {"message": "Validation error", "code": 422}})

    user = authenticate(email=email, password=password)

    if not user:
        return Response({"error": {"message": "authentication failed", "code": 401}})

    token, _ = Token.objects.get_or_create(user=user)

    return Response({"data": {"user_token": token.key, "code": 200}})


@api_view(["POST"])
def post_comment(request, pk):
    if not request.user.is_active:
        return Response({"error": "forbidden for you", "code": "403"})

    try:
        recipient = User.objects.get(pk=pk)
    except:
        return Response({"error": "user not found", "code": 404})

    serialize_data = CommentSerializer(data=request.data)

    if serialize_data.is_valid():
        comment = serialize_data.save()
        print("!!!!!", recipient)

        return Response({"data": {"message": "comment has been added", "code": 201}})
    return Response({"error": serialize_data.errors, "code": 403})


@api_view(["PATCH"])
def transfer_coins(request):
    try:
        sender = User.objects.get(pk=request.data.get("sender_id"))
        recipient = User.objects.get(pk=request.data.get("recipient_id"))

    except:
        return Response({"error": "user not found", "code": 404})

    transfer_summ = request.data.get("transfer_summ")

    if not transfer_summ or transfer_summ > sender.balance:
        return Response({"error": "incorrect value", "code": 400})

    new_sender_balance = sender.balance - transfer_summ
    sender.balance = new_sender_balance
    sender.save()

    new_recipient_balance = recipient.balance + transfer_summ
    recipient.balance = new_recipient_balance
    recipient.save()

    return Response({"data": "successful transfer", "code": 200})


@api_view(["GET"])
def get_user_data(request, pk):
    user = User.objects.get(pk=pk)
    serialize_data = UserSerializer(user)
    data = {
        "email": serialize_data.data["email"],
        "fio": serialize_data.data["fio"],
        "balance": serialize_data.data["balance"]
    }

    if request.user != user:
        return Response({"error": "forbidden for you", "code": 403})

    return Response({"data": data, "code": 200})


@api_view(["GET"])
def get_user_names(request):
    names = User.objects.all()
    serialize_data = UserSerializer(names, many=True)
    data = []

    for i in serialize_data.data:
        data.append(i["fio"])

    return Response({"data": data, "code": 200})
