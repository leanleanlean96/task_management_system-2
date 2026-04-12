class TaskError(Exception):
    pass


class InvalidTaskData(TaskError):
    pass


class InvalidTaskFieldValue(TaskError):
    pass


class AccessPermitted(Exception):
    pass
