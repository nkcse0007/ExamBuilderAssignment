from flask import Flask, Blueprint, request, jsonify
from src.ExamBuilder.controller.exam import Exam
from src.ExamBuilder.controller.sub_category import SubCategory
from src.ExamBuilder.controller.subject import Subject
from src.ExamBuilder.controller.topic import Topic
import os

url = os.environ.get('URL')
exam_app = Blueprint('exam_app', __name__, template_folder='templates')


@exam_app.route('/exam', methods=['GET', 'POST'])
@exam_app.route('/exam/<exam_id>', methods=['GET', 'PUT', 'DELETE'])
def exam(exam_id=None):
    obj = Exam(request, exam_id)

    if request.method == 'GET':
        response, status = obj.get()
        return jsonify(response), status

    if request.method == 'POST':
        response, status = obj.post()
        return jsonify(response), status

    if request.method == 'PUT':
        response, status = obj.put()
        return jsonify(response), status

    if request.method == 'DELETE':
        response, status = obj.delete()
        return jsonify(response), status


@exam_app.route('/exam/<exam_id>/sub-category', methods=['GET', 'POST'])
@exam_app.route('/exam/<exam_id>/sub-category/<subcategory_id>', methods=['GET', 'PUT', 'DELETE'])
def subcategory(exam_id, subcategory_id=None):
    if not exam_id or type(exam_id) is not str:
        return {'message': 'exam_id is required', 'data': {}, 'status': False}, 400

    obj = SubCategory(request, exam_id, subcategory_id)

    if request.method == 'GET':
        response, status = obj.get()
        return jsonify(response), status

    if request.method == 'POST':
        response, status = obj.post()
        return jsonify(response), status

    if request.method == 'PUT':
        response, status = obj.put()
        return jsonify(response), status

    if request.method == 'DELETE':
        response, status = obj.delete()
        return jsonify(response), status


@exam_app.route('/exam/<exam_id>/subject', methods=['GET', 'POST'])
@exam_app.route('/exam/<exam_id>/subject/<subject_id>', methods=['GET', 'PUT', 'DELETE'])
@exam_app.route('/exam/<exam_id>/sub-category/<subcategory_id>', methods=['GET'])
@exam_app.route('/exam/<exam_id>/sub-category/<subcategory_id>/subject', methods=['GET', 'POST'])
@exam_app.route('/exam/<exam_id>/sub-category/<subcategory_id>/subject/<subject_id>', methods=['GET', 'PUT', 'DELETE'])
def subject(exam_id, subcategory_id=None, subject_id=None):
    if not exam_id or type(exam_id) is not str:
        return {'message': 'exam_id is required', 'data': {}, 'status': False}, 400

    obj = Subject(request, exam_id, subcategory_id, subject_id)

    if request.method == 'GET':
        response, status = obj.get()
        return jsonify(response), status

    if request.method == 'POST':
        response, status = obj.post()
        return jsonify(response), status

    if request.method == 'PUT':
        response, status = obj.put()
        return jsonify(response), status

    if request.method == 'DELETE':
        response, status = obj.delete()
        return jsonify(response), status


@exam_app.route('/exam/<exam_id>/topic', methods=['GET', 'POST'])
@exam_app.route('/exam/<exam_id>/topic/<topic_id>', methods=['GET', 'PUT', 'DELETE'])
@exam_app.route('/exam/<exam_id>/sub-category/<subcategory_id>', methods=['GET'])
@exam_app.route('/exam/<exam_id>/sub-category/<subcategory_id>/subject/<subject_id>', methods=['GET'])
@exam_app.route('/exam/<exam_id>/subject/<subject_id>/topic', methods=['GET', 'POST'])
@exam_app.route('/exam/<exam_id>/subject/<subject_id>/topic/<topic_id>', methods=['GET', 'POST', 'PUT'])
@exam_app.route('/exam/<exam_id>/sub-category/<subcategory_id>/subject/<subject_id>/topic', methods=['GET', 'POST'])
@exam_app.route('/exam/<exam_id>/sub-category/<subcategory_id>/subject/<subject_id>/topic/<topic_id>',
                methods=['GET', 'PUT', 'DELETE'])
def topic(exam_id, subcategory_id=None, subject_id=None, topic_id=None):
    if not exam_id or type(exam_id) is not str:
        return {'message': 'exam_id is required', 'data': {}, 'status': False}, 400

    obj = Topic(request, exam_id, subcategory_id, subject_id, topic_id)

    if request.method == 'GET':
        response, status = obj.get()
        return jsonify(response), status

    if request.method == 'POST':
        response, status = obj.post()
        return jsonify(response), status

    if request.method == 'PUT':

        response, status = obj.put()
        return jsonify(response), status

    if request.method == 'DELETE':
        response, status = obj.delete()
        return jsonify(response), status
