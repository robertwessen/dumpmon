from Queue import Queue
import requests
import time
import re
from pymongo import MongoClient
from requests import ConnectionError
from twitter import TwitterError
from settings import USE_DB, DB_HOST, DB_PORT
import logging
import helper


class Site(object):
    '''
    Site - parent class used for a generic
    'Queue' structure with a few helper methods
    and features. Implements the following methods:

            empty() - Is the Queue empty
            get(): Get the next item in the queue
            put(item): Puts an item in the queue
            tail(): Shows the last item in the queue
            peek(): Shows the next item in the queue
            length(): Returns the length of the queue
            clear(): Clears the queue
            list(): Lists the contents of the Queue
            download(url): Returns the content from the URL

    '''
    # I would have used the built-in queue, but there is no support for a peek() method
    # that I could find... So, I decided to implement my own queue with a few
    # changes
    def __init__(self, queue=None):
        if queue is None:
            self.queue = []
        if USE_DB:
            # Lazily create the db and collection if not present
            self.db_client = MongoClient(DB_HOST, DB_PORT).paste_db.pastes


    def empty(self):
        return len(self.queue) == 0

    def get(self):
        if not self.empty():
            result = self.queue[0]
            del self.queue[0]
        else:
            result = None
        return result

    def put(self, item):
        self.queue.append(item)

    def peek(self):
        return self.queue[0] if not self.empty() else None

    def tail(self):
        return self.queue[-1] if not self.empty() else None

    def length(self):
        return len(self.queue)

    def clear(self):
        self.queue = []

    def list(self):
        print('\n'.join(url for url in self.queue))

    def monitor(self, bot, t_lock):
        self.update()
        while(1):
            while not self.empty():
                paste = self.get()
                self.ref_id = paste.id
                logging.info('[*] Checking ' + paste.url)
                paste.text = self.get_paste_text(paste)
                tweet = helper.build_tweet(paste)
                if tweet:
                    logging.info(tweet)
                    with t_lock:
                        if USE_DB:
                            self.db_client.save({
                                'pid' : paste.id,
                                'text' : paste.text,
                                'emails' : paste.emails,
                                'hashes' : paste.hashes,
                                'num_emails' : paste.num_emails,
                                'num_hashes' : paste.num_hashes,
                                'type' : paste.type,
                                'db_keywords' : paste.db_keywords,
                                'url' : paste.url
                               })
                        try:
                            bot.statuses.update(status=tweet)
                        except TwitterError:
                            pass
                        # hackish attempt to cobble in a RSS feed output without changing much else
                        #try:
                        #    bot.RSS2.blahblah.invokeRSSupdate(tweet)
                        #except
                        #    pass
            self.update()
            while self.empty():
                logging.debug('[*] No results... sleeping')
                time.sleep(self.sleep)
                self.update()
