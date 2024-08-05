package com.egalacoral.spark.timeform.api.connectivity;

import com.egalacoral.spark.timeform.api.TimeFormException;
import org.junit.Assert;
import org.junit.Test;

public class NoFailOverStrategyTest {

  @Test
  public void testOnError() {
    NoFailOverStrategy noFailOverStrategy = new NoFailOverStrategy();
    Assert.assertNull(noFailOverStrategy.onError(new TimeFormException(), 100));
  }

  @Test
  public void testOnReloginError() {
    NoFailOverStrategy noFailOverStrategy = new NoFailOverStrategy();
    Assert.assertNull(noFailOverStrategy.onReloginError(new TimeFormException(), 100));
  }
}
