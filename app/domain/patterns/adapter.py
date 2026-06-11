# внешняя система 1
class MoodleSystem:
    def enroll_user_to_course(self, student_name: str, course_name: str):
        return f"Moodle: {student_name} enrolled in {course_name}"


# внешняя система 2
class GoogleClassroomSystem:
    def add_student(self, course_name: str, student_name: str):
        return f"Google Classroom: {student_name} added to {course_name}"


# общий интерфейс
class LMSAdapter:
    def enroll(self, student_name: str, course_name: str):
        raise NotImplementedError("Method enroll() must be implemented")


class MoodleAdapter(LMSAdapter):
    def __init__(self, system: MoodleSystem):
        self.system = system

    def enroll(self, student_name: str, course_name: str):
        return self.system.enroll_user_to_course(student_name, course_name)


class GoogleClassroomAdapter(LMSAdapter):
    def __init__(self, system: GoogleClassroomSystem):
        self.system = system

    def enroll(self, student_name: str, course_name: str):
        return self.system.add_student(course_name, student_name)