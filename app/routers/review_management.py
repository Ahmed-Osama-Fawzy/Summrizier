from flask import render_template, request, jsonify
from app import app, db
from app.models import Review as ReviewDB

@app.route('/Review')
def Review():
    return render_template('clientside/Review.html', Title = "Review")

# Adding New Review
@app.route('/addReview', methods = ['POST'])
def addReview():
    try:
        data = request.get_json()
        name = data.get('name')
        job = data.get('job')
        city = data.get('city')
        rate = float(data.get('rate') or 0)
        phone = data.get('phone') if data.get('phone') else "none"
        email = data.get('email') if data.get('email') else "none"
        message = data.get('message')
        newRecord = ReviewDB(name=name, job=job, city=city, rate=rate, email=email, phone=phone, message=message)
        db.session.add(newRecord)
        db.session.commit()
        return jsonify({"message":"تم إرسال الاطلاع بنجاح, نشكركم علي حسن تعاونكم معنا", "status":"success"}), 201
    
    except Exception as e:
        db.session.rollback()
        print(f"The Error Is: {e}, Can't Add the Review")
        return jsonify({"message":" عذرا لم يتم إرسال الاطلاع بنجاح, من فضلك حاول مره  آخري ", "status":"failed"}), 500

@app.route('/reviewsManagement')
def reviewsManagement():
    allReivews = ReviewDB.query.all()
    return render_template("adminside/reviewsManagement.html", Title="Reviews Management", headerTitle="لوحة التحكم في الآراي", data=allReivews)

# Updating Review Visibility
@app.route('/changeVisibility/<int:id>', methods=['POST'])
def changeVisibility(id):
    try:
        theRecord = ReviewDB.query.get_or_404(id)
        currentState = theRecord.status
        if currentState == "hidden":
            theRecord.status = "show"
        else:
            theRecord.status = "hidden"
        db.session.commit()
        return jsonify({"message":"تم تعديل الشفافية بنجاح", "status":"success"}), 201

    except Exception as e:
        print(f"The Error Is: {e}, Can't Add the Review")
        return jsonify({"message":" عذرا لم بتم تعديل الشفافية بنجاح", "status":"failed"}), 500
    

# Removing Review
@app.route('/removeReview/<int:id>', methods=['POST'])
def removeReview(id):
    try:
        theRecord = ReviewDB.query.get_or_404(id)
        db.session.delete(theRecord)
        db.session.commit()
        return jsonify({"message":"تم حذف الراي بنجاح", "status":"success"}), 201

    except Exception as e:
        print(f"The Error Is: {e}, Can't Remove the Review")
        return jsonify({"message":" عذرا لم يتم حذف الراي بنجاح", "status":"failed"}), 500