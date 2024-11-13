from dataclasses import dataclass


@dataclass
class Submission:
    submission_id: int
    username: str
    challenge_slug: str
    lang: str
    code: str


def save_submissions(submission_list: list[Submission]):
    pass
