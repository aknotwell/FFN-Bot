import praw, os, requests, json
from bs4 import BeautifulSoup

print('Startup succesful!')
# Reddit API Login 
reddit = praw.Reddit(client_id= os.getenv('client_id'),
                        client_secret= os.getenv('client_secret'),
                        username= os.getenv('username'),
                        password= os.getenv('password'),
                        user_agent= os.getenv('user_agent'))

subreddit = reddit.subreddit('FFNbot_Test')

keyphrase = 'linkffn('

api_url =  "https://fichub.net/api/v0/meta"

headers = {
    'User-Agent': 'FFN-bot/0.0.1 @knotti'
}

#Various checks for validity of links etc.
class Checkers:
    def isUsingLinkffn(self, my_link, comment):
        linkffn = "linkffn([{}]".format(my_link)
        return linkffn in comment.body 
    
#Used to Generate comments and make sure only 1 comment per post, unless limit is met. 
class CommentGenarator: 
    print()


#ADD BACK skip_existing = True when TESTING IS DONE 
for comment in subreddit.stream.comments(skip_existing = True): 
    if keyphrase in comment.body:
        print('Keyword found in comment')
        word = comment.body_html.replace(keyphrase, '')
        soup = BeautifulSoup(word, features="html.parser")
        href_list = soup.find_all(href = True)
        for href in href_list:
            link = href.get('href')
            checker = Checkers() 
            if(checker.isUsingLinkffn(link, comment)):
                print("linkffn method call has been found, now checking valid link.")
                params = {
                    'q': link
                }
                response = requests.get(api_url, headers=headers, params=params) 
                fic_data = response.json()
                title = fic_data.get('title')
                if title:

                    print("Valid link, genarating and responding to comment")
                    metadata = fic_data.get('rawExtendedMeta')
                    author = fic_data.get('author')
                    author_url = fic_data.get('authorUrl')
                    description = fic_data.get('description')
                    description = description.replace('<p>', "")
                    description = description.replace('</p>', "")
                    category =  metadata.get('category')
                    rating = metadata.get('rated')
                    words = metadata.get('words')
                    reviews = metadata.get('reviews')
                    published = fic_data.get('created')
                    status = fic_data.get('status')
                    id = metadata.get('id')
                    language = metadata.get('language')
                    genre = metadata.get('genres')
                    print('category: ' + category + '\n rating: ' + rating + '\nwords: ' + words + '\n reviews: ' + reviews + '\npublished: ' + published)
                    print('id: ' + id + '\n language: ' + language + '\n genre: ' + genre)
                    name_link = "[{}]({}) by [{}]({}) \n> {}".format(title,link, author, author_url,description)
                    comment.reply(str(name_link))
                else:
                    github_link= "https://github.com/aknotwell/FFN-bot"
                    comment.reply("Sorry, your link {} was not valid. Think this is a mistake? Make an issue on the github here".format(github_link))
    

