
class Action:
    def __init__(self, attitude, author):
        self.author = author
        self.attitude = attitude


class Comment(Action):
    def __init__(self, attitude, author):
        super().__init__(attitude, author)


class Reaction(Action):
    def __init__(self, attitude, author):
        super().__init__(attitude, author)


class Post(Action):
    def __init__(self, attitude, tags, author):
        super().__init__(attitude, author)
        self.tags = tags
        self.comments = []
        self.reactions = []
        self.shared = []

    def add_comment(self, comment):
        self.comments.append(comment)

    def add_reaction(self, reaction):
        self.reactions.append(reaction)

    def add_shared(self, user):
        self.shared.append(user)

    def share_post(self):
        pass
