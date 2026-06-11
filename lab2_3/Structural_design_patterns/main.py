from adapter import ExternalAPI, APIAdapter
from decorator import BasicUserProfile, AvatarDecorator, StatusDecorator, RoleDecorator
from facade import CourseCreationFacade
from proxy import CertificateProxy


def run_adapter():
    print("\n=== Adapter ===")

    api = ExternalAPI()
    data_source = APIAdapter(api)

    print(data_source.get_data())


def run_decorator():
    print("\n=== Decorator ===")

    profile = BasicUserProfile(
        username="andrei",
        email="andrei@example.com"
    )

    profile = AvatarDecorator(profile, "avatar.png")
    profile = StatusDecorator(profile, "Online")
    profile = RoleDecorator(profile, "Student")

    print(profile.get_info())


def run_facade():
    print("\n=== Facade ===")

    facade = CourseCreationFacade()

    print(facade.create_full_course("Python Basics"))


def run_proxy():
    print("\n=== Proxy ===")

    certificate1 = CertificateProxy(
        username="Andrei",
        course_title="Python Basics",
        course_completed=False
    )

    print(certificate1.download())

    certificate2 = CertificateProxy(
        username="Maria",
        course_title="Python Basics",
        course_completed=True
    )

    print(certificate2.download())


if __name__ == "__main__":
    run_adapter()
    run_decorator()
    run_facade()
    run_proxy()