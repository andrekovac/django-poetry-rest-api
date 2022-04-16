from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Show
from .serializers import ShowSerializer


class ShowListView(APIView):
    # `_request` is not used. The leading underscore expresses that it won't be used.
    def get(self, _request):
        shows = Show.objects.all()
        serialized_shows = ShowSerializer(shows, many=True)
        return Response(serialized_shows.data)
