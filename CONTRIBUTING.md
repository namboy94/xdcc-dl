# Contributing to xdcc-dl

## Copyright and Management

The original author, Hermann Krumrey, has the absolute authority on the management
of this project and may steer the development process as he sees fit.

Contributions will be attributed to the author of said code and the copyright will
remain the author's.

## Coding guidelines

**Unit Testing**

Code should be unit tested with a near-100% coverage. This may not always be completely
feasible, but at least 90%+ should be targeted. However, Unit tests should not just be
done to achieve a high test coverage, writing useful tests is even more important,
just not as easily measurable.

**Style**

We feel that a unified coding style is important, which is why we require a linter to
be used. In this case **pycodestyle** is used. Code must pass pep8's tests.

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
