from django.http import JsonResponse

def health_check(request):
    data = {
        'status':'ok'
    }
    return JsonResponse(data)