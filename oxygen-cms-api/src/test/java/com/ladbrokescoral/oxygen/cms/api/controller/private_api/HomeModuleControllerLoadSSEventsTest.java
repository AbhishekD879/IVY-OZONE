package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.junit.Assert.assertEquals;
import static org.mockito.Matchers.any;
import static org.mockito.Matchers.anyObject;
import static org.mockito.Matchers.eq;
import static org.mockito.Mockito.when;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Aggregation;
import com.egalacoral.spark.siteserver.model.Event;
import com.google.common.base.Joiner;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventDto;
import com.ladbrokescoral.oxygen.cms.api.exception.SiteServeMarketValidationException;
import com.ladbrokescoral.oxygen.cms.api.service.impl.HomeModuleSiteServeServiceImpl;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeLoadEventByCategory;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeLoadEventByClass;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeLoadEventByEnhancedMultiples;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeLoadEventById;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeLoadEventByMarket;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeLoadEventByRaceTypeId;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeLoadEventBySelection;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeLoadEventByType;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeLoadEventFactory;
import com.ladbrokescoral.oxygen.cms.configuration.MarketTemplateFilterConfig;
import java.time.Duration;
import java.time.OffsetDateTime;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class HomeModuleControllerLoadSSEventsTest {

  private final String marketId = "8789522";

  @Mock private SiteServerApi siteServerApi;
  @Mock SiteServeApiProvider siteServeApiProvider;
  @Mock MarketTemplateFilterConfig marketTemplateFilterConfig;
  private HomeModules homeModuleController;

  private List<SiteServeEventDto> expected;

  private List<String> categoryCodes;
  private List<String> eventCodes;
  private List<String> templates;
  private List<String> eventCodesForDiffCategories;

  @Before
  public void setUp() throws Exception {
    categoryCodes =
        Arrays.asList(
            "MOTOR_CARS",
            "TV_SPECIALS",
            "CYCLING",
            "MOTOR_SPEEDWAY",
            "MOTOR_BIKES",
            "POLITICS",
            "GOLF",
            "MOTOR_SPORTS",
            "MOVIES");
    eventCodes =
        Arrays.asList(
            "TNMT", "TR01", "TR02", "TR03", "TR04", "TR05", "TR06", "TR07", "TR08", "TR09", "TR10",
            "TR11", "TR12", "TR13", "TR14", "TR15", "TR16", "TR17", "TR18", "TR19", "TR20", "MTCH");
    eventCodesForDiffCategories =
        Arrays.asList(
            "TNMT", "TR01", "TR02", "TR03", "TR04", "TR05", "TR06", "TR07", "TR08", "TR09", "TR10",
            "TR11", "TR12", "TR13", "TR14", "TR15", "TR16", "TR17", "TR18", "TR19", "TR20");
    templates =
        Arrays.asList(
            "Win or Each Way",
            "Match Betting",
            "Match Result",
            "Match Results",
            "Extra Time Result",
            "Extra-Time Result",
            "Penalty Shoot-Out Winner",
            "To Qualify");

    Joiner joiner = Joiner.on(",");

    SiteServeLoadEventByEnhancedMultiples siteServeLoadEventByEnhancedMultiples =
        new SiteServeLoadEventByEnhancedMultiples(siteServeApiProvider);
    SiteServeLoadEventByRaceTypeId siteServeLoadEventByRaceTypeId =
        new SiteServeLoadEventByRaceTypeId(siteServeApiProvider, marketTemplateFilterConfig);
    SiteServeLoadEventBySelection siteServeLoadEventBySelection =
        new SiteServeLoadEventBySelection(siteServeApiProvider);
    SiteServeLoadEventByType siteServeLoadEventByType =
        new SiteServeLoadEventByType("M", joiner.join(eventCodes), siteServeApiProvider);
    SiteServeLoadEventByClass siteServeLoadEventByClass =
        new SiteServeLoadEventByClass(siteServeApiProvider);
    SiteServeLoadEventByCategory siteServeLoadEventByCategory =
        new SiteServeLoadEventByCategory(siteServeApiProvider);
    SiteServeLoadEventByMarket siteServeLoadEventByMarket =
        new SiteServeLoadEventByMarket(
            joiner.join(categoryCodes),
            joiner.join(eventCodes),
            joiner.join(eventCodesForDiffCategories),
            joiner.join(templates),
            siteServeApiProvider);
    SiteServeLoadEventById siteServeLoadEventById =
        new SiteServeLoadEventById("M", joiner.join(eventCodes), siteServeApiProvider);

    SiteServeLoadEventFactory siteServeLoadEventFactory =
        new SiteServeLoadEventFactory(
            siteServeLoadEventByEnhancedMultiples,
            siteServeLoadEventByRaceTypeId,
            siteServeLoadEventBySelection,
            siteServeLoadEventByType,
            siteServeLoadEventByClass,
            siteServeLoadEventByCategory,
            siteServeLoadEventByMarket,
            siteServeLoadEventById);

    homeModuleController =
        new HomeModules(
            null,
            new HomeModuleSiteServeServiceImpl(siteServeApiProvider, siteServeLoadEventFactory));

    when(siteServeApiProvider.api(any())).thenReturn(siteServerApi);
    List<Event> events =
        TestUtil.deserializeListWithJackson(
            "controller/private_api/home-module-ss-events.json", Event.class);
    when(siteServerApi.getEventToOutcomeForType(eq("442"), anyObject()))
        .thenReturn(Optional.ofNullable(events));

    List<Aggregation> marketCounts =
        TestUtil.deserializeListWithJackson(
            "controller/private_api/home-module-ss-events-market-counts.json", Aggregation.class);
    when(siteServerApi.getMarketsCountForEvent(any(), any()))
        .thenReturn(Optional.ofNullable(marketCounts));

    when(siteServerApi.getEventToOutcomeForOutcome(any(), any(), any()))
        .thenReturn(Optional.ofNullable(events));

    Optional<List<Event>> event =
        Optional.of(
            Collections.singletonList(
                TestUtil.deserializeWithJackson(
                    "controller/private_api/home-module-ss-event-by-market.json", Event.class)));
    when(siteServerApi.getWholeEventToOutcomeForMarket(any(), any())).thenReturn(event);

    expected =
        TestUtil.deserializeListWithJackson(
            "controller/private_api/home-module-ss-events-dto.json", SiteServeEventDto.class);
  }

  @Test
  public void testLoadSSEventsByRaceTypeId() {

    List<SiteServeEventDto> result =
        homeModuleController.loadSSEvents(
            "bma",
            "RaceTypeId",
            "442",
            OffsetDateTime.now(),
            OffsetDateTime.now().minus(Duration.ofDays(1)));
    assertEquals(expected, result);
  }

  @Test
  public void testLoadSSEventsByType() throws Exception {

    expected =
        TestUtil.deserializeListWithJackson(
            "controller/private_api/home-module-ss-events-dto-with-outright.json",
            SiteServeEventDto.class);

    List<SiteServeEventDto> result =
        homeModuleController.loadSSEvents(
            "bma",
            "Type",
            "442",
            OffsetDateTime.now(),
            OffsetDateTime.now().minus(Duration.ofDays(1)));
    assertEquals(expected, result);
  }

  @Test
  public void testLoadSSEventsBySelection() throws Exception {
    expected =
        TestUtil.deserializeListWithJackson(
            "controller/private_api/home-module-ss-events-selection-dto.json",
            SiteServeEventDto.class);

    List<SiteServeEventDto> result =
        homeModuleController.loadSSEvents(
            "bma",
            "Selection",
            "442",
            OffsetDateTime.now(),
            OffsetDateTime.now().minus(Duration.ofDays(1)));
    assertEquals(expected, result);
  }

  @Test
  public void testLoadSSEventsByEnhancedMultiples() {

    List<SiteServeEventDto> result =
        homeModuleController.loadSSEvents(
            "bma",
            "Enhanced Multiples",
            "442",
            OffsetDateTime.now(),
            OffsetDateTime.now().minus(Duration.ofDays(1)));
    assertEquals(expected, result);
  }

  @Test
  public void testLoadSSEventsByMarket() throws Exception {
    expected =
        TestUtil.deserializeListWithJackson(
            "controller/private_api/home-module-ss-event-by-market-dto.json",
            SiteServeEventDto.class);

    List<SiteServeEventDto> result =
        homeModuleController.loadSSEvents(
            "bma", "Market", marketId, OffsetDateTime.now(), OffsetDateTime.now());
    assertEquals(expected, result);
  }

  @Test
  public void testLoadSSEventsByMatchResultMarket() throws Exception {
    expected =
        TestUtil.deserializeListWithJackson(
            "controller/private_api/home-module-ss-event-by-market-dto.json",
            SiteServeEventDto.class);

    Optional<List<Event>> event =
        Optional.of(
            Collections.singletonList(
                TestUtil.deserializeWithJackson(
                    "controller/private_api/home-module-ss-event-by-match-result-market.json",
                    Event.class)));
    when(siteServerApi.getWholeEventToOutcomeForMarket(any(), any())).thenReturn(event);

    List<SiteServeEventDto> result =
        homeModuleController.loadSSEvents(
            "bma", "Market", marketId, OffsetDateTime.now(), OffsetDateTime.now());
    assertEquals(expected, result);
  }

  @Test
  public void testLoadSSEventsByMarketWithValidationOnCategoryAndSortCode() throws Exception {
    expected =
        TestUtil.deserializeListWithJackson(
            "controller/private_api/home-module-ss-event-by-market-dto.json",
            SiteServeEventDto.class);
    Event inputJson =
        TestUtil.deserializeWithJackson(
            "controller/private_api/home-module-ss-event-by-market.json", Event.class);

    for (String categoryCode : categoryCodes) {
      inputJson.setCategoryCode(categoryCode);

      for (String sortCode : eventCodes) {
        inputJson.setEventSortCode(sortCode);

        Optional<List<Event>> event = Optional.of(Collections.singletonList(inputJson));
        when(siteServerApi.getWholeEventToOutcomeForMarket(any(), any())).thenReturn(event);
        List<SiteServeEventDto> result =
            homeModuleController.loadSSEvents(
                "bma", "Market", marketId, OffsetDateTime.now(), OffsetDateTime.now());
        assertEquals(expected, result);
      }
    }
  }

  @Test
  public void testLoadSSEventsByMarketWithValidationOnSortCode() throws Exception {
    expected =
        TestUtil.deserializeListWithJackson(
            "controller/private_api/home-module-ss-event-by-market-dto.json",
            SiteServeEventDto.class);
    Event inputJson =
        TestUtil.deserializeWithJackson(
            "controller/private_api/home-module-ss-event-by-market.json", Event.class);

    for (String sortCode : eventCodesForDiffCategories) {
      inputJson.setEventSortCode(sortCode);

      Optional<List<Event>> event = Optional.of(Collections.singletonList(inputJson));
      when(siteServerApi.getWholeEventToOutcomeForMarket(any(), any())).thenReturn(event);
      List<SiteServeEventDto> result =
          homeModuleController.loadSSEvents(
              "bma", "Market", marketId, OffsetDateTime.now(), OffsetDateTime.now());
      assertEquals(expected, result);
    }
  }

  @Test
  public void testLoadSSEventsByMarketWithValidationOnTemplate() throws Exception {
    expected =
        TestUtil.deserializeListWithJackson(
            "controller/private_api/home-module-ss-event-by-market-dto.json",
            SiteServeEventDto.class);
    Event inputJson =
        TestUtil.deserializeWithJackson(
            "controller/private_api/home-module-ss-event-by-market.json", Event.class);

    for (String template : templates) {
      inputJson.getMarkets().stream().forEach(m -> m.setTemplateMarketName(template));

      Optional<List<Event>> event = Optional.of(Collections.singletonList(inputJson));
      when(siteServerApi.getWholeEventToOutcomeForMarket(any(), any())).thenReturn(event);
      List<SiteServeEventDto> result =
          homeModuleController.loadSSEvents(
              "bma", "Market", marketId, OffsetDateTime.now(), OffsetDateTime.now());
      assertEquals(expected, result);
    }
  }

  @Test(expected = SiteServeMarketValidationException.class)
  public void testLoadSSEventsByMarketInvalid() throws Exception {
    Event inputJson =
        TestUtil.deserializeWithJackson(
            "controller/private_api/home-module-ss-event-by-market.json", Event.class);

    inputJson.setEventSortCode("not supported");
    inputJson.getMarkets().stream().forEach(m -> m.setTemplateMarketName("not a template"));

    Optional<List<Event>> event = Optional.of(Collections.singletonList(inputJson));
    when(siteServerApi.getWholeEventToOutcomeForMarket(any(), any())).thenReturn(event);

    homeModuleController.loadSSEvents(
        "bma", "Market", marketId, OffsetDateTime.now(), OffsetDateTime.now());
  }
}
