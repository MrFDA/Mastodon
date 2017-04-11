# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 07:38:36 2017

@author: FDA
"""

from pyquery import PyQuery as pq
from argparse import ArgumentParser

def parseArgs():
    description = 'Get number of follower from an instance'
    parser = ArgumentParser(description=description)
    parser.add_argument('username', help='Full username (with instance)')
    parser.add_argument('instance', help='Instance name')
    parser.add_argument('-l','--list', action='store_true',
                        help='Print follower list')
    return parser.parse_args()    

def get_follow(url):
    page = pq(url)
    users = [e.text for e in page("span.username")]
    return users

def get_next_page(url):
    page = pq(url)
    link = [e.attrib['href'] for e in page("a.next_page")]
    if len(link)>0:
        link = link[0]
    else:
        link = ''
    return link

def get_all_followers(username,srv):    
    url_end = '/users/' + username + '/followers'
    followers = []
    while url_end != '':
        url = 'https://' + srv + url_end
        followers = followers + get_follow(url)
        url_end = get_next_page(url)
    return followers

def main():
    options = parseArgs()
    full_username = options.username
    from_srv = options.instance
    parsed_username = filter(None,full_username.split('@'))
    if len(parsed_username)<2:
        raise ValueError('Please provide the full username, i.e. username@instance')
    elif len(parsed_username)>2:
        raise ValueError("The usernane you provided doesn't have the structure of a username")
    else:
        (username,srv) = parsed_username
    followers = get_all_followers(username,srv)
    if srv==from_srv:
        from_srv_followers = [e+'@'+srv for e in followers if len(e.split('@'))==2]        
    else:
        from_srv_followers = [e for e in followers if e.split('@')[-1]==from_srv]
    nb_followers = len(from_srv_followers)
    print 'Number of accounts following %s on the instance %s: %i'%(full_username,from_srv,nb_followers)
    if options.list:
        print from_srv_followers

if __name__ == '__main__' :
    main()