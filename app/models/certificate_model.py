from dataclasses import dataclass


@dataclass
class CertificateModel:
    id: int
    user_id: int
    course_id: int
    title: str
