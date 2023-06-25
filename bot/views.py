from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from bot.models import TgUser
from bot.serializers import TgUserSerializer
from bot.tg.client import TgClient


class VerificationView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TgUserSerializer
    model = TgUser

    def patch(self, request: Request, *args, **kwargs) -> Response:
        serializer: TgUserSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tg_user: TgUser = serializer.validated_data['tg_user']
        tg_user.user = self.request.user
        tg_user.save(update_fields=['user'])
        instance_serializer: TgUserSerializer = self.get_serializer(tg_user)

        TgClient().send_message(tg_user.telegram_chat_id, 'Bot token verified')

        return Response(instance_serializer.data)


        # serializer = TgUserSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # tg_user: TgUser = serializer.save(user=request.user)
        #
        # TgClient().send_message(tg_user.telegram_chat_id, 'Bot token verified')
        #
        # return Response(serializer.data)
