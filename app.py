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
    

    @app.route("/api/glav", methods=["GET"])
    def get_projects(supports_credentials=True):
        user_id = request.args.get("user_id")
        print(user_id)
        projects = app.db.projects.find({"user_id": user_id})
        projects_list = convert_projects_to_list(projects)
        return jsonify({"status": "success", "user_id": str(user_id), "projects": projects_list})
    

    @app.route("/glav", methods=["GET"])
    def get_projectse(supports_credentials=True):
            return render_template("index.html")
    

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
    @app.route("/api/EditProject/<string:project_id>", methods=["POST"])
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
    
    @app.route("/EditProject/<project_id>", methods=["GET"])
    def get_projectse_edit_project(project_id,supports_credentials=True):
        return render_template("index.html")

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
    def add_subsection(project_id):
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
    def get_gpt_recommendations(project_id):
        data = request.json
        section = data['section']
        subsection = data['subsection']
        description = data['step_description']
        prompt = f"был проведен осмотр части корабля {section}, а именно осматривалась {subsection}. если в крации то {description}"

        try:
            response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты помощник работника который осмотривает яхты он тебе пишет краткое описание осмотра определенной части коробля тебе нужно расписать как проводился осмотр"},
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
            

    if __name__ == "__main__":
        app.run(debug=True)
    
    return app
