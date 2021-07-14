class Type:
    def __init__(self, project_name, package_name, type_name, file_path, start_line_no):
        self.project_name = project_name
        self.package_name = package_name
        self.type_name = type_name
        self.file_path = file_path
        self.start_line_no = start_line_no


class Method:
    def __init__(self, project_name, package_name, type_name, method_name, start_line_no):
        self.project_name = project_name
        self.package_name = package_name
        self.type_name = type_name
        self.method_name = method_name
        self.start_line_no = start_line_no