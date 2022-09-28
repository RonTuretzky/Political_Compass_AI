import praw
class Elicitation:
    def __init__(self):
        self._file = open("controversial.txt", "a")
        self._political_opinion = {"Libertarian Right": 0, "Libertarian Left": 0 ,"Authoritarian Left": 0, "Authoritarian Right": 0}
        self.counter = 0
        self.MAX_CMD = 10000

    def run(self):
        secret = ""
        user_agent = "political_comment_scraper"
        client_id= ""
        reddit = praw.Reddit(client_id=client_id, client_secret=secret, user_agent=user_agent)
        ml_subreddit = reddit.subreddit('PoliticalCompassMemes')
        for post in ml_subreddit.controversial(time_filter="all"):
            print(post.title)
            print(self._political_opinion)
            sum_political = sum(self._political_opinion.values())
            print(sum_political)
            if(self.counter >= self.MAX_CMD):
                print('STOP')
                return
            post.comments.replace_more(limit=0)
            comment_queue = post.comments[:]
            while comment_queue:
                comment = comment_queue.pop(0)
                self.commentToTuple(comment)
                comment_queue.extend(comment.replies)
            # post.comments.replace_more(limit=None)
            # for comment in post.comments:
            #     self.commentToTuple(comment)

    def commentToTuple(self, cmd):
        if(cmd):
            political_commend = cmd.body
            political_opinion = self.extractPoliticalOpinion(cmd.author_flair_text)
            if(political_opinion):
                self.counter += 1
                self._political_opinion[political_opinion] += 1
                tuple_opinion = ( political_opinion, political_commend)
                try:
                    self._file.write(str(tuple_opinion))
                    self._file.write("\n")
                except:
                    self.counter -= 1


    def extractPoliticalOpinion(self, text):
        if(text):
            if ":libright:" in text:
                return "Libertarian Right"
            elif ":libleft:" in text:
                return "Libertarian Left"
            elif ":authleft:" in text:
                return "Authoritarian Left"
            elif ":authright:" in text:
                return "Authoritarian Right"
            else:
                return None
