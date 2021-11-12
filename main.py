from typing import Any
from crud import UserCRUD
from flask import Flask, jsonify, request

app = Flask("__name__")

user = UserCRUD("data.json")


@app.route("/", methods=["VIEW"])
def get_all_users():
    return jsonify(user.get_all_users())


@app.route("/", methods=["POST"])
def create_new_user():
    new_user: dict[str, Any] = request.json  # type: ignore

    # TODO Validation

    if user.get_item(new_user["login"]) is not None:
        return jsonify({"info": "User with such name already exists"}), 403
    user.set_item(new_user["login"], {"password": new_user["password"]})
    user.write_to_file()

    return jsonify({"info": "success"})


@app.route("/", methods=["DELETE"])
def delete_user():
    user_to_delete: dict[str, Any] = request.json  # type: ignore

    # TODO Validation

    if user.get_item(user_to_delete["login"]) is None:
        return jsonify({"info": "There is no such user"}), 403
    user.delete_item(user_to_delete["login"])
    user.write_to_file()
    return jsonify({"info": "Complete"})


@app.route("/", methods=["PATCH"])
def change_password():
    new_user: dict[str, Any] = request.json  # type: ignore

    # TODO Validation

    if user.get_item(new_user["login"]) is None:
        return jsonify({"info": "Where is no such user"}), 403
    user.delete_item(new_user["login"])
    user.write_to_file()
    user.set_item(new_user["login"], {"password": new_user["password"]})
    user.write_to_file()

    return jsonify({"info": "success"})


@app.route("/", methods=["PUT"])
def check_password():
    new_user: dict[str, Any] = request.json  # type: ignore

    # TODO Validation

    if user.get_item(new_user["login"]) is None:
        return jsonify({"info": "Where is no such user"}), 403

    return jsonify({"info": "success login and password"})


if __name__ == "__main__":
    app.run(debug=True)
