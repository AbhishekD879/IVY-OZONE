package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import com.ladbrokescoral.oxygen.cms.api.service.sporttab.MainTier1Sports;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.MainTier2Sports;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class Tier1nTier2SportsTabTest {

  @Test
  public void testaddTabsForTier1Sports() {
    MainTier1Sports mainTier1Sports = MainTier1Sports.FOOTBALL;
    Assert.assertEquals("FOOTBALL", mainTier1Sports.getName());
    Assert.assertNotNull(MainTier1Sports.categoryIds());
  }

  @Test
  public void testaddTabsForTier2Sports() {
    MainTier2Sports mainTier2Sports = MainTier2Sports.GOLF;
    Assert.assertEquals("GOLF", mainTier2Sports.getName());
    Assert.assertNotNull(MainTier1Sports.categoryIds());
  }
}
