from flask import Flask, jsonify, request
import db_utils
from schemas import *
from models import *
# import exceptions
from marshmallow import exceptions
# from sqlalchemy.orm import exc
from sqlalchemy.exc import IntegrityError
from sqlalchemy import exc

app = Flask(__name__)


@app.route('/api/v1/hello-world-15/')
def hello():
    return 'Hello, World 15'


# MEDICINE
@app.route("/api/v1/medicine", methods=["POST"])
def add_medicine():
    try:
        med_data = MedicineToDo().load(request.json)
        t_med = db_utils.create_entry(Medicine, **med_data)
        return jsonify(MedicineData().dump(t_med))

    except exceptions.ValidationError as err:
        return str(err), 405


@app.route("/api/v1/medicine/<int:medicine_id>", methods=["GET"])
def get_medicine_by_id(medicine_id):
    try:
        medicine = db_utils.get_entry_byid(Medicine, medicine_id)
        return jsonify(MedicineData().dump(medicine)), 200

    except exc.NoResultFound:
        return jsonify({"Error": "Medicine not found"}), 404


@app.route("/api/v1/medicine/<int:medicine_id>", methods=["PUT"])
def upd_medicine_by_id(medicine_id):
    try:
        medicine_data = MedicineToUpdate().load(request.json)
        medicine = db_utils.get_entry_byid(Medicine, medicine_id)
        db_utils.update_entry(medicine, **medicine_data)
        return jsonify({"code": 200})

    except exc.NoResultFound:
        return jsonify({"Error404": "Medicine not found"}), 404

    except exceptions.ValidationError:
        return jsonify({"error405": "Invalid input"}), 405


@app.route("/api/v1/medicine/<int:medicine_id>", methods=["DELETE"])
def delete_medicine_by_id(medicine_id):
    if Session.query(Medicine).filter_by(id=medicine_id).count() == 0:
        return jsonify({"Error": "Medicine not found"}), 404

    try:
        Session.query(MedOrder).filter(MedOrder.medicine_id == medicine_id).delete()
        Session.query(Demand).filter(Demand.medicine_id == medicine_id).delete()
        Session.query(Medicine).filter(Medicine.id == medicine_id).delete()

        Session.commit()
        return jsonify({"Succes": "Medicine deleted"}), 200

    except exc.NoResultFound:
        return jsonify("Error404: Medicine not found"), 404

    except:
        return "something went wrong";


# PHARMACY (ORDER)
@app.route("/api/v1/pharmacy/medorder", methods=["POST"])
def add_order():
    try:
        med_data = MedOrderToDo().load(request.json)
        t_med_ord = db_utils.create_entry(MedOrder, **med_data)
        return jsonify(MedicineData().dump(t_med_ord))

    except exceptions.ValidationError:
        return jsonify({"error": "Invalid input"}), 405

    except IntegrityError as err:
        return str(err), 401


@app.route("/api/v1/pharmacy/medorder/<int:order_id>", methods=["GET"])
def get_order_by_id(order_id):
    try:
        order = db_utils.get_entry_byid(MedOrder, order_id)
        return jsonify(MedOrderData().dump(order)), 200

    except exc.NoResultFound:
        return jsonify({"Error": "Order not found"}), 404


@app.route("/api/v1/pharmacy/medorder/<int:order_id>", methods=["DELETE"])
def delete_order_by_id(order_id):
    if Session.query(MedOrder).filter_by(id=order_id).count() == 0:
        return jsonify({"Error": "Order not found"}), 404

    Session.query(MedOrder).filter_by(id=order_id).delete()
    Session.commit()
    return jsonify({"Succes": "Order deleted"}), 200


@app.route("/api/v1/pharmacy/demand/<int:medicine_id>", methods=["GET"])
def get_demand_by_id(medicine_id):
    try:
        demand = Session.query(Demand).filter_by(medicine_id=medicine_id).one()
        return jsonify(DemandData().dump(demand)), 200

    except exc.NoResultFound:
        return jsonify({"Error": "Demand record not found"}), 404


@app.route("/api/v1/pharmacy/demand/", methods=["POST"])
def add_demand():
    try:
        demand_data = DemandToDo().load(request.json)
        t_demand = db_utils.create_entry(Demand, **demand_data)
        return jsonify(DemandData().dump(t_demand)), 200
    except exceptions.ValidationError:
        return jsonify({"error": "Invalid input"}), 405
    except IntegrityError as err:
        return jsonify({"error": "IntegrityError"}), 401


#not working
@app.route("/api/v1/pharmacy/demand", methods=["DELETE"])
def delete_demand():
    args = request.args
    user_id = args.get('user_id')
    medicine_id = args.get('medicine_id')

    if Session.query(Demand).filter(and_(Demand.user_id == user_id, Demand.medicine_id == medicine_id)).count() == 0:
        return jsonify({"Error": "Demand not found"}), 404

    Session.query(Demand).filter(and_(Demand.user_id == user_id, Demand.medicine_id == medicine_id)).delete()
    Session.commit()
    return "Demand deleted", 200


# USER
@app.route("/api/v1/user", methods=["POST"])
def add_user():
    try:
        user_data = UserToDo().load(request.json)
        t_user = db_utils.create_entry(User, **user_data)
        return jsonify(UserData().dump(t_user)), 200
    except ValidationError as err:
        return str(err), 405


@app.route("/api/v1/user/login", methods=["GET"])
def login_user():
    return "test"


@app.route("/api/v1/user/logout", methods=["GET"])
def logout_user():
    return "test"


@app.route("/api/v1/user/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    try:
        user = db_utils.get_entry_byid(User, user_id)
        return jsonify(UserData().dump(user)), 200
    except exc.NoResultFound:
        return jsonify({"Error": "User not found"}), 404


@app.route("/api/v1/user/<int:user_id>", methods=["PUT"])
def upd_user(user_id):
    # fix swagger
    try:
        user_data = UserToUpdate().load(request.json)
        user = db_utils.get_entry_byid(User, user_id)
        db_utils.update_entry(user, **user_data)
        return jsonify({"code": 200})

    except exc.NoResultFound:
        return jsonify({"Error404": "User not found"}), 404

    except exceptions.ValidationError:
        return jsonify({"error405": "Invalid input"}), 405


@app.route("/api/v1/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if Session.query(User).filter_by(id=user_id).count() == 0:
        return jsonify({"Error": "User not found"}), 404

    try:
        Session.query(MedOrder).filter(MedOrder.user_id == user_id).delete()
        Session.query(Demand).filter(Demand.user_id == user_id).delete()
        Session.query(User).filter(User.id == user_id).delete()

        Session.commit()
        return jsonify({"Succes": "User deleted"}), 200

    except exc.NoResultFound:
        return jsonify("Error404: Medicine not found"), 404

    except:
        return "something went wrong";


if __name__ == '__main__':
    app.run(debug=True)
