from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from tagger.forms import UploadFileForm
from . import utils
import json


# Create your views here.
def index(request):
	return render(request,'index.html',{})

@csrf_exempt
def post(request, *args, **kwargs):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        utils.handle_upload(request.FILES['qqfile'], form.cleaned_data)
        return utils.make_response(content=json.dumps({ 'success': True }))
    else:
        return utils.make_response(status=400,
            content=json.dumps({
                'success': False,
                'error': '%s' % repr(form.errors)
            }))

@csrf_exempt
def delete(request, *args, **kwargs):
    """A DELETE request. If found, deletes a file with the corresponding
    UUID from the server's filesystem.
    """
    qquuid = kwargs.get('qquuid', '')
    if qquuid:
        try:
            utils.handle_deleted_file(qquuid)
            return utils.make_response(content=json.dumps({ 'success': True }))
        except Exception as e:
            return utils.make_response(status=400,
                content=json.dumps({
                    'success': False,
                    'error': '%s' % repr(e)
                }))
    return utils.make_response(status=404,
        content=json.dumps({
            'success': False,
            'error': 'File not present'
        }))

