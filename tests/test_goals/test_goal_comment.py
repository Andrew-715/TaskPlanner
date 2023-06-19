import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.fields import DateTimeField

from goals.models import BoardParticipant, GoalComment
from tests.test_goals.factories import CreateGoalCommentRequest


@pytest.mark.django_db()
class TestRetrieveGoalComment:
    @pytest.fixture(autouse=True)
    def setup(self, goal_comment, board_participant, user) -> None:
        board_participant.user = user
        board_participant.save()
        self.url = self.get_url(goal_comment)

    @staticmethod
    def get_url(comment: GoalComment) -> str:
        return reverse('comment_detail', kwargs={'pk': comment.pk})

    def test_auth_required(self, client):
        response = client.get(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_comment_not_participant(self, auth_client):
        BoardParticipant.objects.all().delete()

        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_another_user_comment(self, auth_client, another_user, goal_comment_factory, goal):
        comment = goal_comment_factory.create(goal=goal, user=another_user)

        response = auth_client.get(self.get_url(comment))

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == _serialize_response(comment, with_user=True)


def _serialize_response(goal_comment: GoalComment, **kwargs) -> dict:
    data = {
        'id': goal_comment.id,
        'user': goal_comment.user.id,
        'created': DateTimeField().to_representation(goal_comment.created),
        'updated': DateTimeField().to_representation(goal_comment.updated),
        'text': goal_comment.text,
        'goal': goal_comment.goal.id
    }

    return data | kwargs
