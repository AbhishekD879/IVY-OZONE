package com.oxygen.publisher.util;

public class RangeScanner {

  private String startRange;
  private int index;

  public RangeScanner(String startRange) {
    this.startRange = startRange;
    this.index = 0;
  }

  public boolean hasNext() {
    return index < startRange.length();
  }

  public String next() {
    String value = nextElement(new StringFunction());
    return value;
  }

  public Integer nextInt() {
    Integer value = nextElement(new IntegerFunction());
    return value;
  }

  protected <T> T nextElement(ElementFunction<T> function) {
    StringBuilder buffer = new StringBuilder();
    char character = startRange.charAt(index);
    while (function.accept(character)) {
      buffer.append(character);
      index = index + 1;
      if (!hasNext()) {
        break;
      }
      character = startRange.charAt(index);
    }
    return function.toValue(buffer.toString());
  }

  public interface ElementFunction<T> {

    boolean accept(char character);

    T toValue(String string);
  }

  private static class StringFunction implements ElementFunction<String> {

    @Override
    public boolean accept(char character) {
      return !Character.isDigit(character);
    }

    @Override
    public String toValue(String string) {
      return string;
    }
  }

  private static class IntegerFunction implements ElementFunction<Integer> {

    @Override
    public boolean accept(char character) {
      return Character.isDigit(character);
    }

    @Override
    public Integer toValue(String string) {
      return Integer.valueOf(string);
    }
  }
}
