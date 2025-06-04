from rest_framework import generics, permissions
from .models import User
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.response import Response
from .solana_client import SolanaAPI

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class TransactionListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        wallet = request.user.solana_wallet
        if not wallet:
            return Response({"error": "Wallet not linked"}, status=400)

        solana = SolanaAPI()
        txs = solana.get_transactions(wallet)
        return Response(txs)