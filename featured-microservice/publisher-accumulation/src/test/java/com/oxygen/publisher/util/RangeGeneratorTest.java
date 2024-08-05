package com.oxygen.publisher.util;

import java.util.List;
import org.junit.Assert;
import org.junit.Test;

public class RangeGeneratorTest {

  @Test
  public void testToIds() {
    RangeGenerator rangeUtil = new RangeGenerator();
    List<String> ids = rangeUtil.generate("s1m1v5-s3m5v10");
    Assert.assertTrue(ids.contains("s2m2v5"));
    Assert.assertFalse(ids.contains("s2m2v3"));
  }
}
