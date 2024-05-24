import os
from flask import Flask, render_template, request, redirect, url_for, session,jsonify,abort,send_file, make_response
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
import jwt
import requests
from jose import jwt, JWTError
from functools import wraps
from openai import OpenAI
import traceback
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Indenter, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.graphics.shapes import Drawing, Line
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import html
import time


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
        api_key="",
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


    # Конфигурация Auth0
    AUTH0_DOMAIN = 'dev-whbba5qnfveb88fc.us.auth0.com'
    API_AUDIENCE = 'http://Survzilla'
    ALGORITHMS = ['RS256']


    # Получение открытых ключей Auth0 с обработкой ошибок
    jwks_url = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'

    def get_jwks():
        for attempt in range(3):  # Попробуем три раза
            try:
                jwks = requests.get(jwks_url).json()
                return jwks
            except requests.exceptions.ConnectionError as e:
                print(f"Ошибка соединения при попытке {attempt + 1}: {e}")
                time.sleep(1)  # Подождем секунду перед повторной попыткой
        raise RuntimeError("Не удалось получить JWKS ключи после нескольких попыток")

    jwks = get_jwks()

    def get_rsa_key(header):
        for key in jwks['keys']:
            if key['kid'] == header['kid']:
                return {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }
        return None

    def requires_auth(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth_header = request.headers.get('Authorization', None)
            if not auth_header:
                return jsonify({"message": "Authorization header is missing"}), 401

            token = auth_header.split()[1]
            try:
                header = jwt.get_unverified_header(token)
                rsa_key = get_rsa_key(header)
                if not rsa_key:
                    return jsonify({"message": "Invalid header"}), 401

                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer=f'https://{AUTH0_DOMAIN}/'
                )
            except JWTError as e:
                return jsonify({"message": "Invalid token"}), 401

            request.user = payload
            return f(*args, **kwargs)
        return decorated



    @app.route("/", methods=["GET"])
    def login(supports_credentials=True):
        return render_template("login.html")
    

    @app.route("/api/vitrine", methods=["GET"])
    def get_vitrine_projects():
        try:
            projects = list(app.db.vitrine.find({}))
            for project in projects:
                project['_id'] = str(project['_id'])
                project['project_id'] = str(project['project_id'])
            return jsonify({"status": "success", "projects": projects}), 200
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500
    

    #выход
    @app.route("/logout")
    def logout():
        # Очищаем сессию пользователя при выходе
        session.pop("user_id", None)
        return redirect(url_for("login"))


    def create_project_pdf(project):
        buffer = BytesIO()
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='CustomNormal', fontName='DejaVuSans'))
        styles.add(ParagraphStyle(name='CenteredHeading1', parent=styles['Heading1'], alignment=1))

        def build_story(project):
            story = []

            # Добавление основной информации проекта
            Survey_logo = "static/images/survz.webp"
            img = Image(Survey_logo)
            img.drawHeight = 2 * inch
            img.drawWidth = 2 * inch
            story.append(img)

            F_L_Name = project['first_name'] + " " + project['last_name']
            story.append(Paragraph(f"Survzilla Survey Report for {F_L_Name}", styles['CenteredHeading1']))
            story.append(Paragraph(f"Vessel - {project['vessel_name']}", styles['CenteredHeading1']))

            gen_info_images = project['sections']['introduction']['gen_info'].get('images', [])
            if gen_info_images:
                intro_image_url = gen_info_images[0]
                intro_image = Image(intro_image_url)
                intro_image.drawHeight = 5 * inch
                intro_image.drawWidth = 5 * inch
                story.append(intro_image)
            story.append(Spacer(1, 0.2 * inch))
            story.append(PageBreak())

            for section_name, section_content in project['sections'].items():
                # Проверка, есть ли в подразделах непустые данные
                has_non_empty_subsection = False
                for subsection_name, subsection_content in section_content.items():
                    if subsection_content['steps'] or subsection_content['images']:
                        has_non_empty_subsection = True
                        break
                
                if not has_non_empty_subsection:
                    continue  # Пропускаем этот раздел, если все его подразделы пусты

                cleaned_section_name = section_name.replace('_', ' ').title()
                story.append(Paragraph(cleaned_section_name, styles['CenteredHeading1']))

                for subsection_name, subsection_content in section_content.items():
                    if subsection_content['steps'] or subsection_content['images']:
                        cleaned_subsection_name = subsection_name.replace('_', ' ').title()
                        story.append(Paragraph(cleaned_subsection_name, styles['CustomNormal']))

                        images = []
                        for image_url in subsection_content['images']:
                            img = Image(image_url)
                            img.drawHeight = 2 * inch
                            img.drawWidth = 2 * inch
                            images.append(img)
                            if len(images) == 2:
                                story.append(Table([images], colWidths=[2.5 * inch, 2.5 * inch]))
                                story.append(Spacer(1, 0.2 * inch))
                                images = []
                        if images:
                            story.append(Table([images], colWidths=[2.5 * inch, 2.5 * inch]))
                            story.append(Spacer(1, 0.2 * inch))

                        story.append(Indenter(left=20))
                        
                        for step in subsection_content['steps']:
                            step = html.escape(step)
                            story.append(Paragraph(step, styles['CustomNormal']))
                            story.append(Spacer(1, 0.1 * inch))
                        story.append(Indenter(left=-20))

                story.append(Spacer(0.5, 0.2 * inch))
                story.append(Spacer(1, 0.2 * inch))
                story.append(Spacer(0.5, 0.2 * inch))

            return story

        # Создаем временный PDF для определения общего количества страниц
        temp_buffer = BytesIO()
        temp_doc = SimpleDocTemplate(temp_buffer, pagesize=letter)
        story = build_story(project)
        temp_doc.build(story)
        total_pages = temp_doc.page

        # Создаем основной PDF с нумерацией страниц
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)

        def on_first_page(canvas, doc):
            page_num = canvas.getPageNumber()
            text = f"{project['vessel_name']} inspected by Survzilla Boat Inspection page {page_num} of {total_pages}"
            canvas.setFont('Helvetica', 10)
            canvas.drawRightString(doc.width + doc.rightMargin, 0.75 * inch, text)

        def on_later_pages(canvas, doc):
            page_num = canvas.getPageNumber()
            text = f"'{project['vessel_name']}' inspected by Survzilla Boat Inspection page {page_num} of {total_pages}"

            canvas.setFont('Helvetica-Bold', 12)
            canvas.drawString(doc.leftMargin, doc.height + doc.topMargin + 35, project['vessel_name'])
            canvas.setStrokeColor(colors.black)
            canvas.setLineWidth(0.5)
            canvas.line(doc.leftMargin, doc.height + doc.topMargin + 25, doc.width + doc.leftMargin, doc.height + doc.topMargin + 25)
            canvas.line(doc.leftMargin, doc.height + doc.topMargin + 27, doc.width + doc.leftMargin, doc.height + doc.topMargin + 27)

            canvas.setFont('Helvetica', 10)
            canvas.drawRightString(doc.width + doc.rightMargin, 0.75 * inch, text)

        story = build_story(project)
        doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
        buffer.seek(0)
        return buffer


    @app.route('/download_project_pdf/<project_id>')
    @requires_auth
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
        return projects_list
    

    @app.route("/api/glav", methods=["GET"])
    @requires_auth
    def get_projects(supports_credentials=True):
        user_id = request.user.get('sub')  # Извлекаем user_id из токена
        projects = app.db.projects.find({"user_id": user_id})
        projects_list = convert_projects_to_list(projects)
        return jsonify({"status": "success", "user_id": str(user_id), "projects": projects_list})
    

    @app.route("/glav", methods=["GET"])
    @requires_auth
    def get_projectse(supports_credentials=True):
            return render_template("index.html")
    


    @app.route("/index2", methods=["POST"])
    @requires_auth
    def create_project():
        user_id = request.user.get("sub")
        data = request.json  # Получаем данные из JSON-запроса
        # Обновляем запрос к базе данных, чтобы фильтровать проекты по user_id
        projects = app.db.projects.find({"user_id": user_id})
        projects_list = convert_projects_to_list(projects)

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
            "vessel_name": vessel_name,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": user_id
        }

        result = app.db.projects.insert_one(project)
        project_id = result.inserted_id

        print("Entry added:", first_name, last_name, city, phone, post, vessel_name, user_id, project_id, projects_list)
        return jsonify({"status": "success", "user_id": str(user_id), "project_id": str(project_id)})



    # Проверка, что текущий пользователь является владельцем проекта
    def check_project_owner(user_id, project_id):
        project = app.db.projects.find_one({"_id": ObjectId(project_id), "user_id": user_id})
        return project is not None


    @app.route("/api/update_criticality", methods=["POST"])
    @requires_auth
    def update_criticality():
        user_id = request.user.get('sub')  # Извлекаем user_id из токена
        data = request.get_json()
        section = data.get('section')
        subsection = data.get('subsection')
        criticality = data.get('criticality')
        project_id = ObjectId(data.get('project_id'))

        #Проверка подлености клиента
        if not check_project_owner(user_id, project_id):
            return jsonify({"status": "error", "message": "Unauthorized access"}), 403

        if not section or not subsection or not criticality:
            return jsonify({"message": "Missing data"}), 400

        # Обновление критичности в проекте
        result = app.db.projects.update_one(
            {"_id": project_id, "user_id": user_id},
            {"$set": {f"sections.{section}.{subsection}.criticality": criticality}}
        )

        if result.modified_count == 1:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"message": "Failed to update criticality"}), 400


    #Переключение на проект в главное странице нажатие на имя проекта
    @app.route("/api/EditProject/<string:project_id>", methods=["POST"])
    @requires_auth
    def edit_project(project_id,supports_credentials=True):
        user_id = request.user.get('sub')

        #Проверка подлености клиента
        if not check_project_owner(user_id, project_id):
            return jsonify({"status": "error", "message": "Unauthorized access"}), 403

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


    @app.route("/EditProject/<project_id>", methods=["GET"])
    def get_projectse_edit_project(project_id,supports_credentials=True):
        return render_template("index.html")


    #Дабовление и удаление записей в разделах 
    @app.route("/edit_project/<project_id>/add_step", methods=["POST"])
    @requires_auth
    def add_step(project_id):
        user_id = request.user.get('sub')

        #Проверка подлености клиента
        if not check_project_owner(user_id, project_id):
            return jsonify({"status": "error", "message": "Unauthorized access"}), 403
        
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

    
    #вОЗМОЖНО НЕ НУЖНО!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    @app.route('/view_project_report/<filename>', methods=['GET'])
    def view_project_report(filename):
        file_path = os.path.join('static', 'pdfs', filename)
        if not os.path.isfile(file_path):
            return jsonify({"message": "File not found"}), 404
        return send_file(file_path, as_attachment=False)
    

    #Добавление изображения в основные подразделы (нужно переделать)-----------------------------------------
    @app.route('/edit_project/<project_id>/add_imagestandard', methods=['POST'])
    @requires_auth
    def add_imagestandard(project_id):
        user_id = request.user.get('sub')

        #Проверка подлености клиента
        if not check_project_owner(user_id, project_id):
            return jsonify({"status": "error", "message": "Unauthorized access"}), 403
        

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
    @requires_auth
    def remove_image(project_id):
        user_id = request.user.get('sub')

        #Проверка подлености клиента
        if not check_project_owner(user_id, project_id):
            return jsonify({"status": "error", "message": "Unauthorized access"}), 403
        

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
    @requires_auth
    def remove_step(project_id):
        user_id = request.user.get('sub')

        #Проверка подлености клиента
        if not check_project_owner(user_id, project_id):
            return jsonify({"status": "error", "message": "Unauthorized access"}), 403
        

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


    #----------------------------------------------------------------
    #Добавление раздела
    @app.route("/edit_project/<project_id>/add_section", methods=["POST"])
    @requires_auth
    def add_section(project_id):
        user_id = request.user.get('sub')

        #Проверка подлености клиента
        if not check_project_owner(user_id, project_id):
            return jsonify({"status": "error", "message": "Unauthorized access"}), 403
        

        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return "Invalid project_id", 400

        section_name = request.form.get("section_name")

        try:
            result = app.db.projects.update_one(
                {"_id": project_id},
                {"$set": {f"sections.{section_name}": {}}}
            )
            if result.modified_count == 0:
                return "Project not found", 404
        except Exception as e:
            print("Error:", e)
            return "An error occurred", 500
        updated_project = app.db.projects.find_one({"_id": project_id})
        updated_project['_id'] = str(updated_project['_id'])
        
        return jsonify({"status": "success", "message": "Section added successfully", "updated_project": updated_project})


    #Добавление подраздела
    @app.route("/edit_project/<project_id>/add_subsection", methods=["POST"])
    @requires_auth
    def add_subsection(project_id):
        user_id = request.user.get('sub')

        #Проверка подлености клиента
        if not check_project_owner(user_id, project_id):
            return jsonify({"status": "error", "message": "Unauthorized access"}), 403
        

        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return jsonify({"status": "error", "message": "Invalid project_id"}), 400

        data = request.json
        section_name = data.get("section_name")
        subsection_name = data.get("subsection_name")
        print(section_name,subsection_name)

        if not section_name or not subsection_name:
            return jsonify({"status": "error", "message": "Section name and Subsection name are required"}), 400

        try:
            # Добавляем новый подраздел в выбранный раздел
            result = app.db.projects.update_one(
                {"_id": project_id},
                {"$set": {f"sections.{section_name}.{subsection_name}": {"images": [], "steps": []}}}
            )
            if result.modified_count == 0:
                return jsonify({"status": "error", "message": "Project or section not found"}), 404
        except Exception as e:
            print("Error:", e)
            return jsonify({"status": "error", "message": "An error occurred during subsection addition"}), 500

        updated_project = app.db.projects.find_one({"_id": project_id})
        updated_project['_id'] = str(updated_project['_id'])
        
        return jsonify({"status": "success", "message": "Subsection added successfully", "updated_project": updated_project})
    

    #чат джипити
    @app.route('/edit_project/<project_id>/get-gpt-recommendations', methods=['POST'])
    @requires_auth
    def get_gpt_recommendations(project_id):
        user_id = request.user.get('sub')

        #Проверка подлености клиента
        if not check_project_owner(user_id, project_id):
            return jsonify({"status": "error", "message": "Unauthorized access"}), 403
        
        data = request.json
        section = data['section']
        subsection = data['subsection']
        description = data['step_description']
        prompt = f"part of the ship was inspected {section}, namely, looked around{subsection}. in short then {description}"

        try:
            response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant to an employee who inspects yachts, he writes you a brief description of the inspection of a certain part of the ship (let’s assume everything is fine), you need to describe how the inspection was carried out"},
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
            


    @app.route("/api/add_to_showcase", methods=["POST"])
    @requires_auth
    def add_to_showcase():
        user_id = request.user.get('sub')  # Извлекаем user_id из токена
        data = request.get_json()
        project_id = ObjectId(data.get('project_id'))
        price = data.get('price')

        #Проверка подлености клиента
        if not check_project_owner(user_id, project_id):
            return jsonify({"status": "error", "message": "Unauthorized access"}), 403

        if not project_id or not price:
            return jsonify({"message": "Missing project_id or price"}), 400

        # Извлечение информации о проекте
        project = app.db.projects.find_one({"_id": project_id, "user_id": user_id})
        if not project:
            return jsonify({"message": "Project not found"}), 404

        # Подготовка данных для витрины
        vitrine_data = {
            "vessel_name": project['vessel_name'],
            "gen_info_image": project['sections']['introduction']['gen_info'].get('images', [])[0],
            "user_id": user_id,
            "project_id": project_id,
            "price": price
        }

        # Проверка, существует ли проект уже в витрине
        existing_entry = app.db.vitrine.find_one({"project_id": project_id})
        if existing_entry:
            # Обновление существующей записи
            result = app.db.vitrine.update_one(
                {"project_id": project_id},
                {"$set": vitrine_data}
            )
            if result.modified_count > 0:
                return jsonify({"status": "success", "message": "Project updated in showcase"}), 200
            else:
                return jsonify({"message": "Failed to update project in showcase"}), 400
        else:
            # Добавление новой записи в коллекцию витрины
            result = app.db.vitrine.insert_one(vitrine_data)
            if result.inserted_id:
                return jsonify({"status": "success", "message": "Project added to showcase"}), 200
            else:
                return jsonify({"message": "Failed to add project to showcase"}), 400
        
