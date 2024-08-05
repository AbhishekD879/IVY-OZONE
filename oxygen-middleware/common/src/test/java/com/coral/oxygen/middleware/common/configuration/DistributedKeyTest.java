package com.coral.oxygen.middleware.common.configuration;

import org.junit.Assert;
import org.junit.Ignore;
import org.junit.Test;

/**
 * @author volodymyr.masliy
 */
@Deprecated
@Ignore
public class DistributedKeyTest {

  @Test
  public void testFromNameDoesNotExist() {
    Assert.assertFalse(DistributedKey.fromString("bla-bla").isPresent());
  }

  @Test
  public void testFromName() {
    Assert.assertEquals(
        DistributedKey.INPLAY_STRUCTURE_MAP,
        DistributedKey.fromString("inplay_structure").orElse(null));
  }
}
