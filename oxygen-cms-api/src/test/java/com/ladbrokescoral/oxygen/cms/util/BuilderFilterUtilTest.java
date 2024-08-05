package com.ladbrokescoral.oxygen.cms.util;

import static org.junit.jupiter.api.Assertions.*;

import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import org.junit.Test;

public class BuilderFilterUtilTest {

  @Test
  public void getLiveEventsFilterBuilderTest() {
    assertNotNull(BuilderFilterUtil.getLiveEventsFilterBuilder(getSportCategory()));
  }

  @Test
  public void getEventMarketIsAvailableFilterTest() {
    assertNotNull(BuilderFilterUtil.getEventMarketIsAvailableFilter());
  }

  @Test
  public void getUpcomingEventExistsforMatchesTabBuilderTest() {
    assertNotNull(BuilderFilterUtil.getUpcomingEventExistsforMatchesTabBuilder(getSportCategory()));
  }

  @Test
  public void getExistsFilterTest() {
    assertNotNull(BuilderFilterUtil.getExistsFilter());
  }

  @Test
  public void getLiveEventExistsforMatchesTabBuilderTest() {
    assertNotNull(BuilderFilterUtil.getLiveEventExistsforMatchesTabBuilder(getSportCategory()));
  }

  @Test
  public void getUpcomingEventExistsForNext24HBuilderTest() {
    assertNotNull(BuilderFilterUtil.getUpcomingEventExistsForNext24HBuilder(getSportCategory()));
  }

  @Test
  public void getUpcomingEventBuilderTest() {
    assertNotNull(BuilderFilterUtil.getUpcomingEventBuilder(getSportCategory()));
  }

  SportCategory getSportCategory() {
    SportCategory sportCategory = new SportCategory();
    sportCategory.setBrand("ladbrokes");
    sportCategory.setCategoryId(1);
    return sportCategory;
  }
}
