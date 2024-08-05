package com.coral.oxygen.middleware.featured.service;

import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPage;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex.PageType;
import java.util.ArrayList;
import java.util.Arrays;
import org.junit.Assert;
import org.junit.Test;

public class SportPageFilterTest {

  @Test
  public void testSupportedPageSport() {
    SportPageFilter filter = filter(PageType.sport);
    Assert.assertTrue(filter.isSupportedPage(page("1")));
  }

  @Test
  public void testSupportedPageEventHub() {
    SportPageFilter filter = filter(PageType.sport, PageType.eventhub);
    Assert.assertTrue(filter.isSupportedPage(page("h3")));
  }

  @Test
  public void testSupportedPageUnsupportedId() {
    SportPageFilter filter = filter(PageType.sport, PageType.eventhub);
    Assert.assertTrue(filter.isSupportedPage(page("h35")));
  }

  @Test
  public void testSupportedPageUnsupportedIdAndType() {
    SportPageFilter filter = filter(PageType.sport, PageType.eventhub);
    Assert.assertFalse(filter.isSupportedPage(page("g35")));
  }

  @Test
  public void testSupportedPageUnsupportedType() {
    SportPageFilter filter = filter(PageType.sport, PageType.eventhub);
    Assert.assertFalse(filter.isSupportedPage(page("s35")));
  }

  @Test
  public void testSupportedPageSportEventHub() {
    SportPageFilter filter = filter(PageType.sport, PageType.eventhub, PageType.sporteventhub);
    Assert.assertTrue(filter.isSupportedPage(page("s5")));
  }

  public SportPageFilter filter(PageType... types) {
    return new SportPageFilter(Arrays.asList(types));
  }

  private SportPage page(String sportId) {
    return new SportPage(sportId, new ArrayList<>());
  }
}
