package com.coral.oxygen.middleware.ms.liveserv.utils;

import org.junit.Assert;
import org.junit.Test;

public class StringUtilsTest {

  @Test
  public void testValidateDigits() {
    Assert.assertTrue(StringUtils.validateDigits("123456"));
    Assert.assertFalse(StringUtils.validateDigits("123456,"));
    Assert.assertFalse(StringUtils.validateDigits("g123456"));
    Assert.assertFalse(StringUtils.validateDigits("-g123456"));
  }

  @Test
  public void testNormalizeNumber() {
    Assert.assertEquals("123456", StringUtils.normalizeNumber("123456"));
    Assert.assertEquals("1", StringUtils.normalizeNumber("1"));
    Assert.assertEquals("2221", StringUtils.normalizeNumber("00002221"));
    Assert.assertEquals("0", StringUtils.normalizeNumber("0000"));
  }

  @Test(expected = IllegalArgumentException.class)
  public void testNormalizeNumberNotNumber() {
    StringUtils.normalizeNumber("12345a");
  }

  @Test(expected = IllegalArgumentException.class)
  public void testNormalizeNumberEmpty() {
    StringUtils.normalizeNumber("");
  }

  @Test
  public void testAddLeadingZeros() {
    Assert.assertEquals("0000123456", StringUtils.addLeadingZeros("123456", 10));
    Assert.assertEquals("0000123456", StringUtils.addLeadingZeros("00123456", 10));
    Assert.assertEquals("0100123456", StringUtils.addLeadingZeros("100123456", 10));
    Assert.assertEquals("0000000000", StringUtils.addLeadingZeros("0", 10));
  }

  @Test(expected = IllegalArgumentException.class)
  public void testAddLeadingZerosNotNumber() {
    StringUtils.addLeadingZeros("12345a", 10);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testAddLeadingZerosToLongNumber() {
    StringUtils.addLeadingZeros("12345", 3);
  }
}
