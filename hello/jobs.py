from django.http import HttpResponse
from json import dumps
import uuid

import ml.podr

from .forms import UploadFileForm

class Job:
    def __init__(self, id):
        self.id = str(id)

    def to_json(self):
        return dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


# Create your views here.
def index(request):
    #  create a job id
    jobid = uuid.uuid4()
    job = Job(jobid)
    # Earlier there was print(ml.podr.runpx)
    ml.podr.runpx(jobid)
    # return the response with the job id
    # fire off a back ground process for the processing
    response = HttpResponse(job.to_json())
    response['Content-Type'] = 'application/json'
    return response

def upload_view(request):
    if request.method == 'POST':
        form = FileUploadForm

def simple_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

