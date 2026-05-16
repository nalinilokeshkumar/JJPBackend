from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Job
from .serializers import JobSerializer
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError


# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.exceptions import AuthenticationFailed

# def check_jwt(request):
#     auth = JWTAuthentication()

#     header = request.headers.get('Authorization')
#     if not header:
#         raise AuthenticationFailed("Token Required")

#     try:
#         raw_token = header.split()[1]
#     except:
#         raise AuthenticationFailed("Invalid Token Format")

#     auth.get_validated_token(raw_token)

#     return True


    
@csrf_exempt
@api_view(['POST'])
def add_job(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return Response({"msg": "Login Required"})

    data = request.data.copy()
    data['user'] = user_id
    data['isActive'] = True

    serializer = JobSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"msg": "Job Added"})
    return Response(serializer.errors)


@api_view(['GET'])
def get_jobs(request):
    jobs = Job.objects.all()
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_job(request, id):
    job = Job.objects.get(id=id)
    serializer = JobSerializer(job)
    return Response(serializer.data)

from django.shortcuts import get_object_or_404


@csrf_exempt
@api_view(['PUT'])
def update_job(request, id):
    job = Job.objects.get(id=id)

    user_id = request.session.get('user_id')

    if job.user.id != user_id:
        return Response({"msg": "Not Allowed"})

    data = request.data.copy()
    data['user'] = user_id

    serializer = JobSerializer(job, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"msg": "Updated"})
    return Response(serializer.errors)


@csrf_exempt
@api_view(['PATCH'])
def patch_job(request, id):
    job = Job.objects.get(id=id)

    user_id = request.session.get('user_id')

    if job.user.id != user_id:
        return Response({"msg": "Not Allowed"})

    serializer = JobSerializer(job, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"msg": "Patched"})
    return Response(serializer.errors)



@api_view(['DELETE'])
def delete_job(request, id):

    user_id = request.session.get('user_id')

    if not user_id:
        return Response({"msg": "Login Required"})

    job = get_object_or_404(Job, id=id)

    if job.user.id != user_id:
        return Response({"msg": "Not Allowed"})

    job.delete()

    return Response({"msg": "Deleted"})


# @api_view(['DELETE'])
# def delete_job(request, id):

#     user_id = request.session.get('user_id')
#     if not user_id:
#         return Response({"msg": "Login Required"})

#     try:
#         check_jwt(request)
#     except Exception as e:
#         return Response({"msg": str(e)})

#     job = get_object_or_404(Job, id=id)


#     if job.user.id != user_id:
#         return Response({"msg": "Not Allowed"})

#     job.delete()
#     return Response({"msg": "Deleted"})


from django.core.exceptions import ValidationError

def validate_image(file):
    if file:
        if not file.name.endswith(('.jpg','.jpeg','.png')):
            raise ValidationError("Only JPG, JPEG, PNG allowed")
        



from django.db.models import Q
from django.db.models.functions import Lower, Replace
from rest_framework.decorators import api_view
from rest_framework.response import Response
import re



@api_view(['GET'])
def search_jobs(request):

    query = request.GET.get('q')

    if not query:
        return Response({"msg": "Search query required"})

 
    keywords = query.lower().split()

    jobs = Job.objects.filter(isActive=True)

    final_query = Q()

    for word in keywords:

        q = Q()

        q |= Q(title__icontains=word)
        q |= Q(desc__icontains=word)
        q |= Q(company_location__icontains=word)
        q |= Q(job_type__icontains=word)
        q |= Q(hr_name__icontains=word)
        q |= Q(hr_email__icontains=word)
        q |= Q(hr_mobile__icontains=word)
        q |= Q(company_website__icontains=word)
        q |= Q(salary__icontains=word)

     
        q |= Q(user__username__icontains=word)

   
        if re.match(r'^\d+(\.\d+)?$', word):
            num = float(word)

            q |= Q(experience=num)

            try:
                q |= Q(vacancy=int(num))
            except:
                pass

    
        if word in ['fresher', '0']:
            q |= Q(experience=0)

        final_query &= q   

    jobs = jobs.filter(final_query).distinct()

    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)