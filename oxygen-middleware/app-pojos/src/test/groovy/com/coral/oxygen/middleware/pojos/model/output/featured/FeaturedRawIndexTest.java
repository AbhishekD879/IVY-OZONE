package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex.PageType;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Test;

public class FeaturedRawIndexTest {

  @Test
  public void testPageTypeEventHub() throws Exception {
    Optional<PageType> pageType = PageType.fromPageId("h1567");
    Assert.assertEquals(
        PageType.eventhub, pageType.orElseThrow(() -> new Exception("Fail on h1567")));
  }

  @Test
  public void testPageTypeSport() throws Exception {
    Optional<PageType> pageType = PageType.fromPageId("1");
    Assert.assertEquals(PageType.sport, pageType.orElseThrow(() -> new Exception("Fail on 1")));
  }

  @Test
  public void testPageTypeSportEventHub() throws Exception {
    Optional<PageType> pageType = PageType.fromPageId("s1");
    Assert.assertEquals(
        PageType.sporteventhub, pageType.orElseThrow(() -> new Exception("Fail on s1")));
  }

  @Test
  public void testPageTypeUnknown() {
    Assert.assertFalse(PageType.fromPageId("1j").isPresent());
  }
}
