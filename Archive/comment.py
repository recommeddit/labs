from collections import namedtuple

Bounds = namedtuple('Bounds', "start end")


class Comment:
    def __init__(self, text, score, url):
        self.text = text
        self.score = score
        self.url = url

    @classmethod
    def from_dict(cls, dict):
        return cls(dict["text"], dict["score"], dict["url"])


class CommentList:
    def __init__(self, comments):
        self.bounds_list = [Bounds(0, 0)] * len(comments)
        self.comments = comments
        self.set_bounds()

    def to_chunked_comments(self, limit=42000):
        next_chunk_start_index = next((i for i, bounds in enumerate(self.bounds_list) if bounds.end >= limit),
                                      None)
        if next_chunk_start_index is None:
            return [ChunkedComment(self.comments)]
        next_chunk = CommentList(self.comments[next_chunk_start_index:])
        return [ChunkedComment(self.comments[0:next_chunk_start_index])] + next_chunk.to_chunked_comments()

    def to_list(self):
        return self.comments

    def set_bounds(self):
        for i, comment in enumerate(self.comments):
            if i == 0:
                offset = 0
            else:
                offset = self.bounds_list[i - 1].end + 2  # we add 2 because there is "\n\n" between comments
            self.bounds_list[i] = Bounds(offset, offset + len(self.comments[i]))


class ChunkedComment:
    def __init__(self, comments):
        self.comments = comments

    def get_raw_text(self):
        text = ""
        for comment in self.comments:
            text += comment.text + "\n\n"

        return text
