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

Given the command and files `svg2code rect.svg circle.svg -s 2 -c SVGIcons --author James --project MobileApp --stdout`

```xml
    <!-- rect.svg -->
    <svg width="200" height="200">
      <rect x="50" y="50" width="100" height="100" 
        style="fill:rgb(0,0,255);stroke-width:3;stroke:rgb(255,0,0)" />
    </svg>
```

```xml
    <!-- circle.svg -->
    <svg height="100" width="100">
      <circle cx="50" cy="50" r="40" stroke="green" stroke-width="3" fill="red" />
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
      case circle
      case rect

      var size: CGSize {
        switch self {
        case .circle: return CGSize(width: 100.0, height: 100.0)
        case .rect: return CGSize(width: 200.0, height: 200.0)
        }
      }

      var path: UIBezierPath {
        switch self {
        case .circle: return SVGIcons.circlePath1
        case .rect: return SVGIcons.rectPath1
        }
      }

      func image(withSize size: CGSize, opaque: Bool = false, alignment: Alignment = .center) -> UIImage {
        switch self {
        case .circle: return SVGIcons.image(withSize: size, opaque: opaque, alignment: alignment, drawingMethod: SVGIcons.drawCircle)
        case .rect: return SVGIcons.image(withSize: size, opaque: opaque, alignment: alignment, drawingMethod: SVGIcons.drawRect)
        }
      }

      func draw(inRect target: CGRect, alignment: Alignment = .center){
        switch self {
        case .circle: return SVGIcons.drawCircle(inRect: target, alignment: alignment)
        case .rect: return SVGIcons.drawRect(inRect: target, alignment: alignment)
        }
      }

      private static func drawCircle(inRect target: CGRect = CGRect(x: 0, y: 0, width: 100.0, height: 100.0), alignment: Alignment = .center) {
        let frame = CGRect(origin: .zero, size: SVGIcons.circle.size)

        let context = UIGraphicsGetCurrentContext()!
        context.saveGState()
        context.concatenate(SVGIcons.transformToFit(rect: frame, inRect: target, alignment: alignment))
           
        let path1 = SVGIcons.circlePath1
        UIColor(red: 0, green: 0, blue: 0, alpha: 1.0).setFill()
        path1.fill()

        context.restoreGState()
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
      private static let circlePath1: UIBezierPath = {
        let path = UIBezierPath()
        path.move(to: CGPoint(x: 50.0, y: 10.0))
        path.addCurve(to: CGPoint(x: 90.0, y: 50.0), controlPoint1: CGPoint(x: 72.0913899932, y: 10.0), controlPoint2: CGPoint(x: 90.0, y: 27.9086100068))
        path.addCurve(to: CGPoint(x: 50.0, y: 90.0), controlPoint1: CGPoint(x: 90.0, y: 72.0913899932), controlPoint2: CGPoint(x: 72.0913899932, y: 90.0))
        path.addCurve(to: CGPoint(x: 10.0, y: 50.0), controlPoint1: CGPoint(x: 27.9086100068, y: 90.0), controlPoint2: CGPoint(x: 10.0, y: 72.0913899932))
        path.addCurve(to: CGPoint(x: 50.0, y: 10.0), controlPoint1: CGPoint(x: 10.0, y: 27.9086100068), controlPoint2: CGPoint(x: 27.9086100068, y: 10.0))
        path.close()
        return path
      }()
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

How to use it
-------------

```swift
    // Using images
    let imageViewSize = CGSize(width: 200, height: 200)
    let imageView = UIImageView(frame: CGRect(origin: .zero, size: imageViewSize))
    imageView.image = SVGIcons.circle.image(withSize: imageViewSize)
    
    // Using draw(rect:)
    class CustomView: UIView {
        override func draw(_ rect: CGRect) {
            SVGIcons.circle.draw(inRect: self.bounds)
        }
    }

    let customView = CustomView(frame: CGRect(x: 0, y: 0, width: 200, height: 200))
    customView.backgroundColor = UIColor.white
```

Notes
-----

At this moment, it only supports Swift code generation.

It doesn't implement the full SVG 1.1 specification. 

Whenever I find something from the specification that I need I implement it.

I might also accept implementation requests, e.g., if someone needs shadows or gradients support. 

[Future: Instead of using templates for formating, I'll just feed unformatted code into a formater.]

License
-------

MIT - Copyright (c) 2017 Tiago Bras
