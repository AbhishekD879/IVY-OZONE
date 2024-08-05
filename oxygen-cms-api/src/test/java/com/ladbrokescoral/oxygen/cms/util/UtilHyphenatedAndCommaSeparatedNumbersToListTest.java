package com.ladbrokescoral.oxygen.cms.util;

import static org.junit.Assert.assertEquals;

import java.util.Arrays;
import java.util.List;
import org.junit.Test;

public class UtilHyphenatedAndCommaSeparatedNumbersToListTest {

  @Test
  public void test() {
    String input = "1";
    List<Integer> result = Util.hyphenatedAndCommaSeparatedNumbersToList(input);
    assertEquals(Arrays.asList(1), result);

    input = "1,1";
    result = Util.hyphenatedAndCommaSeparatedNumbersToList(input);
    assertEquals(Arrays.asList(1), result);

    input = "1-1";
    result = Util.hyphenatedAndCommaSeparatedNumbersToList(input);
    assertEquals(Arrays.asList(1), result);

    input = "1-2";
    result = Util.hyphenatedAndCommaSeparatedNumbersToList(input);
    assertEquals(Arrays.asList(1, 2), result);

    input = "1-2,1-2";
    result = Util.hyphenatedAndCommaSeparatedNumbersToList(input);
    assertEquals(Arrays.asList(1, 2), result);

    input = "1-2,3";
    result = Util.hyphenatedAndCommaSeparatedNumbersToList(input);
    assertEquals(Arrays.asList(1, 2, 3), result);

    input = "0,0,4-3,1";
    result = Util.hyphenatedAndCommaSeparatedNumbersToList(input);
    assertEquals(Arrays.asList(0, 1, 3, 4), result);

    input = "9-8,8,8-9";
    result = Util.hyphenatedAndCommaSeparatedNumbersToList(input);
    assertEquals(Arrays.asList(8, 9), result);

    input = "1,2,3,4,4,3,2,1,1,2,2-3,3-4,4-3,2-4,1-4,4-1";
    result = Util.hyphenatedAndCommaSeparatedNumbersToList(input);
    assertEquals(Arrays.asList(1, 2, 3, 4), result);

    input = "0";
    result = Util.hyphenatedAndCommaSeparatedNumbersToList(input);
    assertEquals(Arrays.asList(0), result);

    input = "10000";
    result = Util.hyphenatedAndCommaSeparatedNumbersToList(input);
    assertEquals(Arrays.asList(10000), result);

    input = "00001";
    result = Util.hyphenatedAndCommaSeparatedNumbersToList(input);
    assertEquals(Arrays.asList(1), result);

    input = "00001, 001-000004";
    result = Util.hyphenatedAndCommaSeparatedNumbersToList(input);
    assertEquals(Arrays.asList(1, 2, 3, 4), result);

    input = "10,    4-0";
    result = Util.hyphenatedAndCommaSeparatedNumbersToList(input);
    assertEquals(Arrays.asList(0, 1, 2, 3, 4, 10), result);

    input = "    1,    5,    7  -  7      ,      2";
    result = Util.hyphenatedAndCommaSeparatedNumbersToList(input);
    assertEquals(Arrays.asList(1, 2, 5, 7), result);
  }
}
