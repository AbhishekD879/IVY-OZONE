package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.when;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeKnockoutEventDto;
import com.ladbrokescoral.oxygen.cms.api.exception.InputValueIncorrectException;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeServiceImpl;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class CompetitionsGetKnockoutEventTest {

  Competitions competitionController;

  @Mock SiteServerApi siteServerApi;

  @Mock SiteServeApiProvider siteServeApiProvider;

  @Before
  public void setUp() throws Exception {
    SiteServeService siteServerService = new SiteServeServiceImpl(siteServeApiProvider);
    competitionController = new Competitions(null, siteServerService, null);
    when(siteServeApiProvider.api("bma")).thenReturn(siteServerApi);
  }

  @Test
  public void testGetKnockoutEventById() throws Exception {
    Event event =
        TestUtil.deserializeWithJackson(
            "controller/private_api/competition/competition-ss-knockout-event.json", Event.class);
    when(siteServerApi.getEvent("8133119", true)).thenReturn(Optional.of(event));

    SiteServeKnockoutEventDto result = competitionController.getKnockoutEvent("bma", "8133119");

    SiteServeKnockoutEventDto expected =
        TestUtil.deserializeWithJackson(
            "controller/private_api/competition/competition-dto-knockout-event.json",
            SiteServeKnockoutEventDto.class);

    assertEquals(expected, result);
  }

  @Test(expected = InputValueIncorrectException.class)
  public void testGetKnockoutEventByInvalidId() throws Exception {
    when(siteServerApi.getEvent("8133120", true)).thenReturn(Optional.empty());
    competitionController.getKnockoutEvent("bma", "8133120");
  }

  @Test(expected = InputValueIncorrectException.class)
  public void testGetKnockoutEventByEmptydId() throws Exception {
    competitionController.getKnockoutEvent("bma", "");
  }
}
