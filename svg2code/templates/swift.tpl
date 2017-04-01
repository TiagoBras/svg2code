{% macro point(x, y) -%}
    CGPoint(x: {{ x | stripzeros }}, y: {{ y | stripzeros }})
{%- endmacro %}
{% macro makeSize(width, height) -%}
    CGSize(width: {{ width | stripzeros }}, height: {{ height | stripzeros }})
{%- endmacro %}
{% macro makeRect(x, y, width, height) -%}
    CGRect(x: {{ x | stripzeros }}, y: {{ y | stripzeros }}, width: {{ width | stripzeros }}, height: {{ height | stripzeros }})
{%- endmacro %}
{% macro rgbaColor(c) -%}
    UIColor(red: {{ c.r | stripzeros }}, green: {{ c.g | stripzeros }}, blue: {{ c.b | stripzeros }}, alpha: {{ c.a | stripzeros }})
{%- endmacro %}
{% macro makeBezierPath(path, name) %}
    let {{ name }} = UIBezierPath()
    {% for c in path.commands %}
        {% if c is MoveTo %}
    {{ name }}.move(to: {{ point(c.x, c.y) }})
        {% elif c is LineTo %}
    {{ name }}.addLine(to: {{ point(c.x, c.y) }})
        {% elif c is CurveTo %}
    {{ name }}.addCurve(to: {{ point(c.x, c.y) }}, controlPoint1: {{ point(c.x1, c.y1) }}, controlPoint2: {{ point(c.x2, c.y2) }})
        {% elif c is ClosePath %}
    {{ name }}.close()
        {% else %}
            // Command unknown: {{ p }} 
        {% endif %}
    {% endfor %}
{% endmacro %}
{% macro makeBezierPathStyle(path, name) -%}
    {% if path.usesEvenOddFillRule %}
    {{ name }}.usesEvenOddFillRule = true
    {% endif %}
    {% set strokeLineCap = path.strokeLineCap %}
    {% if strokeLineCap is not none and strokeLineCap != "butt" %}
    {{ name }}.lineCapStyle = .{{ strokeLineCap | stripzeros }}
    {% endif %}
    {% set strokeWidth = path.strokeWidth %}
    {% if strokeWidth is not none and strokeWidth != 1.0 %}
    {{ name }}.lineWidth = {{ strokeWidth | stripzeros }}
    {% endif %}
    {% set fillColor = path.rgbaFillColor %}
    {% if fillColor is not none %}
    {{ rgbaColor(fillColor) }}.setFill()
    {{ name }}.fill()
    {% endif %}
    {% set strokeColor = path.rgbaStrokeColor %}
    {% if strokeColor is not none %}
    {{ rgbaColor(strokeColor) }}.setStroke()
    {{ name }}.stroke()
    {% endif %}
{%- endmacro %}
{% macro renderSvg(svg) %}
    {% for path in svg.paths %}
        {% set pathName = "path" + loop.index | string %}   
        let {{ pathName }} = {{ class_name }}.{{ enumCase(svg.name) }}Path{{ loop.index }}
    {{ makeBezierPathStyle(path, pathName) | indent(4) }}
    {% endfor %}
{% endmacro %}
{% macro enumCase(name) %}
{{ name | firstlower }}
{%- endmacro %}
//
//  {{ class_name }}.swift
//  {{ project }}
//
//  Created by {{ author }} on {{ date.day|string|lpad(2, '0') }}/{{ date.month|string|lpad(2, '0') }}/{{ date.year }}.
//  Copyright © {{ date.year }} {{ author | removewhitespace }}. All rights reserved.
//

import UIKit

enum {{ class_name }} {
{% for svg in svgs %}
    case {{ enumCase(svg.name) }}
{% endfor %}

    var size: CGSize {
        switch self {
    {% for svg in svgs %}
        case .{{ enumCase(svg.name) }}: return {{ makeSize(svg.width, svg.height) }}
    {% endfor %}
        }
    }

    func image(withSize size: CGSize, opaque: Bool = false, alignment: Alignment = .center) -> UIImage {
        switch self {
    {% for svg in svgs %}
        case .{{ enumCase(svg.name) }}: return {{ class_name }}.image(withSize: size, opaque: opaque, alignment: alignment, drawingMethod: {{ class_name }}.draw{{ svg.name | title }})
    {% endfor %}
        }
    }

    func draw(inRect target: CGRect, alignment: Alignment = .center){
        switch self {
    {% for svg in svgs %}
        case .{{ enumCase(svg.name) }}: return {{ class_name }}.draw{{ svg.name | title }}(inRect: target, alignment: alignment)
    {% endfor %}
        }
    }

    var path: UIBezierPath {
        switch self {
    {% for svg in svgs %}
        {% if svg.paths | list | length == 1 %}
        case .{{ enumCase(svg.name) }}: return {{ class_name }}.{{ enumCase(svg.name) }}Path1
        {% else %}
        case .{{ enumCase(svg.name) }}: 
            let path = UIBezierPath()
        {% for path in svg.paths %}
            path.append({{ class_name }}.{{ enumCase(svg.name) }}Path{{ loop.index }})
        {% endfor %}
            return path
        {% endif %}
    {% endfor %}
        }
    }

{% for svg in svgs %}
    private static func draw{{ svg.name | title }}(inRect target: CGRect = CGRect(x: 0, y: 0, width: {{ svg.width }}, height: {{ svg.height }}), alignment: Alignment = .center) {
        let frame = CGRect(origin: .zero, size: {{ class_name }}.{{ enumCase(svg.name) }}.size)

        let context = UIGraphicsGetCurrentContext()!
        context.saveGState()
        context.concatenate({{ class_name }}.transformToFit(rect: frame, inRect: target, alignment: alignment))
        {{ renderSvg(svg) }}
        context.restoreGState()
    }

{% endfor %}

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
{% for svg in svgs %}
    {% for path in svg.paths %}
    private static let {{ enumCase(svg.name) }}Path{{ loop.index }}: UIBezierPath = {
    {{ makeBezierPath(path, "path") | indent(4) }}
        return path
    }()
    {% endfor %}
{% endfor %}
}