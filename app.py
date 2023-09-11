import os
from flask import Flask, jsonify, request
from deepface import DeepFace
import cv2
import numpy as np

app = Flask(__name__)

CONFIG = {
    "UPLOAD_FOLDER": "static/"
}


@app.route("/")
def index():
    return jsonify({
        "status_code": 200,
        "message": "Success fetching the API",
        "data": None
    }), 200


@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        profile_picture = request.files["profile_picture"]
        verification_picture = request.files["verification_picture"]

        profile_picture_path = os.path.join(
            CONFIG['UPLOAD_FOLDER'], profile_picture.filename)
        profile_picture.save(profile_picture_path)

        image_bytes = verification_picture.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        verification_picture_path = os.path.join(
            CONFIG['UPLOAD_FOLDER'], verification_picture.filename)
        cv2.imwrite(verification_picture_path, img)

        try:
            result = DeepFace.verify(img1_path=profile_picture_path,
                                     img2_path=verification_picture_path,
                                     )
            result['verified'] = bool(result['verified'])
            os.remove(profile_picture_path)
            os.remove(verification_picture_path)

            return jsonify({
                "status_code": 200,
                "message": "Success verify the faces",
                "data": result
            }), 200
        except Exception as e:
            return jsonify({
                "status_code": 400,
                "message": "Failed verify the faces because of {}".format(str(e)),
                "data": None,
            }), 400

    else:
        return jsonify({
            "status_code": 405,
            "message": "Method not allowed",
            "data": None
        }), 405


if __name__ == "__main__":
    app.run(debug=True,
            host="0.0.0.0",
            port=int(os.environ.get("PORT", 8080)))
