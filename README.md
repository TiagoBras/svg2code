SVG2Code
========

Combines one or multiple SVG files into a class containing drawing methods using bezier curves to
enable smooth curves drawing no matter the size. It also generates methods to create images of whatever size.

I decided to create this project because I needed to personalized the code generation.


Installation
------------

```Bash
    $ pip install svg2code
```


How it works
------------

```Bash
    # Most simple command, it generates a class named 'SVGDrawablesKit.swift'
    $ svg2code <files_or_directories>
    $ svg2code ~/Desktop/svgs

    # To choose a different output filename
    $ svg2code -o <output> <files_or_directories>
    $ svg2code -o ScalableImages.swift .

    # To choose a different class name
    $ svg2code -o <output> -c <class_name> <files_or_directories>
    $ svg2code -o ScalableImages.swift -c ScalableImages *

    # To use tabs instead of spaces (4)
    $ svg2code --tabs .
    $ svg2code -o ScalableImages.swift --tabs .

    # To choose number of spaces used in indentation 
    $ svg2code -s <number_of_spaces>
    $ svg2code -s 2 -o ScalableImages.swift ~/Documents/AwesomeSVGS

    # Send output to stdout
    $ svg2code --stdout ~/Documents/svgs
    $ svg2code --stdout -s 2 .
```


Notes
-----

At this moment, it only supports Swift code generation.

It doesn't implement the full SVG 1.1 specification either. 

Whenever I find something from the specification that I need I implement it.

I might also accept implementation requests, e.g., if someone needs shadows or gradients support.


License
-------

MIT - Copyright (c) 2017 Tiago Bras