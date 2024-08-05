package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.hamcrest.Matchers.isEmptyString;
import static org.hamcrest.Matchers.not;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertThat;

import com.ladbrokescoral.oxygen.cms.api.entity.SpotlightEvents;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.service.CrudService;
import com.ladbrokescoral.oxygen.cms.api.service.TimelineSpotlightService;
import java.time.Instant;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class TimelineSpotlightsTest extends BDDMockito {

  private TimelineSpotlightController controller;

  @Mock private TimelineSpotlightService service;

  @Mock private CrudService<User> userCrudService;

  private TimelineSpotlightController.RefreshSiteserveEventsQuery query;

  @Before
  public void setUp() {
    SpotlightEvents eventsFromSiteServe = new SpotlightEvents();

    when(service.fetchSiteServeDataForBrandByApi(any(), any())).thenReturn(eventsFromSiteServe);

    controller = new TimelineSpotlightController(service);

    query =
        new TimelineSpotlightController.RefreshSiteserveEventsQuery(
            Instant.MAX, "2352,35453", true);
  }

  @Test
  public void testRefreshingSiteServeData() {
    controller.refreshData("ladbrokes", query);

    verify(service, times(1)).fetchSiteServeDataForBrandByApi("ladbrokes", query);
  }

  @Test
  public void testSettingDefaultQueryParams() {
    query = new TimelineSpotlightController.RefreshSiteserveEventsQuery(null, "", true);
    controller.refreshData("ladbrokes", query);

    assertThat(query.getRefreshEventsClassesString(), not(isEmptyString()));
    assertNotNull(query.getRefreshEventsFrom());
  }

  @Test
  public void testFetchingSpotlightDataForEventId() {
    controller.fetchSpotlightDataForEventId("ladbrokes", "campaignId", "eventId");

    verify(service, times(1)).fetchSpotlightData("ladbrokes", "eventId");
  }
}
