from django.shortcuts import render
from django.conf import settings
from datetime import time, datetime
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'index/index.html')

@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        output_file = 'F:/pycode/env_python3.6.5/homepage/downloadcsv_sql.txt'
        filewriter = open(output_file, 'a+', newline=None)
        callback = request.GET.get('CKEditorFuncNum')
        try:
            path = settings.CKEDITOR_UPLOAD_PATH + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f = request.FILES.get("upload", None)
            # f = request.FILES["upload"]
            file_name = path + "/" + f.name
            des_origin_f = open(file_name, "wb+")
            for chunk in f.chunks():
                des_origin_f.write(chunk)
            des_origin_f.close()
            filewriter.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + file_name + "\n")
        except Exception as e:
            print(e)
        # res = r"<script>window.parent.CKEDITOR.tools.callFunction(" + callback + ",'/" + file_name + "', '');</script>"
        filewriter.close()
        return HttpResponse(None)
    else:
        raise Http404()
