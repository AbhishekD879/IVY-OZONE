package com.egalacoral.spark.liveserver.utils;

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

  @Test
  public void testAddLeadingZeros() {
    Assert.assertEquals("0000123456", StringUtils.addLeadingZeros("123456", 10));
    Assert.assertEquals("0000123456", StringUtils.addLeadingZeros("00123456", 10));
    Assert.assertEquals("0100123456", StringUtils.addLeadingZeros("100123456", 10));
    Assert.assertEquals("0000000000", StringUtils.addLeadingZeros("0", 10));
  }
}
