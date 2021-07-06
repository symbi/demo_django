from django.db.models import Q
from django.http import Http404,HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import Poster, PosterSerializer, Comment, CommentSerializer, Test, TestSerializer, Team, TeamSerializer


from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import os, time

# Create your views here.

@api_view(['DELETE'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def profileDel(request,filename):
    print("enter profileDel")
    print('profileDel request:',request)
    print("profileDel filename:",filename)
    #print("MEDIA_URL in settings:",settings.MEDIA_URL)
    print("CKEDITOR_UPLOAD_PATH in settings:",settings.CKEDITOR_UPLOAD_PATH+filename)
    file_path=settings.CKEDITOR_UPLOAD_PATH+filename
    if os.path.isfile(file_path):
        os.remove(file_path)
        return Response({'removefile':filename}, status=status.HTTP_200_OK)
    return Response({'removefile':filename}, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
def profile(request):
    print("enter profile")
    if request.method == 'POST':
        #print('enter request.body:',request.body)
        print('enter request:',request)
        print('enter request time:',str(time.time()))
        print('enter request.POST:',request.POST)
        print('request.FILES:',request.FILES)
        print('request.FILES upload:',request.FILES['upload'])
  

        #path = "media/uploads/images/"
        
        f = request.FILES["upload"]
        file_path = settings.CKEDITOR_UPLOAD_PATH + '_' +str(time.time())+'_'+f.name
        print("new file name:",file_path)
        des_origin_f = open(file_path, "wb+")  
        for chunk in f.chunks():
            des_origin_f.write(chunk)
        des_origin_f.close()
        
        return HttpResponse('{ "uploaded": true, "url": "http://127.0.0.1:8000/'+file_path+'"}')
        

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


# vote_type could be 'upvote' or 'cancel_vote'
def updateVote(user, target, target_type, action):
    
    if target_type=='poster':
        upvoted_targets = user.upvoted_posts
    if target_type=='comment':
        upvoted_targets = user.upvoted_comments


    upvoted_targets.remove(target)


    #upvote or cancel
    if action == 'upvote':
        upvoted_targets.add(target)

    target.update_points()
    return target.points


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

@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
def postersListView(request):
    print("posterList user:",request.user)
    print("current_user.is_authenticated:",request.user.is_authenticated)   
    # #last 30days?
    posters = Poster.objects.all()
    serializer = PosterSerializer(posters, many=True)

    for p in serializer.data:
        p['upvoted'] = False
        p['self_post'] = False 
        if not request.user.is_authenticated:
            pass
        elif request.user.upvoted_posts.filter(id=p['id']).count() > 0:
            p['upvoted'] = True  
        elif request.user== p['user']:
            p['self_post'] = True 

        for c in p['comments']:
            c['upvoted'] = False
            c['self_post'] = False 
            if not request.user.is_authenticated:
                pass
            elif request.user.upvoted_comments.filter(id=c['id']).count() > 0:
                c['upvoted'] = True
            elif request.user== c['user']:
                c['self_post'] = True             

    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def voteView(request, id):
    current_user = request.user
    if not current_user.is_authenticated:
        return Response('Not logged in', status=status.HTTP_401_UNAUTHORIZED) 
    # if current_user== target.user:
    #     pass
    #comment vote or post vote

    target_type = request.data.get('vote_type', '')
    target = None
    if target_type=='poster':#todo if not found return msg
        target = Poster.objects.get(pk=id)
    if target_type=='comment':
        target = Comment.objects.get(pk=id)
    
    if target==None:
        return Response('item no more exist', status=status.HTTP_204_NO_CONTENT) 
    action = request.data.get('action', '')
    print('action:',action)

    points = updateVote(current_user, target, target_type, action)

    return Response({'action': action, 'points': points})






# @api_view(['GET'])
# @authentication_classes([authentication.TokenAuthentication])
# def posterView(request, id):
#     print("posterView user:",request.user)



class postersList_del(APIView):

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


