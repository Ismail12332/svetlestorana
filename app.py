from flask import Flask, render_template, request, redirect, url_for, session,jsonify,abort,send_file
from pymongo import MongoClient
from passlib.hash import bcrypt
from bson import ObjectId
from datetime import datetime
from dotenv import load_dotenv
from flask_cors import CORS,cross_origin
from urllib.parse import quote
from b2sdk.v2 import *
import secrets
import uuid
import pprint
from openai import OpenAI
import traceback
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

load_dotenv()

def create_app():
    class User:
        def __init__(self, username, password, email):
            self.username = username
            self.password_hash = bcrypt.hash(password)
            self.email = email



    app = Flask(__name__, template_folder='templates')
    CORS(app, supports_credentials=True)
    app.secret_key = secrets.token_hex(32)
    client = MongoClient("mongodb://localhost:27017")
    app.db = client.my_database
    users_collection = app.db.users
    projects_collection = app.db.projects
    client = OpenAI(
        api_key="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",
    )

    # Создание клиента Backblaze B2
    info = InMemoryAccountInfo()
    b2_api = B2Api(info)
    application_key_id = '4ad4332a1370'
    application_key = '004787d4a1ca0ed42646b85d3f9cf9523f3c5847a4'
    b2_api.authorize_account("production", application_key_id, application_key)

    # Получение бакета (папки) для хранения изображений
    bucket_name = 'Survzila'
    bucket = b2_api.get_bucket_by_name(bucket_name)

    # Регистрация шрифта
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))

    @app.route("/", methods=["GET", "POST"])
    def login(supports_credentials=True):
        if request.method == "POST":
            data = request.json
            username = data.get("username")
            password = data.get("password")

            user = users_collection.find_one({"username": username})

            
            if user and bcrypt.verify(password, user["password_hash"]):
                user_id = user["user_id"]
                print({'status': 'success', 'user_id': str(user["_id"])})
                return jsonify({'status': 'success', 'user_id': str(user_id)})  # Возвращаем JSON-ответ

            return jsonify({'status': 'error', 'message': 'Incorrect username or password.'}), 401  # Возвращаем JSON-ответ

        return render_template("login.html")

    #выход
    @app.route("/logout")
    def logout():
        # Очищаем сессию пользователя при выходе
        session.pop("user_id", None)
        return redirect(url_for("login"))

    @app.route("/register", methods=["POST"])
    def register():
        data = request.json  # Получаем данные из JSON-запроса
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")

        # Проверка, что пользователь с таким именем уже не существует
        if users_collection.find_one({"username": username}):
            return "Пользователь с таким именем уже существует.", 400

        # Создание нового пользователя и сохранение его в базе данных
        user_id = secrets.token_urlsafe(16)  # Generate a random user_id
        new_user = User(username, password, email)
        users_collection.insert_one({
            "user_id": user_id,
            "username": new_user.username,
            "password_hash": new_user.password_hash,
            "email": new_user.email
        })

        return "Регистрация прошла успешно.", 200


    def create_project_pdf(project):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='CustomNormal', fontName='DejaVuSans'))

        # Добавление основной информации проекта
        story.append(Paragraph(f"First Name: {project['first_name']}", styles['Heading1']))
        story.append(Paragraph(f"Last Name: {project['last_name']}", styles['Heading1']))
        story.append(Paragraph(f"City: {project['city']}", styles['Heading1']))
        story.append(Spacer(1, 0.2 * inch))

        # Перебор разделов и подразделов
        for section_name, section_content in project['sections'].items():
            story.append(Paragraph(section_name, styles['Heading1']))
            for subsection_name, subsection_content in section_content.items():
                story.append(Paragraph(subsection_name, styles['Heading2']))

                # Добавление шагов
                for step in subsection_content['steps']:
                    story.append(Paragraph(step, styles['CustomNormal']))
                    story.append(Spacer(1, 0.1 * inch))

                # Добавление изображений
                for image_url in subsection_content['images']:
                    img = Image(image_url)
                    img.drawHeight = 2 * inch
                    img.drawWidth = 2 * inch
                    story.append(img)
                    story.append(Spacer(1, 0.2 * inch))

            story.append(Spacer(1, 0.2 * inch))

        doc.build(story)
        buffer.seek(0)
        return buffer


    @app.route('/download_project_pdf/<project_id>')
    def download_project_pdf(project_id):
        # Получение проекта по его ID (примерная реализация)
        project = projects_collection.find_one({"_id": ObjectId(project_id)})

        if not project:
            abort(404, description="Project not found")

        pdf_buffer = create_project_pdf(project)

        # Отправка PDF клиенту
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f"project_{project_id}.pdf",
            mimetype='application/pdf'
        )

    def convert_projects_to_list(projects):
        #Converts MongoDB projects to a list with ObjectId converted to string.
        projects_list = []
        for project in projects:
            project_data = {**project}
            project_data["_id"] = str(project["_id"])
            projects_list.append(project_data)
        print(projects_list)
        return projects_list
    

    @app.route("/glav", methods=["GET"])
    def get_projects(supports_credentials=True):
        user_id = request.args.get("user_id")
        print(user_id)
        projects = app.db.projects.find({"user_id": user_id})
        projects_list = convert_projects_to_list(projects)
        return jsonify({"status": "success", "user_id": str(user_id), "projects": projects_list})
    

    @app.route("/index2", methods=["POST"])
    def create_project():
        data = request.json  # Получаем данные из JSON-запроса
        user_id = data.get("user_id")
        print(user_id)

        # Обновляем запрос к базе данных, чтобы фильтровать проекты по user_id
        projects = app.db.projects.find({"user_id": user_id})
        projects_list = convert_projects_to_list(projects)

        user_id = data.get("user_id")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        city = data.get("city")
        phone = data.get("phone")
        post = data.get("post")
        vessel_name = data.get("vessel_name")

        # Создаем проект
        project = {
            "first_name": first_name,
            "last_name": last_name,
            "city": city,
            "phone": phone,
            "post": post,
            "sections": {
                    "introduction": {"gen_info": {"images": [],"steps": []},"certification": {"images": [],"steps": []},"purpose_of_survey": {"images": [],"steps": []},"circumstances_of_survey": {"images": [],"steps": []},"report_file_no": {"images": [],"steps": []},"surveyor_qualifications": { "images": [],"steps": []},"intended_use": {"images": [],"steps": []},
                    },
                    "hull": { "layout_overview": {"images": [],"steps": []},"design": {"images": [],"steps": []},"deck": {"images": [],"steps": []},"structural_members": {"images": [],"steps": []},"bottom_paint": {"images": [],"steps": []},"blister_comment": {"images": [],"steps": []},"transom": {"images": [],"steps": []},
                    },
                    "above": { "deck_floor_plan": {"images": [],"steps": []},"anchor_platform": {"images": [],"steps": []},"toe_rails": {"images": [],"steps": []},"mooring_hardware": {"images": [],"steps": []},"hatches": {"images": [],"steps": []},"exterior_seating": {"images": [],"steps": []},"cockpit_equipment": {"images": [],"steps": []},"ngine_hatch": {"images": [],"steps": []},"above_draw_water_line": {"images": [],"steps": []},"boarding_ladder": {"images": [],"steps": []},"swim_platform": {"images": [],"steps": []},
                    },
                    "below": { "below_draw_water": {"images": [],"steps": []},"thru_hull_strainers": {"images": [],"steps": []},"transducer": {"images": [],"steps": []},"sea_valves": {"images": [],"steps": []},"sea_strainers": {"images": [],"steps": []},"trim_tabs": {"images": [],"steps": []},"note": {"images": [],"steps": []},
                    },
                    "cathodic": { "bonding_system": {"images": [],"steps": []},"anodes": {"images": [],"steps": []},"lightning_protection": {"images": [],"steps": []},"additional_remarks": {"images": [],"steps": []},
                    },
                    "helm": { "helm_station": {"images": [],"steps": []},"throttle_shift_controls": {"images": [],"steps": []},"engine_room_blowers": {"images": [],"steps": []},"engine_status": {"images": [],"steps": []},"other_electronics_controls": {"images": [],"steps": []},
                    },
                    "cabin": { "entertainment_berthing": {"images": [],"steps": []},"interior_lighting": {"images": [],"steps": []},"galley_dinette": {"images": [],"steps": []},"water_closets": {"images": [],"steps": []},"climate_control": {"images": [],"steps": []},
                    },
                    "electrical": { "dc_systems_type": {"images": [],"steps": []},"ac_systems": {"images": [],"steps": []},"generator": {"images": [],"steps": []},
                    },
                    "inboard": { "engines": {"images": [],"steps": []},"serial_numbers": {"images": [],"steps": []},"engine_hours": {"images": [],"steps": []},"other_note": {"images": [],"steps": []},"reverse_gears": {"images": [],"steps": []},"shafting_propellers": {"images": [],"steps": []},
                    },
                    "steering": { "manufacture": {"images": [],"steps": []},"steering_components": {"images": [],"steps": []},
                    },
                    "tankage": { "fuel": {"images": [],"steps": []},"potable_water_system": {"images": [],"steps": []},"holding_tank_black_water": {"images": [],"steps": []},
                    },
                    "safety": { "navigational_lights": {"images": [],"steps": []},"life_jackets": {"images": [],"steps": []},"throwable_pfd": {"images": [],"steps": []},"visual_distress_signals": {"images": [],"steps": []},"sound_devices": {"images": [],"steps": []},"uscg_placards": {"images": [],"steps": []},"flame_arrestors": {"images": [],"steps": []},"engine_ventilation": {"images": [],"steps": []},"ignition_protection": {"images": [],"steps": []},"inland_navigational_rule_book": {"images": [],"steps": []},"waste_management_plan": {"images": [],"steps": []},"fire_fighting_equipment": {"images": [],"steps": []},"bilge_pumps": {"images": [],"steps": []},"ground_tackle_windlass": {"images": [],"steps": []},"auxiliary_safety_equipment": {"images": [],"steps": []},
                    },
                },
            "sectionse": [],
            "vessel_name": vessel_name,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": user_id
        }

        result = app.db.projects.insert_one(project)
        project_id = result.inserted_id

        print("Entry added:", first_name, last_name, city, phone, post, vessel_name, user_id, project_id, projects_list)
        return jsonify({"status": "success", "user_id": str(user_id), "project_id": str(project_id)})




    #Переключение на проект в главное странице нажатие на имя проекта
    @app.route("/EditProject/<string:project_id>", methods=["GET"])
    def edit_project(project_id,supports_credentials=True):
        try:
            # Преобразовываем project_id в ObjectId
            project_id = ObjectId(project_id)
        except Exception as e:
            # Обработка ошибки, если project_id неверного формата
            return jsonify({"status": "error", "message": "Invalid project_id"}), 400

        # Проверяем, что текущий пользователь имеет доступ к проекту
        project = app.db.projects.find_one({"_id": project_id})
        if project is None:
            return jsonify({"status": "error", "message": "Project not found"}), 404

        project['_id'] = str(project['_id'])
        # Возвращаем данные о проекте в формате JSON
        print(f"Fetching project with ID: {project_id}", project)

        return jsonify({"status": "success", "project": project})

    #Добавление изображения для подразделов стандартных разделов
    @app.route('/edit_project/upload_image/<project_id>/<section_name>/<subsection_name>', methods=['POST'])
    def upload_image(project_id, section_name, subsection_name):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return jsonify({"status": "error", "message": "Invalid project_id"}), 400
        
        if 'file' not in request.files:
            return jsonify({"status": "error", "message": "No file part"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"status": "error", "message": "No selected file"}), 400

        if file:
            file_data = file.read()
            file_name = file.filename
            b2_file_name = str(uuid.uuid4())

            bucket.upload_bytes(
                data_bytes=file_data,
                file_name=b2_file_name
            )

            file_info = {
                'file_name': file_name,
                'b2_file_name': b2_file_name,
                'b2_url': 'https://f004.backblazeb2.com/file/Survzila/' + quote(b2_file_name)
            }
            app.db.files.insert_one(file_info)
            print(section_name, subsection_name)

            # Обновление проекта с добавлением информации о загруженном изображении
            app.db.projects.update_one(
                {"_id": project_id, f"{section_name}.name": subsection_name},
                {"$push": {f"{section_name}.$.subsections": {"image_url": file_info['b2_url']}}}
            )

            updated_project = app.db.projects.find_one({"_id": project_id})
            updated_project["_id"] = str(updated_project["_id"])
            
            return jsonify({
                "status": "success",
                "message": "Image uploaded successfully",
                "image_url": file_info['b2_url'],
                "updated_project": updated_project
            }), 200
        else:
            return jsonify({"status": "error", "message": "Failed to upload file"}), 400
        

    #delite
    @app.route('/edit_project/<project_id>/<section_name>/<subsection_name>/delete_images', methods=['POST'])
    def delete_images(project_id, section_name, subsection_name):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return jsonify({"status": "error", "message": "Invalid project_id"}), 400
        
        image_url = request.json.get('image_url')

            # Удаление изображения из базы данных проекта
        result = app.db.projects.update_one(
            {"_id": project_id, f"{section_name}.name": subsection_name},
            {"$pull": {f"{section_name}.$.subsections": {"image_url": image_url}}}
        )
        updated_project = app.db.projects.find_one({"_id": project_id})
        updated_project["_id"] = str(updated_project["_id"])

        if result.modified_count > 0:
            return jsonify({"status": "success", "message": "Image deleted successfully","updated_project": updated_project}), 200
        else:
            return jsonify({"status": "error", "message": "Failed to delete image"}), 400

        

    @app.route('/edit_project/<project_id>/<section_name>/<subsection_name>/add_image', methods=['POST'])
    def add_image(project_id,section_name, subsection_name):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return jsonify({"status": "error", "message": "Invalid project_id"}), 400

        # Получение файла из запроса
        if 'file' not in request.files:
            return jsonify({"status": "error", "message": "No file part"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"status": "error", "message": "No selected file"}), 400

        if file:
            file_data = file.read()
            file_name = file.filename
            b2_file_name = str(uuid.uuid4())

            bucket.upload_bytes(
                data_bytes=file_data,
                file_name=b2_file_name
            )

            file_info = {
                'file_name': file_name,
                'b2_file_name': b2_file_name,
                'b2_url': 'https://f004.backblazeb2.com/file/Survzila/' + quote(b2_file_name)
            }

            print(file_info)
            # Обновление проекта с добавлением информации о загруженном изображении
            app.db.projects.update_one(
                {"_id": project_id, "sectionse.name": section_name, "sectionse.subsections.name": subsection_name},
                {"$push": {"sectionse.$.subsections.$[elem].images": {"image_url": file_info['b2_url']}}},
                array_filters=[{"elem.name": subsection_name}]
            )

            updated_project = app.db.projects.find_one({"_id": project_id})
            updated_project["_id"] = str(updated_project["_id"])
            pprint.pprint(updated_project)
            return jsonify({
                "status": "success",
                "message": "Image uploaded successfully",
                "image_url": file_info['b2_url'],
                "updated_project": updated_project
            }), 200
        else:
            return jsonify({"status": "error", "message": "Failed to upload file"}), 400
        

    @app.route('/edit_project/<project_id>/<section_name>/<subsection_name>/delete_image', methods=['POST'])
    def delete_image(project_id, section_name, subsection_name):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return jsonify({"status": "error", "message": "Invalid project_id"}), 400

        image_url = request.json.get('image_url')  # Получение URL изображения из запроса

        # Удаление изображения из подраздела в базе данных
        result = app.db.projects.update_one(
            {"_id": project_id, f"sectionse.name": section_name, f"sectionse.subsections.name": subsection_name},
            {"$pull": {f"sectionse.$.subsections.$[elem].images": {"image_url": image_url}}},
            array_filters=[{"elem.name": subsection_name}]
        )
        updated_project = app.db.projects.find_one({"_id": project_id})
        updated_project["_id"] = str(updated_project["_id"])

        if result.modified_count > 0:
            return jsonify({"status": "success", "message": "Image deleted successfully","updated_project": updated_project}), 200
        else:
            return jsonify({"status": "error", "message": "Failed to delete image"}), 400


    #Дабовление и удаление записей в стандартные разделы разделах
    @app.route("/edit_project/<project_id>/add_step_standard", methods=["POST"])
    def add_step_standard(project_id):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return jsonify({"status": "error", "message": "Invalid project_id"}), 400
        
        section_name = request.form.get("section_name")
        subsection_name = request.form.get("subsection_name")
        step_description = request.form.get("step_description")

        # Добавьте ваш код для обработки данных и добавления шага в соответствующий подраздел
        print(section_name,subsection_name, step_description)

        updated_project = app.db.projects.find_one_and_update(
            {"_id": project_id, f"{section_name}.name": subsection_name},
            {"$push": {f"{section_name}.$.subsections": {"step_description": step_description}}}
        )

        updated_project = app.db.projects.find_one({"_id": project_id})
        updated_project["_id"] = str(updated_project["_id"])
        print('твой проект',updated_project)
        return jsonify({
            "status": "success",
            "message": "Step added successfully",
            "step_description": step_description,
            "section_name": section_name,
            "subsection_name": subsection_name,
            "updated_project": updated_project
        })
        

    #Дабовление и удаление записей в разделах (нужно переделать)--------------------------------------------------
    @app.route("/edit_project/<project_id>/add_step", methods=["POST"])
    def add_step(project_id):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return jsonify({"status": "error", "message": "Invalid project_id"}), 400

        data = request.json
        section = data.get("section")
        subsection = data.get("subsection")
        step_description = data.get("step_description")
        print(section,subsection,step_description)

        try:
            # Обновляем структуру базы данных, чтобы каждый раздел содержал список подразделов,
            # а каждый подраздел содержал список шагов
            result = app.db.projects.update_one(
                {"_id": project_id, f"sections.{section}.{subsection}": {"$exists": True}},
                {"$push": {f"sections.{section}.{subsection}.steps": step_description}}
            )

            if result.modified_count == 0:
                return jsonify({"status": "error", "message": "Project or section not found"}), 404

            # Получаем обновленный проект после добавления шага
            updated_project = app.db.projects.find_one({"_id": project_id})

            # Преобразуем ObjectId в строку перед возвратом ответа JSON
            updated_project["_id"] = str(updated_project["_id"])

            return jsonify({"status": "success", "message": "Step added successfully", "updated_project": updated_project})
        except Exception as e:
            print("Error:", e)
            return jsonify({"status": "error", "message": "An error occurred"}), 500


    @app.route("/edit_project/<project_id>/add_subsection_step", methods=["POST"])
    def add_subsection_step(project_id):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return "Invalid project_id", 400

        section_name = request.form.get("section_name")
        subsection_name = request.form.get("subsection_name")
        step_description = request.form.get("step_description")

        try:
            result = app.db.projects.update_one(
                {"_id": project_id, "sectionse.name": section_name},
                {"$push": {"sectionse.$.subsections.$[s].cells": {"description": step_description}}},
                array_filters=[{"s.name": subsection_name}]
            )
            if result.modified_count == 0:
                return "Section or subsection not found in the project", 404
        except Exception as e:
            print("Error:", e)
            return "An error occurred", 500

        updated_project = app.db.projects.find_one({"_id": project_id})
        updated_project['_id'] = str(updated_project['_id'])

        return jsonify({"status": "success", "message": "Step added successfully", "updated_project": updated_project})
    

    #Добавление изображения в основные подразделы (нужно переделать)-----------------------------------------
    @app.route('/edit_project/<project_id>/add_imagestandard', methods=['POST'])
    def add_imagestandard(project_id):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return jsonify({"status": "error", "message": "Invalid project_id"}), 400

        # Получение файла из запроса
        if 'image_upload' not in request.files:
            return jsonify({"status": "error", "message": "No file part"}), 400

        image_file = request.files['image_upload']

        if image_file.filename == '':
            return jsonify({"status": "error", "message": "No selected file"}), 400

        if image_file:
            file_data = image_file.read()
            file_name = image_file.filename
            b2_file_name = str(uuid.uuid4())

            bucket.upload_bytes(
                data_bytes=file_data,
                file_name=b2_file_name
            )

            file_info = {
                'file_name': file_name,
                'b2_file_name': b2_file_name,
                'b2_url': 'https://f004.backblazeb2.com/file/Survzila/' + quote(b2_file_name)
            }
            app.db.files.insert_one(file_info)

            # Получение описания изображения и раздела
            section = request.form.get('section')
            subsection = request.form.get("subsection")
            print(section,subsection)
            section_field = f"{section}_steps"
            # Обновление проекта с добавлением информации о загруженном изображении
            app.db.projects.update_one(
                {"_id": project_id, f"sections.{section}.{subsection}": {"$exists": True}},
                {"$push": {f"sections.{section}.{subsection}.images": file_info["b2_url"]}}
            )

            updated_project = app.db.projects.find_one({"_id": project_id})
            updated_project["_id"] = str(updated_project["_id"])

            return jsonify({
                "status": "success",
                "message": "Image uploaded successfully",
                "updated_project": updated_project
            }), 200
        else:
            return jsonify({"status": "error", "message": "Failed to upload file"}), 400
        

    @app.route("/edit_project/<project_id>/remove_image", methods=["POST"])
    def remove_image(project_id):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return jsonify({"status": "error", "message": "Invalid project_id"}), 400

        data = request.json
        section = data.get("section")
        subsection = data.get("subsection")
        image = data.get("image")

        try:
            # Удаляем изображение из списка
            result = app.db.projects.update_one(
                {"_id": project_id, f"sections.{section}.{subsection}.images": image},
                {"$pull": {f"sections.{section}.{subsection}.images": image}}
            )

            if result.modified_count == 0:
                return jsonify({"status": "error", "message": "Image not found"}), 404

            # Получаем обновленный проект после удаления изображения
            updated_project = app.db.projects.find_one({"_id": project_id})

            # Преобразуем ObjectId в строку перед возвратом ответа JSON
            updated_project["_id"] = str(updated_project["_id"])

            return jsonify({"status": "success", "message": "Image removed successfully", "updated_project": updated_project})
        except Exception as e:
            print("Error:", e)
            return jsonify({"status": "error", "message": "An error occurred"}), 500


    @app.route("/edit_project/<project_id>/remove_step", methods=["POST"])
    def remove_step(project_id):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return jsonify({"status": "error", "message": "Invalid project_id"}), 400

        data = request.json
        section = data.get("section")
        subsection = data.get("subsection")
        step_description = data.get("step_description")

        try:
            # Выполните удаление шага из базы данных
            result = app.db.projects.update_one(
                {"_id": project_id, f"sections.{section}.{subsection}.steps": step_description},
                {"$pull": {f"sections.{section}.{subsection}.steps": step_description}}
            )

            if result.modified_count == 0:
                return jsonify({"status": "error", "message": "Step not found"}), 404

            # Получите обновленный проект после удаления шага
            updated_project = app.db.projects.find_one({"_id": project_id})

            # Преобразуйте ObjectId в строку перед возвратом ответа JSON
            updated_project["_id"] = str(updated_project["_id"])

            return jsonify({"status": "success", "message": "Step removed successfully", "updated_project": updated_project})
        except Exception as e:
            print("Error:", e)
            return jsonify({"status": "error", "message": "An error occurred"}), 500

    @app.route("/edit_project/<project_id>/delete_step", methods=["POST"])
    def delete_step(project_id):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return jsonify({"status": "error", "message": "Invalid project_id"}), 400

        step_to_delete = request.form.get("step_to_delete")
        section = request.form.get("section")
        project = app.db.projects.find_one({"_id": project_id})

        if not project:
            return jsonify({"status": "error", "message": "Project not found"}), 404

        try:
            result = app.db.projects.update_one(
                {"_id": project_id},
                {"$pull": {f"{section}_steps": step_to_delete}}
            )
            if result.modified_count == 0:
                return jsonify({"status": "error", "message": "Step not found"}), 404
        except Exception as e:
            print("Error:", e)
            return jsonify({"status": "error", "message": "An error occurred"}), 500

        # Получите обновленный проект после добавления шага
        updated_project = app.db.projects.find_one({"_id": project_id})

        # Преобразуйте ObjectId в строку перед возвратом ответа JSON
        updated_project["_id"] = str(updated_project["_id"])

        return jsonify({"status": "success", "message": "Step deleted successfully", "updated_project": updated_project})


    #----------------------------------------------------------------
    #Добавление раздела
    @app.route("/edit_project/<project_id>/add_section", methods=["POST"])
    def add_section(project_id):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return "Invalid project_id", 400

        section_name = request.form.get("section_name")

        try:
            result = app.db.projects.update_one(
                {"_id": project_id},
                {"$push": {"sectionse": {"name": section_name, "subsections": []}}}
            )
            if result.modified_count == 0:
                return "Project not found", 404
        except Exception as e:
            print("Error:", e)
            return "An error occurred", 500
        updated_project = app.db.projects.find_one({"_id": project_id})
        updated_project['_id'] = str(updated_project['_id'])
        
        return jsonify({"status": "success", "message": "Section added successfully", "updated_project": updated_project})


    #--удаление раздела
    @app.route("/edit_project/<project_id>/delete_section/<section_name>", methods=["POST"])
    def delete_section(project_id, section_name):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return "Invalid project_id", 400

        try:
            result = app.db.projects.update_one(
                {"_id": project_id},
                {"$pull": {"sections": {"name": section_name}}}
            )
            if result.modified_count == 0:
                return "Section not found in the project", 404
        except Exception as e:
            print("Error:", e)
            return "An error occurred", 500

        return redirect(url_for("edit_project", project_id=project_id))


    #Добавление подраздела
    @app.route("/edit_project/<project_id>/add_subsection", methods=["POST"])
    def add_subsection(project_id):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return "Invalid project_id", 400

        section_name = request.form.get("section_name")
        subsection_name = request.form.get("subsection_name")

        try:
            result = app.db.projects.update_one(
                {"_id": project_id, "sectionse.name": section_name},
                {"$push": {"sectionse.$.subsections": {"name": subsection_name, "cells": []}}}
            )
            if result.modified_count == 0:
                return "Section not found in the project", 404
        except Exception as e:
            print("Error:", e)
            return "An error occurred", 500

        updated_project = app.db.projects.find_one({"_id": project_id})
        updated_project['_id'] = str(updated_project['_id'])
        
        return jsonify({"status": "success", "message": "Section added successfully", "updated_project": updated_project})
    
    #Добавление подраздела стандартного
    @app.route("/edit_project/<project_id>/add_subsection_standard", methods=["POST"])
    def add_subsection_standard(project_id):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return "Invalid project_id", 400
        
        section_name = request.form.get("section_name")
        subsection_name = request.form.get("subsection_name")

        try:
            # Добавляем новый подраздел в указанный раздел
            result = app.db.projects.update_one(
                {"_id": project_id, f"sections.{section_name}": {"$exists": True}},
                {"$set": { f"sections.{section_name}.{subsection_name}": {"images": [], "steps": []}}}
            )
            
            if result.modified_count == 0:
                return "Section not found in the project", 404
        except Exception as e:
            print("Error:", e)
            return "An error occurred", 500
        
        updated_project = app.db.projects.find_one({"_id": project_id})
        updated_project['_id'] = str(updated_project['_id'])

        return jsonify({"status": "success", "message": "Subsection added successfully", "project": updated_project})


    #чат джипити
    @app.route('/edit_project/<project_id>/get-gpt-recommendations', methods=['POST'])
    def get_gpt_recommendations(project_id):
        data = request.json
        section = data['section']
        subsection = data['subsection']
        prompt = f"Пожалуйста, дайте рекомендации для осмотра яхты для раздела {section}, подраздела {subsection}. Что стоит осмотреть и проверить при осмотре {subsection}?"

        try:
            response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты помощник клиента в осмотре яхты указываешь на то что стоит проверить и как лучше проверять"},
                {"role": "user", "content": prompt}
            ]
            )
            print(response)
            recommendations = response.choices[0].message.content.strip()
            return jsonify({'recommendations': recommendations})
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            traceback.print_exc()
            return jsonify({'error': str(e)}), 500
            
    
    #--удаление подраздела
    @app.route("/edit_project/<project_id>/delete_subsection/<section_name>/<subsection_name>", methods=["POST"])
    def delete_subsection(project_id, section_name, subsection_name):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return "Invalid project_id", 400

        try:
            result = app.db.projects.update_one(
                {"_id": project_id, "sections.name": section_name},
                {"$pull": {"sections.$.subsections": {"name": subsection_name}}}
            )
            if result.modified_count == 0:
                return "Subsection not found in the project", 404
        except Exception as e:
            print("Error:", e)
            return "An error occurred", 500

        return redirect(url_for("edit_project", project_id=project_id))


    #Добавление ячейки
    @app.route("/edit_project/<project_id>/add_cell", methods=["POST"])
    def add_cell(project_id):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return "Invalid project_id", 400

        section_name = request.form.get("section_name")
        subsection_name = request.form.get("subsection_name")
        cell_name = request.form.get("cell_name")
        cell_description = request.form.get("cell_description")

        try:
            result = app.db.projects.update_one(
                {"_id": project_id},
                {
                    "$push": {
                        "sections.$[section].subsections.$[subsection].cells": {
                            "name": cell_name,
                            "description": cell_description
                        }
                    }
                },
                array_filters=[
                    {"section.name": section_name},
                    {"subsection.name": subsection_name}
                ]
            )
            if result.modified_count == 0:
                return "Section or subsection not found in the project", 404
        except Exception as e:
            print("Error:", e)
            return "An error occurred", 500

        return redirect(url_for("edit_project", project_id=project_id))



    #--удаление ячейки
    @app.route("/edit_project/<project_id>/delete_cell/<section_name>/<subsection_name>/<cell_name>", methods=["POST"])
    def delete_cell(project_id, section_name, subsection_name, cell_name):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return "Invalid project_id", 400

        try:
            # Находим проект по идентификатору
            project = app.db.projects.find_one({"_id": project_id})

            # Находим раздел, подраздел и ячейку, которую нужно удалить
            section_index = None
            subsection_index = None
            cell_index = None

            for i, section in enumerate(project["sections"]):
                if section["name"] == section_name:
                    section_index = i
                    for j, subsection in enumerate(section["subsections"]):
                        if subsection["name"] == subsection_name:
                            subsection_index = j
                            for k, cell in enumerate(subsection["cells"]):
                                if cell["name"] == cell_name:
                                    cell_index = k

            # Если раздел, подраздел и ячейка найдены, удаляем ячейку
            if section_index is not None and subsection_index is not None and cell_index is not None:
                del project["sections"][section_index]["subsections"][subsection_index]["cells"][cell_index]

                # Обновляем документ проекта в базе данных
                app.db.projects.update_one({"_id": project_id}, {"$set": project})

            else:
                return "Cell not found in the project", 404

        except Exception as e:
            print("Error:", e)
            return "An error occurred", 500

        return redirect(url_for("edit_project", project_id=project_id))



    # -- удаление комментария
    @app.route("/edit_project/<project_id>/delete_comment/<section_name>/<subsection_name>/<cell_name>", methods=["POST"])
    def delete_comment(project_id, section_name, subsection_name, cell_name):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return "Invalid project_id", 400

        try:
            result = app.db.projects.update_one(
                {
                    "_id": project_id,
                    "sections.name": section_name,
                    "sections.subsections.name": subsection_name,
                    "sections.subsections.cells.name": cell_name
                },
                {
                    "$unset": {
                        "sections.$[section].subsections.$[subsection].cells.$[cell].comment": ""
                    }
                },
                array_filters=[
                    {"section.name": section_name},
                    {"subsection.name": subsection_name},
                    {"cell.name": cell_name}
                ]
            )
            if result.modified_count == 0:
                return "Section, subsection, or cell not found in the project", 404
        except Exception as e:
            print("Error:", e)
            return "An error occurred", 500

        return redirect(url_for("edit_project", project_id=project_id))
        


    #Добавление коментария
    @app.route("/edit_project/<project_id>/add_comment/<section_name>/<subsection_name>/<cell_name>", methods=["POST"])
    def add_comment(project_id, section_name, subsection_name, cell_name):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return "Invalid project_id", 400

        cell_comment = request.form.get("cell_comment")

        try:
            result = app.db.projects.update_one(
                {
                    "_id": project_id,
                    "sections.name": section_name,
                    "sections.subsections.name": subsection_name,
                    "sections.subsections.cells.name": cell_name
                },
                {
                    "$set": {
                        "sections.$[section].subsections.$[subsection].cells.$[cell].comment": cell_comment
                    }
                },
                array_filters=[
                    {"section.name": section_name},
                    {"subsection.name": subsection_name},
                    {"cell.name": cell_name}
                ]
            )
            if result.modified_count == 0:
                return "Section, subsection, or cell not found in the project", 404
        except Exception as e:
            print("Error:", e)
            return "An error occurred", 500

        return redirect(url_for("edit_project", project_id=project_id))



    # #--удаление рейтинга
    @app.route("/edit_project/<project_id>/delete_rating/<section_name>/<subsection_name>/<cell_name>", methods=["POST"])
    def delete_rating(project_id, section_name, subsection_name, cell_name):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return "Invalid project_id", 400

        try:
            # Находим проект по идентификатору
            project = app.db.projects.find_one({"_id": project_id})

            # Находим раздел, подраздел, ячейку и рейтинг, который нужно удалить
            section_index = None
            subsection_index = None
            cell_index = None
            rating_index = None

            for i, section in enumerate(project["sections"]):
                if section["name"] == section_name:
                    section_index = i
                    for j, subsection in enumerate(section["subsections"]):
                        if subsection["name"] == subsection_name:
                            subsection_index = j
                            for k, cell in enumerate(subsection["cells"]):
                                if cell["name"] == cell_name:
                                    cell_index = k
                                    if "rating" in cell:
                                        rating_index = "rating"

            # Если раздел, подраздел, ячейка и рейтинг найдены, удаляем рейтинг
            if (
                section_index is not None
                and subsection_index is not None
                and cell_index is not None
                and rating_index is not None
            ):
                del project["sections"][section_index]["subsections"][subsection_index]["cells"][cell_index][rating_index]

                # Обновляем документ проекта в базе данных
                app.db.projects.update_one({"_id": project_id}, {"$set": project})

            else:
                return "Rating not found in the project", 404

        except Exception as e:
            print("Error:", e)
            return "An error occurred", 500

        return redirect(url_for("edit_project", project_id=project_id))
        


    #Добавление рейтинга
    @app.route("/edit_project/<project_id>/add_rating/<section_name>/<subsection_name>/<cell_name>", methods=["POST"])
    def add_rating(project_id, section_name, subsection_name, cell_name):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return "Invalid project_id", 400

        cell_rating = request.form.get("cell_rating")

        try:
            result = app.db.projects.update_one(
                {
                    "_id": project_id,
                    "sections.name": section_name,
                    "sections.subsections.name": subsection_name,
                    "sections.subsections.cells.name": cell_name
                },
                {
                    "$set": {
                        "sections.$[section].subsections.$[subsection].cells.$[cell].rating": cell_rating
                    }
                },
                array_filters=[
                    {"section.name": section_name},
                    {"subsection.name": subsection_name},
                    {"cell.name": cell_name}
                ]
            )
            if result.modified_count == 0:
                return "Section, subsection, or cell not found in the project", 404
        except Exception as e:
            print("Error:", e)
            return "An error occurred", 500

        return redirect(url_for("edit_project", project_id=project_id))

    if __name__ == "__main__":
        app.run(debug=True)
    
    return app
