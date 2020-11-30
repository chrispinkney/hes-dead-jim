<p align="center">
  <img src="..\assets\hdj\hdj.gif" alt="He's Dead, Jim" width="738">
</p>

- [What?](#what)
- [Why?](#why)
- [How?](#how)
- [Features](#features)
- [Usage](#usage--installation)
- [Contribution](#contribution)
- [Issues](#issues)
- [License](#license)
- [TODO](https://github.com/chrispinkney/He-s-Dead-Jim/issues)

#### What

He's Dead, Jim is a link checking program, specifically it is a command-line tool for finding and reporting dead links (e.g., broken URLs) in a specified file or website. This tool can be used to help locate broken URLs in an HTML page.

#### How

He's Dead, Jim aggregates (a fancy word for saying _grabs_) all href tags on a single page/file and creates get requests for each link on the page. Those requests are then reported back to the user along with the status code and a delightful colour coded message indicating the status of each link.

#### Why

He's Dead, Jim is a small project developed as part of my introduction to the world of Open Source Development, in addition to Git and GitHub.

This is my project. There are many like it, but this one is mine.

#### Features

He's Dead Jim features the following optional features:

- Colourized output. Good URLs are printed in green, bad URLs are printed in red, and unknown URLs in gray.
- -v can be supplied to the program for current version information.
- Program incorporates multi-threading to allow for parallelization of the program.

#### Usage / Installation

Install [Python](https://www.python.org/downloads/) on your machine (*Be sure to select `Add Python 3.x to PATH` when installing*) and reboot (*optional*):

> Open a shell/cmd and execute the following commands:
>
> `pip install He-s-Dead-Jim`
>
> `hdj`

#### Contribution

Please be sure to read [CONTRIBUTING.md](CONTRIBUTING.md) prior to any development.
Feel free to make a Pull Request or Issue regarding and functionality and I'll get to it ASAP.

#### Issues

Current issues in the projects can be found on the [repo's issues page](https://github.com/chrispinkney/He-s-Dead-Jim/issues).

#### License

MIT License - A short and simple permissive license with conditions only requiring preservation of copyright and license notices. Licensed works, modifications, and larger works may be distributed under different terms and without source code.
