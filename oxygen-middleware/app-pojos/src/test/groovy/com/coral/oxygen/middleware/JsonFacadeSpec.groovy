package com.coral.oxygen.middleware

import com.google.gson.Gson
import spock.lang.Specification

class JsonFacadeSpec extends Specification {

  abstract class Shape {

    int x = 10;
    int y = 11;
  }

  class Circle extends Shape {
    int radius;

    Circle(int radius) {
      this.radius = radius
    }
  }

  class Rectangle extends Shape {
    int width = 12;
    int height = 13;
  }

  def "JSON polymorphism translation for both sides"() {
    RuntimeTypeAdapterFactory<Shape> adapterFactory = RuntimeTypeAdapterFactory
        .of(Shape.class)
        .registerSubtype(Circle.class)
        .registerSubtype(Rectangle.class)
    Gson jsonParser = JsonFacade.createParser({ builder -> builder.registerTypeAdapterFactory(adapterFactory)})

    when:
    String output = jsonParser.toJson(new Circle(5))
    Shape circle = jsonParser.fromJson(output, Shape.class)


    then:
    circle instanceof Circle
  }
}
