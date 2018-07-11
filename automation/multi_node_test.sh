#!/bin/sh
echo "Starts multi nodes testing..."

/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6 lauchworknode.py --worknode.name=worknode-1 --logger.dir=/usr/local/python/var/logs/worknode-1.log --server.crawler.nodeServer.port=17001 >/dev/null 2>&1 &
/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6 lauchworknode.py --worknode.name=worknode-2 --logger.dir=/usr/local/python/var/logs/worknode-2.log --server.crawler.nodeServer.port=17002 >/dev/null 2>&1 &
/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6 lauchworknode.py --worknode.name=worknode-3 --logger.dir=/usr/local/python/var/logs/worknode-3.log --server.crawler.nodeServer.port=17003 >/dev/null 2>&1 &
/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6 lauchworknode.py --worknode.name=worknode-4 --logger.dir=/usr/local/python/var/logs/worknode-4.log --server.crawler.nodeServer.port=17004 >/dev/null 2>&1 &
/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6 lauchworknode.py --worknode.name=worknode-5 --logger.dir=/usr/local/python/var/logs/worknode-5.log --server.crawler.nodeServer.port=17005 >/dev/null 2>&1 &
/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6 lauchworknode.py --worknode.name=worknode-6 --logger.dir=/usr/local/python/var/logs/worknode-6.log --server.crawler.nodeServer.port=17006 >/dev/null 2>&1 &
/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6 lauchworknode.py --worknode.name=worknode-7 --logger.dir=/usr/local/python/var/logs/worknode-7.log --server.crawler.nodeServer.port=17007 >/dev/null 2>&1 &
/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6 lauchworknode.py --worknode.name=worknode-8 --logger.dir=/usr/local/python/var/logs/worknode-8.log --server.crawler.nodeServer.port=17008 >/dev/null 2>&1 &
/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6 lauchworknode.py --worknode.name=worknode-9 --logger.dir=/usr/local/python/var/logs/worknode-9.log --server.crawler.nodeServer.port=17009 >/dev/null 2>&1 &
/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6 lauchworknode.py --worknode.name=worknode-10 --logger.dir=/usr/local/python/var/logs/worknode-10.log --server.crawler.nodeServer.port=17010 >/dev/null 2>&1 &
