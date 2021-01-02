#[ci8.it](http://ci8.it/)

This repo is for my personal site [ci8.it](https://ci8.it/) based on [Bootstrap](https://getbootstrap.com/) 
and use [django-static-sites](https://github.com/ciotto/django-static-sites/) in order to make static files that can be hoasted by [GitHub Pages](https://pages.github.com/).

The dynamic part is in the `sites` folder.

In order to activate the development environment run:

```
> source bin/activate                                                                                                                                                              ~/Documents/Ciotto/ci8.it/ci8.it(master✗)@MBP-18.local
Clean .pyc files...OK
Activate virtualenv...OK

..............######..####..#######......####.########.............
.............##....##..##..##.....##......##.....##................
.............##........##..##.....##......##.....##................
.............##........##...#######.......##.....##................
.............##........##..##.....##......##.....##................
.............##....##..##..##.....##.###..##.....##................
..............######..####..#######..###.####....##................

Welcome to the ci8.it development environment.

ci8.it>
```

For site generation use:

```
ci8.it> python src/make.py
```

For local test use:

```
ci8.it> cd docs
ci8.it> python3 -m http.server
```
