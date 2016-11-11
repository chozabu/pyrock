# PyRock

PyRock is aiming to be a high level authorised decentral networking solution

### unusably early stages

####running

create a venv, activate and install requirements

virtualenv -p python3 env
. env/bin/activate
pip install -r requirements

you can now run main.py with

python main.py

or run two instances with ./testit.sh

###current features

- basic sockets networking backend
- basic HTTP POST networking backend
- machine contacts (from a file)
- start of synclist, high level sync/additive json store
- very basic HTML UI
- start of websockets interface for UI
- start of forums
- instant messenger (broadcast)

###todo

- human contacts
- keypairs
- data storage
- API/IPC/Plugins
- Solidify protocol
- global connection graph
- more alternate network backends
- alternate programming language implementations

###more todo
- blogs
- comics
- file sharing
- virtual LAN
- turtle messaging
- games
- voting
- www
- central nameserver