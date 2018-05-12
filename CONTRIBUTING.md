# Contributing to xdcc-dl

## Copyright and Management

The original author, Hermann Krumrey, has the absolute authority on the management
of this project and may steer the development process as he sees fit.

Contributions will be attributed to the author of said code and the copyright will
remain the author's.

## Coding guidelines

**Testing**

Due to the nature of this project, testing is rather complicated. Small unit
tests for the offline components should be implemented, however the online
components may prove to be too cumbersome to test. To test those, a complete
server infrastructure would be required.

**Style**

We feel that a unified coding style is important, which is why we require a linter to
be used. In this case **pycodestyle** is used. Code must pass `pycodestyle`'s tests.

**Documentation**

We use sphinx-autodoc to create automated documentation from docstring comments. As a result, all
classes, methods and class/instance variables should be described using docstring comments.

Hard to understand parts of code within a method should always be commented
accordingly.

## Contributing

All active development is done on a [self-hosted Gitlab server](https://gitlab.namibsun.net).
To contribute, send an email to hermann@krumreyh.com to create an account. Once you have an
account, you may issue a merge or pull request.

Using the Gitlab issue tracker is preferred, but the issues on Github are also
taken into consideration.
