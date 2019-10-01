DEV-CLI
=======

A CLI interface for dev.to

Please note before using that you should put your `API
key <https://docs.dev.to/api/#section/Authentication/api_key>`__ in the
``DEV_API_KEY`` environment variable. If you prefer, when starting the
program will also look for a ``.env`` file in the working directory.

You can get this tool simply by doing a:

::

    pip install dev-cli

Publishing
----------

You can publish a Markdown file directly to dev.to using DEV-CLI. Your
Markdown file must be identical to what you would input directly in the
website's interface.

Something else that you should take in account is the key. Indeed, when
an article is created the API ID isn't retrofitted to the Markdown file
since this would get a little bit messy. Instead, you have several
options to map your local files to your remote articles.

Namely you can use the ``cover_picture``, the ``canonical_url`` or the
``title`` from the front matter. Please note that whatever you chose it
must be set in the front matter, otherwise the program will fail. The
default key is ``canonical_url``, because it won't appear in your source
file unless you know what you're doing.

Please note that you don't have to use the same key every time. Suppose
that you use the ``title`` but want to change it, you can do one sync
with ``cover_picture`` instead of ``title`` as long as you don't change
both at the same time.

To publish using the ``canonical_url``:

::

    python -m dev_cli publish ~/dev/dev-blog/test.md

To publish using another key:

::

    python -m dev_cli publish -k title ~/dev/dev-blog/test.md

In case of conflict the first found article will be updated.
