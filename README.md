SVG2Code
========

Combines one or multiple SVG files into a class containing drawing methods using bezier curves to
enable smooth curves drawing no matter the size. It also generates methods to create images of whatever size.

I decided to create this project because I needed complete control of the code generation.


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

    # [-o --output] To choose a different output filename
    $ svg2code -o <output> <files_or_directories>
    $ svg2code -o ScalableImages.swift .

    # [-c --class-name] To choose a different class name
    $ svg2code -o <output> -c <class_name> <files_or_directories>
    $ svg2code -o ScalableImages.swift -c ScalableImages *

    # [--tabs] To use tabs instead of spaces (4)
    $ svg2code --tabs .
    $ svg2code -o ScalableImages.swift --tabs .

    # [-s --spaces N] To choose number of spaces used in indentation 
    $ svg2code -s <number_of_spaces>
    $ svg2code -s 2 -o ScalableImages.swift ~/Documents/AwesomeSVGS

    # [--stdout] Send output to stdout
    $ svg2code --stdout ~/Documents/svgs
    $ svg2code --stdout -s 2 .

    # It is also possible to pipe into it
    $ cat <svg_file> | svg2code -o <output> <files_or_directories>
    $ cat ~/Desktop/Logo.svg | python svg2code/cli.py --stdout -s 2
```


Example
-------

Given the command `cat rect.svg | svg2code --stdout -s 2`

```xml
    <!-- rect.svg -->
    <svg width="200" height="200">
      <rect x="50" y="50" width="100" height="100" 
        style="fill:rgb(0,0,255);stroke-width:3;stroke:rgb(255,0,0)" />
    </svg>
```

it produces the following output

```swift
    import UIKit

    class SVGDrawablesKit {
      static func imageOfPath(withSize size: CGSize, opaque: Bool = false) -> UIImage {
        return image(withSize: size, opaque: opaque, drawingMethod: drawPath)
      }

      static func drawPath(inRect target: CGRect = CGRect(x: 0, y: 0, width: 200, height: 200)) {
        let frame = CGRect(x: 0, y: 0, width: 200, height: 200)

        let context = UIGraphicsGetCurrentContext()!
        context.saveGState()
        context.concatenate(SVGDrawablesKit.transformToFit(rect: frame, inRect: target))

        let path1 = UIBezierPath()
        path1.move(to: CGPoint(x: 50.000000, y: 50.000000))
        path1.addLine(to: CGPoint(x: 150.000000, y: 50.000000))
        path1.addLine(to: CGPoint(x: 150.000000, y: 150.000000))
        path1.addLine(to: CGPoint(x: 50.000000, y: 150.000000))
        path1.close()
        path1.lineWidth = 3
        UIColor(red: 0.0, green: 0.0, blue: 1.0, alpha: 1.0).setFill()
        path1.fill()
        UIColor(red: 1.0, green: 0.0, blue: 0.0, alpha: 1.0).setStroke()
        path1.stroke()

        context.restoreGState()
      }

      static private func image(withSize size: CGSize, opaque: Bool, drawingMethod: (CGRect) -> Void) -> UIImage {
        UIGraphicsBeginImageContextWithOptions(size, opaque, 0.0)

        drawingMethod(CGRect(origin: .zero, size: size))

        let image = UIGraphicsGetImageFromCurrentImageContext()!

        UIGraphicsEndImageContext()

        return image
      }

      static private func transformToFit(rect: CGRect, inRect target: CGRect) -> CGAffineTransform {
        var scale = CGPoint(
          x: abs(target.size.width / rect.size.width),
          y: abs(target.size.height / rect.size.height)
        )

        let tallerThanWider = scale.y < scale.x

        scale.x = min(scale.x, scale.y)
        scale.y = scale.x

        var translate = target.origin
        if tallerThanWider {
          translate.x += 0.5 * (target.size.width - (rect.size.width * scale.x))
        } else {
          translate.y += 0.5 * (target.size.height - (rect.size.height * scale.y))
        }

        let scaleT = CGAffineTransform(scaleX: scale.x, y: scale.y)
        let translateT = CGAffineTransform(translationX: translate.x, y: translate.y)

        return scaleT.concatenating(translateT)
      }
    }
```

```Bash

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
