from flask import Flask, render_template, request, redirect, url_for, session,jsonify,abort
from pymongo import MongoClient
from passlib.hash import bcrypt
from bson import ObjectId
from datetime import datetime
from dotenv import load_dotenv
from flask_cors import CORS,cross_origin
import secrets

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
            "sections": [],
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


    #Дабовление и удаление записей в стандартные разделы разделах
    @app.route("/edit_project/<project_id>/add_step_standard", methods=["POST"])
    def add_step_standard(project_id):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return jsonify({"status": "error", "message": "Invalid project_id"}), 400
        
        section_name = request.form.get("section_name")
        step_description = request.form.get("step_description")

        # Добавьте ваш код для обработки данных и добавления шага в соответствующий подраздел
        print(section_name,step_description)

        return jsonify({"status": "success", "message": "Step added successfully","step_description": step_description,"section_name": section_name,})
        
    #Дабовление и удаление записей в разделах
    @app.route("/edit_project/<project_id>/add_step", methods=["POST"])
    def add_step(project_id):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return jsonify({"status": "error", "message": "Invalid project_id"}), 400

        step_description = request.form.get("step_description")
        section = request.form.get("section")

        section_field = f"{section}_steps"

        try:
            result = app.db.projects.update_one(
                {"_id": project_id},
                {"$push": {section_field: step_description}}
            )
            if result.modified_count == 0:
                return jsonify({"status": "error", "message": "Project not found"}), 404
        except Exception as e:
            print("Error:", e)
            return jsonify({"status": "error", "message": "An error occurred"}), 500
        
        # Получите обновленный проект после добавления шага
        updated_project = app.db.projects.find_one({"_id": project_id})

        # Преобразуйте ObjectId в строку перед возвратом ответа JSON
        updated_project["_id"] = str(updated_project["_id"])

        print("Вот твоя поебота!!!!!!!!!!!!!!!!",updated_project)

        return jsonify({"status": "success", "message": "Step added successfully","updated_project": updated_project})

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
                {"_id": project_id, "sections.name": section_name},
                {"$push": {"sections.$.subsections.$[s].cells": {"description": step_description}}},
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
                {"$push": {"sections": {"name": section_name, "subsections": []}}}
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
                {"_id": project_id, "sections.name": section_name},
                {"$push": {"sections.$.subsections": {"name": subsection_name, "cells": []}}}
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

        print(section_name, subsection_name)
        
        try:
            result = app.db.projects.update_one(
                {"_id": project_id},
                {"$push": {section_name: {"name": subsection_name, "subsections": []}}}
            )
            if result.modified_count == 0:
                return "Section not found in the project", 404
        except Exception as e:
            print("Error:", e)
            return "An error occurred", 500
        
        updated_project = app.db.projects.find_one({"_id": project_id})
        updated_project['_id'] = str(updated_project['_id'])

        return jsonify({"status": "success", "message": "Hello bithes", "project": updated_project})

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
