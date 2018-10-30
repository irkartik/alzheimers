# from django.shortcuts import render

# # Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from .models import Person
from django.core.files.base import ContentFile

import face_recognition
import numpy as np
import json
import base64
from tempfile import TemporaryFile
import string
import random

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


@csrf_exempt
def addPerson(request):
	if request.method == "POST":
		name = request.POST.get('name')
		lives_in = request.POST.get('lives_in')
		contact = request.POST.get('contact')
		age = request.POST.get('age')
		place_of_meeting = request.POST.get('place_of_meeting')
		relation = request.POST.get('relation')
		notes = request.POST.get('notes')
		image = base64.b64decode(request.POST.get('image'))


		try:
			temp = Person.objects.create(name = name, lives_in = lives_in, contact = contact, age = age, place_of_meeting = place_of_meeting, relation = relation, notes = notes, image = image)
			filename = id_generator()
			temp.image.save(filename + '.png', ContentFile(image))
			print(type(ContentFile(image)))

			target_image_path = temp.image.path
			target_image = face_recognition.load_image_file(target_image_path)
			try:
				encoded_target = face_recognition.face_encodings(target_image)[0]
			except Exception as e:
				print('No Face Detected')
				temp.delete()
				return HttpResponse(json.dumps({'status': 'No Face Detected'}))
			temp.save()
		except Exception as e:
			response = dict()
			response['status'] = 'ERROR'
			response['message'] = e
			return HttpResponse(json.dumps(response))

		msg = 'Successfully added ' + temp.name
		return HttpResponse(json.dumps({'status': msg}))

@csrf_exempt
def comparePerson(request):
	from django.core.files.uploadedfile import InMemoryUploadedFile
	from io import BytesIO

	data = base64.b64decode(request.POST.get('image'))
	print('data type ', type(data))
	buf = BytesIO(data)
	buf.seek(0, 2)
	filename = id_generator()
	image = InMemoryUploadedFile(buf, "image", filename + ".png", None, buf.tell(), None)
	
	image_input = face_recognition.load_image_file(image)
	encoded_input = face_recognition.face_encodings(image_input)[0]

	matched = []

	for person in Person.objects.all():
		target_image_path = person.image.path
		target_image = face_recognition.load_image_file(target_image_path)
		encoded_target = face_recognition.face_encodings(target_image)[0]

		dic = {}

		result = face_recognition.compare_faces([encoded_target], encoded_input)
		if result[0]:
			dic['name'] = person.name
			dic['lives_in'] = person.lives_in
			dic['contact'] = person.contact
			dic['age'] = person.age
			dic['place_of_meeting'] = person.place_of_meeting
			dic['relation'] = person.relation
			dic['notes'] = person.notes
			dic['image_url'] = person.image.url
			matched.append(dic)		
		final = dict()
		if len(matched) > 0:
			final['status'] = 'matched'
			final['person'] = matched
		else:
			final['status'] = 'not found'
	return HttpResponse(json.dumps(final))

def getAll(request):
	final = dict()
	matched = list()
	for person in Person.objects.all():
		dic = {}
		dic['name'] = person.name
		dic['lives_in'] = person.lives_in
		dic['contact'] = person.contact
		dic['age'] = person.age
		dic['place_of_meeting'] = person.place_of_meeting
		dic['relation'] = person.relation
		dic['notes'] = person.notes
		dic['image_url'] = person.image.url

		matched.append(dic)
	if len(matched) > 0:
		final['status'] = 'Found'
		final['children'] = matched
	else:
		final['status'] = 'Not Found'
	return HttpResponse(json.dumps(final))

