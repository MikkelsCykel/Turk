# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.exceptions import SuspiciousOperation
from django.views.decorators.csrf import ensure_csrf_cookie
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.price import Price
from infrastructure import infrastructure
import json

AMAZON_ENDPOINT = 'https://workersandbox.mturk.com/mturk/externalSubmit'

@ensure_csrf_cookie
def index(request):
    assignment_Id = request.GET.get('assignmentId', '')
    worker_id = request.GET.get('workerId', '')
    hit_Id = request.GET.get('hitId', '')
    infra = infrastructure()
    hid = ''
    if assignment_Id == 'ASSIGNMENT_ID_NOT_AVAILABLE':
        set_img = infra.select_rnd_preview_images(20)
    elif assignment_Id == '': 
        set_img = infra.select_rnd_preview_images(20)
    else:
        hid = infra.prepare_hit(hit_Id, assignment_Id, worker_id)
        set_img = infra.select_rnd_images(worker_id, 5, 15)


    view_data = {
        'worker_id': worker_id,
        'assignment_id': assignment_Id,
        'amazon_host': AMAZON_ENDPOINT,
        'hit_id': hit_Id,
        'hid': hid,
        'set_img': set_img
    }
    response = render_to_response('index.html', view_data)
    response['x-frame-options'] = 'ALLOWALL'
    return response

def submit_hit_partial(request):
    if request.method == 'POST':
        assignment_Id = request.POST['assignmentId']
        worker_id = request.POST['workerId']
        hit_Id = request.POST['hitId']
        hid = request.POST['hid']
        imgid = request.POST['imageId']
        appealing = request.POST['appealing']
        course = request.POST['course']
        free = request.POST['free']
        if hid:
            infra = infrastructure()
            infra.insert_hit_response(hid, imgid, appealing, course, free)   
    return HttpResponse('Ok')

