[![Coverage Status](https://coveralls.io/repos/github/teamtaverna/slack_integration/badge.svg?branch=master)](https://coveralls.io/github/teamtaverna/slack_integration?branch=master) [![Build Status](https://travis-ci.org/teamtaverna/slack_integration.svg?branch=master)](https://travis-ci.org/teamtaverna/slack_integration)

# Slack Integration
Slackbot for Taverna app, an open source meal review and management platform. More information can be found on the [wiki](https://github.com/teamtaverna/taverna/wiki).

### Tech

Taverna slackbot is written in Python3 and built on [lins05/slackbot](https://github.com/lins05/slackbot) library.

### Collaboration

Want to contribute? Great!

Clone the repository from [GitHub](https://www.github.com)
```
$ git clone https://github.com/teamtaverna/slack_integration.git
```

Taverna slackbot depends on [Taverna Core](https://github.com/teamtaverna/core), its API. You'd need to set up  [Taverna Core](https://github.com/teamtaverna/core) project also in order to work effectively locally.

### Installation

**Mac Users**

Be sure to have the following installed and setup first.
* Python 3

Next,
* Install [Virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/install.html).
* Create a virtual environment for the project.
    ```
    mkvirtualenv <envname>
    ```

* Use the flag `-p python3` if you also have python 2 installed
    ```
    mkvirtualenv -p python3 <envname>
    ```

* Install requirements in the virtual environment created
    ```
    pip install -r requirements.txt
    ```

* Create a `.env` file and copy the contents of `.env.example` file to it.
* Replace
  - `SLACKBOT_API_TOKEN` with an actual slackbot token. Reach out to any of the collaborators for help with that.
  - `X-TAVERNATOKEN ` with an actual taverna core api token. It can be generated from the API section in Core admin.

### Development

To start the bot

```
$ python run.py
```

Watch the bot come online on slack in a few seconds.

To run tests
```
$ python -m unittest discover tests 'test_*.py'
```
