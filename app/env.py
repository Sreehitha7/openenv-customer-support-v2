import random
from app.tasks import TASKS
from app.graders import grade_response

class CustomerSupportEnv:
    def __init__(self):
        self.task = None
        self.done = False

    def reset(self):
        self.task = random.choice(TASKS)
        self.done = False
        return self.state()

    def state(self):
        return {
            "ticket": self.task["input"],
            "difficulty": self.task["difficulty"]
        }

    def step(self, action):
        if self.done:
            return self.state(), 0.0, True

        reward = grade_response(self.task, action)

        if reward >= 0.8:
            self.done = True

        return self.state(), reward, self.done