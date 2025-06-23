from flask import render_template, jsonify, request
from app import app, db
from app.models import Gallery as GalleryDB
from app.handler.media_handler import MediaHandler 

@app.route("/Gallery")
def Gallery():
    Data = GalleryDB.query.all()
    
    Lenghts = {
        "FullLen":    len(GalleryDB.query.all()),
        "LenWindow":  len(GalleryDB.query.filter(GalleryDB.tag == "Window").all()),
        "LenKitchen": len(GalleryDB.query.filter(GalleryDB.tag == "Kitchen").all()),
        "LenDoor":    len(GalleryDB.query.filter(GalleryDB.tag == "Door").all()),
        "LenShutter": len(GalleryDB.query.filter(GalleryDB.tag == "Shutter").all()),
        "LenCover":   len(GalleryDB.query.filter(GalleryDB.tag == "Cover").all()),
        "LenUnits":   len(GalleryDB.query.filter(GalleryDB.tag == "Units").all()),
        "LenShape":   len(GalleryDB.query.filter(GalleryDB.tag == "Shape").all()),
        "LenSave":    len(GalleryDB.query.filter(GalleryDB.tag == "Save").all()),
    }

    Colors = {
        "Window":"secondary",
        "Door":"secondary",
        "Kitchen":"success",
        "Shutter":"danger",
        "Cover":"warning",
        "Units":"info",
        "Shape":"light",
        "Save":"dark"
    }

    return render_template("clientside/Gallery.html", Title="Gallery", Data=Data, Lenghts=Lenghts, Colors=Colors)


@app.route("/galleryManagement")
def galleryManagement():
    Data = GalleryDB.query.all()
    return render_template("adminside/galleryManagement.html", Title="Gallery Management", Data=Data)


@app.route("/addMedia", methods=["POST"])
def addMedia():
    try:
        file = request.files.get("path")
        tag = request.form.get("tag")
        date = request.form.get("date")
        type = request.form.get("type")
        description = request.form.get("description")
        media = MediaHandler(file, "app/static/assets/Gallery")
        path, name= media.save()
        newRecord = GalleryDB(name=name, tag=tag, date=date, type=type, description=description)
        db.session.add(newRecord)
        db.session.commit()
        return jsonify({"message":"تمم نشر العنصر بنجاح", "status":"success"}), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"message":"لم يتم  نشر العنصر , حاول مرة آخري", "status":"failed"}), 501
        
@app.route("/editMedia", methods=["POST"])
def editMedia():
    try:
        id = request.form.get("id")
        file = request.files.get("path")
        tag = request.form.get("tag")
        date = request.form.get("date")
        type = request.form.get("type")
        description = request.form.get("description")
        selectedRecord = GalleryDB.query.get_or_404(id)
        if file:
            # Delete the old file
            old_media = MediaHandler(file=None, upload_dir="app/static/assets/Gallery")
            old_media.remove(selectedRecord.name)

            # Save the new file
            media = MediaHandler(file, "app/static/assets/Gallery")
            path, name = media.save()
            selectedRecord.name = name
            
        if tag:
            selectedRecord.tag = tag
        if date:
            selectedRecord.date = date
        if type:
            selectedRecord.type = type
        if description:
            selectedRecord.description = description
        db.session.commit()
        return jsonify({"message":"تمم تعديل العنصر بنجاح", "status":"success"}), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"message":"لم يتم  تعديل العنصر , حاول مرة آخري", "status":"failed"}), 501
        
@app.route("/removeMedia", methods=["POST"])
def removeMedia():
    try:
        data = request.get_json()
        id = data.get("id")
        selectedRecord = GalleryDB.query.get_or_404(id)
        name = selectedRecord.name
        media = MediaHandler(file=None, upload_dir="app/static/assets/Gallery")
        media.remove(name)
        db.session.delete(selectedRecord)
        db.session.commit()
        return jsonify({"message":"تمم حذف العنصر بنجاح", "status":"success"}), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"message":"لم يتم  حذف العنصر , حاول مرة آخري", "status":"failed"}), 501