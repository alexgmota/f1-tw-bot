import sys

from Schedule import makeScheduleTweet
from twitterManager import postImageTweet

def actions(opc):
    switch = {
        '1': tweetSchedule()
    }
    return switch.get(opc)

def tweetSchedule():
    txt, img = makeScheduleTweet()
    postImageTweet(txt + "\n\n [Test]", [img])

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(
            '\t Options:\n\n' +
            '\t\t 1. Tweet schedule\n' +
            '\t\t 2. Tweet driver standings\n' +
            '\t\t 3. Tweet constructor standings\n'
        )
        opc = input('\t Select an option: ')
        actions(opc)
