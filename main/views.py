from django.db.models import Q
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import Poster, PosterSerializer, Test, TestSerializer, Team, TeamSerializer


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def newPostView(request):
    print("upload test!",request.user.id)
    p_body = request.data.get('body', '')
    serializer = PosterSerializer(data=request.data)

    if serializer.is_valid():

        try:
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            print('save error:',serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    print('not valid:',serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    #obj, created = foo.objects.get_or_create(field_name='unknown')
    # try:
    #     q = Poster(
    #         body=p_body,
    #         points=0,
    #         answers_count=0,
    #         user_id=request.user.id
    #     )
    #     q.save()
    # except Exception as e:
    #     print(e)
    #     raise Http404

    #return Response("test done", status=status.HTTP_201_CREATED)

class postersList(APIView):

    def get(self, request, format=None):
        print("posterList user:",request.user)
        # #last 30days?
        # posters = Poster.objects.all()
        # serializer = PosterSerializer(posters, many=True)
        # return Response(serializer.data)

class testsList(APIView):

    def get(self, request, format=None):
        print("testList user:",request.user)
        #last 30days?
        tests = Test.objects.all()
        serializer = TestSerializer(tests, many=True)

        print(serializer.data)
        return Response(serializer.data)


class teamsList(APIView):

    def get(self, request, format=None):
        print("teamsList user:",request.user)
        #last 30days?
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        print(serializer.data)
        return Response(serializer.data)


