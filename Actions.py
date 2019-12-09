
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
        self.observers = []

    def add_comment(self, comment):
        # TODO add comment and inform users (who added post, who commented post etc)
        pass

    def add_reaction(self, reaction):
        # TODO add reaction and inform users (who added post, who commented post etc)
        pass

    def share_post(self):
        # TODO just copy (?)
        pass


