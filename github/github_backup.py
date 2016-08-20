#!/usr/bin/env python2

# Spencer Mathews
# 9/2016
#
# Download GitHub repos for students in DES 157
#
# - authentication may be required to overocome API limits
# - in each repo do 'git checkout gh-pages' since web sites on gh-pages branch 

# reference https://stackoverflow.com/questions/10625190/most-suitable-python-library-for-github-api-v3

import os
import requests
import json
import subprocess  # use subprocess32 (backport of py3 subprocess)for more involved things

# read file of github usernames (one per line)
try:
    usernames = open('github_usernames').read().splitlines()
except IOError:
    print 'Failed to read github_usernames'


for username in usernames:

    print '\n**********', username, '**********'
    try:
        os.mkdir(username)
    except OSError:
        print 'Directory', username, 'already exists!'

    # get user's repo list
    # may need to authenticate using personal access token, or otherwise
    # postman constructed authorization header from username/pass {'authorization' : "Basic XXX"} 
    r = requests.get('https://api.github.com/users/'+username+'/repos')
    if(r.ok):
        # load repos json into python as list of dict
        repos_list = json.loads(r.text or r.content)
        for repo_dict in repos_list:
            repo = repo_dict['name']
            print '\n', repo, '/ ~', repo_dict['size']/1000, 'MB'
            subprocess.call(['git', 'clone', repo_dict['clone_url']], cwd=username)
            #subprocess.call(['git', 'clone', '--depth=1', '--no-single-branch', repo_dict['clone_url']], cwd=username)
    else:
        print 'GitHub API request failed!'