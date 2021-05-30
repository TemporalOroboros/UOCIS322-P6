from flask import jsonify
from flask_restful import Resource, Api



def format_to_csv(entries):
    """
    Args:
        - entries: 
    """
    key_dict = {}
    for entry in entries:
        for key in entries:
            key_dict[key] = None

    key_list = [key for key in key_dict]
    row_list = key_list.Copy()
    for entry in entries:
        new_row = []
        for key in key_list:
            new_row.append(entry[key])
        row_list.append(new_row)

    return '\n'.join(','.join(row) for row in row_list)

def format_to_json():
    """
    Args:
        - entries: 
    """
    return flask.jsonify(list(entries))


FORMATTERS {
    'csv': format_to_csv,
    'json': format_to_json
}

# '/base/<ret_type>'
class DB_Access(Resource):
    def __init__(self, projection = {}):
        super().__init__()
        self.projection = projection
        self.projection['_id'] = False

    def get(self, ret_type = 'json'):
        """
        Args:
            - self, the resource
            - ret_type: What format the data should be returned in.
        """
        formatter = FORMATTERS.get(ret_type, None)
        if formatter is None:
            logger.debug('Attempted to fetch from database with {} invalid return type'.format(ret_type))
            return "", 501

        max_num = request.args.get('top', self.limit, type=int)
        entries = db.find(projection = self.projection, limit = max_num)
        return formatter(entries)

@api.add_resource(DB_Access, '/listAll')
@api.add_resource(DB_Access, '/listOpenOnly', resource_class_args = [{'_id': False, 'close': False}])
@api.add_resource(DB_Access, '/listCloseOnly', resource_class_args = [{'_id': False, 'open': False}])

