import praw
import nltk
from textblob import TextBlob


class Elicitation:
    def __init__(self):
        self._file = open("uniqueDB.txt", "a",encoding="utf-8")
        self._fileHot = open("HotPosts.txt", "a",encoding="utf-8")
        self._fileNew = open("NewPosts.txt", "a",encoding="utf-8")
        self._fileTop = open("TopPosts.txt", "a",encoding="utf-8")

        self._political_opinion = {"Libertarian Right": 0, "Libertarian Left": 0 ,"Authoritarian Left": 0, "Authoritarian Right": 0,
                                   "Centrist" : 0, "Authoritarian Center" : 0, "Left" : 0, "Right" : 0, "Libertarian Center" : 0}
        self.counter = 0
        self.MAX_CMD = 100000
        self.DataHot = set()
        self.DataNew = set()
        self.DataTop = set()



    def run(self , sort ):
        secret = "W2psD3CqQ8h12jzEotTe_SFpQQLWQA"
        user_agent = "political_comment_scraper"
        client_id= "rNjUJWa3Rim3KwuhYlfrSA"
        reddit = praw.Reddit(client_id=client_id, client_secret=secret, user_agent=user_agent)
        ml_subreddit = reddit.subreddit('PoliticalCompassMemes')

        if sort == "hot" :
            posts = ml_subreddit.hot()
            self.Create_DataBase(self.DataHot , self._fileHot ,posts )
        elif sort == "new" :
            posts = ml_subreddit.new()
            self.Create_DataBase(self.DataNew , self._fileNew ,posts )
        elif sort == "top":
            posts = ml_subreddit.top()
            self.Create_DataBase(self.DataTop , self._fileTop ,posts )



    def Create_DataBase(self, Data , File , Posts):

        for post in Posts:
            print(post.title)
            print(self._political_opinion)
            sum_political = sum(self._political_opinion.values())
            print(sum_political)
            if(self.counter >= self.MAX_CMD):
                print('STOP')
                return
            post.comments.replace_more(limit=100)
            comment_queue = post.comments[:]
            while comment_queue:
                comment = comment_queue.pop(0)
                tuple_opinion = self.commentToTuple(comment)
                if (tuple_opinion != -1) : # if we don't have problems
                    Data.add(tuple_opinion)
                # comment_queue.extend(comment.replies)
            # post.comments.replace_more(limit=None)
            # for comment in post.comments:
            #     self.commentToTuple(comment)

            # after we get all the opinions we want to write this to the file (data base)
            print(f"{Data} : {len (Data)}")

    def Set_To_File(self):
        # make a set wich contains all the data from Hot/New/Top
        uniqe =( (self.DataHot).union(self.DataNew)  ).union(self.DataTop)
        all_opinions = [str(i) for i in uniqe]
        # write all tje ploitical opinions to file
        for i in range(len(all_opinions)):
            # print(f"all_opinions[{i}] ::\n", all_opinions[i])
            (self._file).write(all_opinions[i] + "\n")




    def commentToTuple(self, cmd):
        if(cmd):
            political_commend = cmd.body
            political_opinion = self.extractPoliticalOpinion(cmd.author_flair_text)
            if(political_opinion):
                self.counter += 1
                self._political_opinion[political_opinion] += 1
                try :
                    grammerScore = self.cal_grammar_score(political_commend)
                    Sentiment = self.sentiment(political_commend)
                    tuple_opinion = ( political_opinion, political_commend, len(political_commend),grammerScore,Sentiment)
                    print(tuple_opinion)
                    return  tuple_opinion

                except Exception as E :
                    return E


                """
                try:
                    #if str(political_opinion) == "Authoritarian Left" and tuple_opinion not in self._file:
                    if not self.CheckDuplicate(tuple_opinion) :
                        self._file.write(str(tuple_opinion))
                        self._file.write("\n")
                except:
                    self.counter -= 1
                """

        return -1


    def text_to_sentences(self,__text):
        import re
        return re.split("[\.\?\!]", __text)


    def cal_grammar_score(self,text):
        import language_tool_python
        tool = language_tool_python.LanguageTool('en-US')
        count_errors = 0
        processed = self.text_to_sentences(text)
        for sentence in processed:
            matches = tool.check(sentence)
            count_errors += len(matches)
        return count_errors

    def sentiment(self ,sentence):
        """
        :param sentence:
        :return: if a sentence is good or bad
        minus - bad sentence
        plus - good sentence
        """
        blob = TextBlob(sentence)
        return blob.sentiment.polarity

    def extractPoliticalOpinion(self, text):
        #TODO add all political types
        if(text):
            if ":libright:" in text:
                return "Libertarian Right"
            elif ":libleft:" in text:
                return "Libertarian Left"
            elif ":authleft:" in text:
                
                return "Authoritarian Left"
            elif ":authright:" in text:
                return "Authoritarian Right"
            elif ":centrist:" in text:
                return "Centrist"
            elif ":authcenter:" in text:
                return "Authoritarian Center"
            elif ":left:" in text:
                return "Left"
            elif ":right:" in text:
                return "Right"
            elif ":libcenter:" in text:
                return "Libertarian Center"
            else:
                return None


    def CheckDuplicate(self, tuple_opinion):
        """
        :param tuple_opinion:
        :return:
        check if tuple_opinion already exists if yes return True
        """
        try :
            lines = [ line.split("\n")[0] for line in (self._file).readlines() ]
            if tuple_opinion in lines :
                return True
        except :
            quit(f"Can't open file {self._file}")

        return False

