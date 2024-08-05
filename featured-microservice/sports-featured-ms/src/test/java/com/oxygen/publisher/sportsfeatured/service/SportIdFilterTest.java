package com.oxygen.publisher.sportsfeatured.service;

import com.oxygen.publisher.model.PageType;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import org.junit.Assert;
import org.junit.Test;

public class SportIdFilterTest {

  @Test
  public void testWithoutSlash() {
    SportIdFilter filter = filter(PageType.sport);
    Assert.assertTrue(filter.isSupportedPageType("1"));
  }

  @Test
  public void testSupportedEventHub() {
    SportIdFilter filter = filter(PageType.sport, PageType.eventhub);
    Assert.assertTrue(filter.isSupportedPageType("h3"));
  }

  @Test
  public void testSupportedUnsupportedId() {
    SportIdFilter filter = filter(PageType.sport, PageType.eventhub);
    Assert.assertTrue(filter.isSupportedPageType("h35"));
  }

  @Test
  public void testSupportedUnsupportedIdAndType() {
    SportIdFilter filter = filter(PageType.sport, PageType.eventhub);
    Assert.assertFalse(filter.isSupportedPageType("g35"));
  }

  @Test
  public void testSupportedUnsupportedType() {
    SportIdFilter filter = filter(PageType.sport, PageType.eventhub);
    Assert.assertFalse(filter.isSupportedPageType("s35"));
  }

  @Test
  public void testSupportedSportEventHub() {
    SportIdFilter filter = filter(PageType.sport, PageType.eventhub, PageType.sporteventhub);
    Assert.assertTrue(filter.isSupportedPageType("s5"));
  }

  public SportIdFilter filter(PageType... types) {
    List<PageType> pageTypes = new ArrayList<PageType>();
    pageTypes.addAll(Arrays.asList(types));
    SportIdFilter filter = new SportIdFilter(pageTypes);
    return filter;
  }
}
