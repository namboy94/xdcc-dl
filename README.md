# XDCC Downloader

An XDCC File downloader based on the [irclib](https://github.com/jaraco/irc) framework.

## Installation

### Via Pip (Preferred):

**As User (Preferred)**

    $ pip install xdcc_dl --user
    
**Systemwide**

    # pip install xdcc_dl
    or
    $ sudo pip install xdcc_dl
    
### Via setup.py

**As User (Preferred)**

    $ python setup.py install --user
    
**Systemwide**

    # python setup.py install
    or
    $ sudo python setup.py install
    
    
### Binaries

The supplied binaries at the [Github Releases](https://github.com/namboy94/xdcc-downloader/releases) page
do not require installation nor any dependencies. They can simply be executed.


## Usage

### Message-based CLI

XDCC Packlists usually list xdcc commands in the folowing form:

    /msg <BOTNAME> xdcc send #<PACKNUMBER>
    
By supplying this message as the ```-m``` parameter, the pack can be downloaded.

**Example:**

    # This is the xdcc message:  /msg the_bot xdcc send #1
    
    # This command downloads pack 1 from the_bot
    xdcc_dl -m "/msg the_bot xdcc send #1"
    
    # It's possible to download a range of packs (1-10 in this case):
    xdcc_dl -m "/msg the_bot xdcc send #1-10"
    
    # you can also specify the destination file or directory:
    xdcc_dl -m "/msg the_bot xdcc send #1" -d /home/user/Downloads
    # The destination defaults to your current working directory
    
    # if the bot is on a different server than irc.rizon.net, a server
    # has to be specified:
    xdcc_dl -m "/msg the_bot xdcc send #1" --server irc.freenode.org
    
    # You can also specify an IRC username. If none was supplied, a
    # random string of numbers will be used instead
    xdcc_dl -m "/msg the_bot xdcc send #1" --user Me
    
 
## Further Information

[Documentation(HTML)](https://docs.namibsun.net/html_docs/xdcc-downloader/index.html)

[Documentation(PDF)](https://docs.namibsun.net/pdf_docs/xdcc-downloader.pdf)

[Python Package Index Site](https://pypi.python.org/pypi/xdcc_dl)

[Git Statistics (gitstats)](https://gitstats.namibsun.net/gitstats/xdcc-downloader/index.html)

[Git Statistics (git_stats)](https://gitstats.namibsun.net/git_stats/xdcc-downloader/index.html)

[Changelog](https://gitlab.namibsun.net/namboy94/xdcc-downloader/raw/master/CHANGELOG)