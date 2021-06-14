from django.db.models import Q
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import Poster, PosterSerializer, Comment, CommentSerializer, Test, TestSerializer, Team, TeamSerializer

def save_serializer(serializer):
    if serializer.is_valid():
        print("---is_valid----:",serializer)
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            print('save error:',serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    print('not valid:',serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def newCommentView(request):
    print("newCommentView user:",request.user.id)
    print("newCommentView request.data:",request.data)
    #p_body = request.data.get('body', '')
    post_data=request.data
    post_data['user']=request.user


    #p_poster_id=2
    #print("newCommentView data:",post_data)

    #poster_instance = Poster.objects.filter(id=p_poster_id).first()
    #post_data['poster']=poster_instance
    #serializer = CommentSerializer(data=post_data)
    comment=Comment(poster_id=request.data.get('poster_id', ''),
                    user_id=request.user.id,
                    body=request.data.get('body', ''))
    comment.save()
    serializer = CommentSerializer(comment)
            #toe return serializer
    return Response(serializer.data, status=status.HTTP_201_CREATED)           
    # print("poster_instance:",poster_instance)
    # serializer = CommentSerializer(data=post_data)
    # print("comment seriazer:",serializer)
    # return save_serializer(serializer)


    # if serializer.is_valid():
    #     print("---is_valid----") 
    #     serializer.save()   
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def newPostView(request):
    print("newPostView user:",request.user)
    #p_body = request.data.get('body', '')
    post_data=request.data
    post_data['user']=request.user

    print("newPostView data:",post_data)

    serializer = PosterSerializer(data=post_data)

    if serializer.is_valid():
        print("---is_valid----")
        try:
            serializer.save()
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
        posters = Poster.objects.all()
        serializer = PosterSerializer(posters, many=True)

        return Response(serializer.data)

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


