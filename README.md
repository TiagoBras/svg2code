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
    $ svg2code -o SVGIcons.swift .

    # [-c --class-name] To choose a different class name
    $ svg2code -o <output> -c <class_name> <files_or_directories>
    $ svg2code -o SVGIcons.swift -c ScalableIcons *

    # [--author] Set author's name
    $ svg2code -o <output> --author <author_name> <files_or_directories>
    $ svg2code -o SVGIcons.swift --author "John Smith" *

    # [--project] Set projects's name
    $ svg2code -o <output> --project <project_name> <files_or_directories>
    $ svg2code -o SVGIcons.swift --project AwesomeApp *

    # [--tabs] To use tabs instead of spaces (4)
    $ svg2code --tabs .
    $ svg2code -o SVGIcons.swift --tabs .

    # [-s --spaces N] To choose number of spaces used in indentation 
    $ svg2code -s <number_of_spaces>
    $ svg2code -s 2 -o SVGIcons.swift ~/Documents/AwesomeSVGS

    # [--stdout] Send output to stdout
    $ svg2code --stdout ~/Documents/svgs
    $ svg2code --stdout -s 2 .

    # It is also possible to pipe into it
    $ cat <svg_file> | svg2code -o <output> <files_or_directories>
    $ cat ~/Desktop/Logo.svg | python svg2code/cli.py --stdout -s 2
```


Example
-------

Given the command `cat rect.svg | svg2code -s 2 -c SVGIcons --author James --project MobileApp --stdout
`

```xml
    <!-- rect.svg -->
    <svg width="200" height="200">
      <rect x="50" y="50" width="100" height="100" 
        style="fill:rgb(0,0,255);stroke-width:3;stroke:rgb(255,0,0)" />
    </svg>
```

it produces the following output

```swift
    //
    //  SVGIcons.swift
    //  MobileApp
    //
    //  Created by James on 01/04/2017.
    //  Copyright © 2017 James. All rights reserved.
    //

    import UIKit

    enum SVGIcons {
      case rect

      var size: CGSize {
        switch self {
        case .rect: return CGSize(width: 200.0, height: 200.0)
        }
      }

      var path: UIBezierPath {
        switch self {
        case .rect: return SVGIcons.rectPath1
        }
      }

      func image(withSize size: CGSize, opaque: Bool = false, alignment: Alignment = .center) -> UIImage {
        switch self {
        case .rect: return SVGIcons.image(withSize: size, opaque: opaque, alignment: alignment, drawingMethod: SVGIcons.drawRect)
        }
      }

      func draw(inRect target: CGRect, alignment: Alignment = .center){
        switch self {
        case .rect: return SVGIcons.drawRect(inRect: target, alignment: alignment)
        }
      }

      private static func drawRect(inRect target: CGRect = CGRect(x: 0, y: 0, width: 200.0, height: 200.0), alignment: Alignment = .center) {
        let frame = CGRect(origin: .zero, size: SVGIcons.rect.size)

        let context = UIGraphicsGetCurrentContext()!
        context.saveGState()
        context.concatenate(SVGIcons.transformToFit(rect: frame, inRect: target, alignment: alignment))
           
        let path1 = SVGIcons.rectPath1
        path1.lineWidth = 3.0
        UIColor(red: 0, green: 0, blue: 1.0, alpha: 1.0).setFill()
        path1.fill()
        UIColor(red: 1.0, green: 0, blue: 0, alpha: 1.0).setStroke()
        path1.stroke()

        context.restoreGState()
      }


      static private func image(withSize size: CGSize, opaque: Bool, alignment: Alignment, drawingMethod: (CGRect, Alignment) -> Void) -> UIImage {
        UIGraphicsBeginImageContextWithOptions(size, opaque, 0.0)

        drawingMethod(CGRect(origin: .zero, size: size), alignment)

        let image = UIGraphicsGetImageFromCurrentImageContext()!

        UIGraphicsEndImageContext()

        return image
      }

      static private func transformToFit(rect: CGRect, inRect target: CGRect, alignment: Alignment = .center) -> CGAffineTransform {
        var scale = CGPoint(
          x: abs(target.size.width / rect.size.width),
          y: abs(target.size.height / rect.size.height)
        )
        
        let widerThanTaller = scale.y < scale.x
        
        scale.x = min(scale.x, scale.y)
        scale.y = scale.x
        
        var translate = target.origin
        
        if widerThanTaller {
          switch alignment {
          case .right: translate.x += rect.size.width * scale.x
          case .center: translate.x += 0.5 * (target.size.width - (rect.size.width * scale.x))
          default: break // it's already aligned to the left margin
          }
        } else {
          switch alignment{
          case .bottom: translate.y += rect.size.height * scale.y
          case .center: translate.y += 0.5 * (target.size.height - (rect.size.height * scale.y))
          default: break // it's already aligned to the top margin
          }
        }
        
        let scaleT = CGAffineTransform(scaleX: scale.x, y: scale.y)
        let translateT = CGAffineTransform(translationX: translate.x, y: translate.y)
        
        return scaleT.concatenating(translateT)
      }

      enum Alignment {
        case center, top, bottom, left, right
      }

      // Paths definitions
      private static let rectPath1: UIBezierPath = {
        let path = UIBezierPath()
        path.move(to: CGPoint(x: 50.0, y: 50.0))
        path.addLine(to: CGPoint(x: 150.0, y: 50.0))
        path.addLine(to: CGPoint(x: 150.0, y: 150.0))
        path.addLine(to: CGPoint(x: 50.0, y: 150.0))
        path.close()
        return path
      }()
    }
```


Notes
-----

At this moment, it only supports Swift code generation.

It doesn't implement the full SVG 1.1 specification. 

Whenever I find something from the specification that I need I implement it.

I might also accept implementation requests, e.g., if someone needs shadows or gradients support.


License
-------

MIT - Copyright (c) 2017 Tiago Bras
