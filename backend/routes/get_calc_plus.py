from flask import request, send_file, after_this_request, current_app, Blueprint
import os
from services.process_sheet import stylize_sheet, change_values

route_calc = Blueprint('calc', __name__)

@route_calc.route('/get_calc', methods=['POST']) # type: ignore
def process_and_send_file():
    request_data = request.get_json()
    
    stylize_sheet(request_data['uploadedFile'])
    change_values(request_data)
    
    @after_this_request
    def remove_file(response):
        try:
            file_path = os.path.join(current_app.config.get('UPLOAD_FOLDER', 'somefile.txt'), request_data['uploadedFile'])
            os.remove(file_path)
        except Exception as e:
            print(f"Error removing or cleaning up file: {e}")
        return response

    file_path = os.path.join(current_app.config.get('UPLOAD_FOLDER', 'somefile.txt'), request_data['uploadedFile'])
    return send_file(file_path, as_attachment=True)