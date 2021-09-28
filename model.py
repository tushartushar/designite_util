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


class ImplSmell:
    def __init__(self, project_name, package_name, type_name, method_name, smell_name, cause, line_no):
        self.project_name = project_name.strip('\n')
        self.package_name = package_name
        self.type_name = type_name
        self.method_name = method_name
        self.smell_name = smell_name
        self.cause = cause.strip('\n')
        self.m_start_line_no = line_no.strip('\n')
        self.matched = False

    def __str__(self):
        return self.project_name + ', ' + self.package_name + ', ' + self.type_name + ', ' + self.method_name + ', ' + self.smell_name + ', ' + self.cause + ', ' + self.m_start_line_no.strip('\n')


class DesignSmell:
    def __init__(self, project_name, package_name, type_name, smell_name, cause):
        self.project_name = project_name.strip('\n')
        self.package_name = package_name
        self.type_name = type_name
        self.smell_name = smell_name
        self.cause = cause.strip('\n')
        self.matched = False

    def __str__(self):
        return self.project_name + ', ' + self.package_name + ', ' + self.type_name + ', ' + self.smell_name + ', ' + self.cause



class ArchSmell:
    def __init__(self, project_name, package_name, smell_name, cause):
        self.project_name = project_name.strip('\n')
        self.package_name = package_name
        self.smell_name = smell_name
        self.cause = cause.strip('\n')
        self.matched = False

    def __str__(self):
        return self.project_name + ', ' + self.package_name + ', ' + self.smell_name + ', ' + self.cause
