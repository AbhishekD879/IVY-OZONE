package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.junit.Assert.assertEquals;
import static org.mockito.Matchers.anyObject;
import static org.mockito.Matchers.eq;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.egalacoral.spark.siteserver.api.BinaryOperation;
import com.egalacoral.spark.siteserver.api.ExistsFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Category;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventValidationResultDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeMinimalEventDto;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeServiceImpl;
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
public class CompetitionsValidateSiteServeIdsTest {

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
  public void testGetOneValidEventById() throws Exception {
    Event event =
        TestUtil.deserializeWithJackson(
            "controller/private_api/validateSSIds/event_from_ss.json", Event.class);
    when(siteServerApi.getEvent(eq(Collections.singletonList("8070616")), anyObject(), anyObject()))
        .thenReturn(Optional.of(Collections.singletonList(event)));
    SiteServeEventValidationResultDto result =
        competitionController.validateAndGetEventsById("bma", "8070616", false);

    List<SiteServeMinimalEventDto> expectedValid =
        Arrays.asList(new SiteServeMinimalEventDto("8070616", "Brighton vs Leicester City"));
    List<String> expectedInvalid = Collections.emptyList();
    SiteServeEventValidationResultDto expected =
        new SiteServeEventValidationResultDto(expectedValid, expectedInvalid);
    assertEquals(expected, result);
  }

  @Test
  public void testGetOneValidEventByIdOnlySpecial() throws Exception {
    Event event =
        TestUtil.deserializeWithJackson(
            "controller/private_api/validateSSIds/event_from_ss.json", Event.class);
    when(siteServerApi.getEvent(anyObject(), anyObject(), anyObject()))
        .thenReturn(Optional.of(Collections.singletonList(event)));
    SiteServeEventValidationResultDto result =
        competitionController.validateAndGetEventsById("bma", "8070616", true);

    ExistsFilter existsFilter =
        (ExistsFilter)
            new ExistsFilter.ExistsFilterBuilder()
                .addBinaryOperation(
                    "event:simpleFilter:market.drilldownTagNames",
                    BinaryOperation.intersects,
                    "MKTFLAG_SP")
                .build();

    verify(siteServerApi)
        .getEvent(
            eq(Collections.singletonList("8070616")),
            eq(Optional.empty()),
            eq(Optional.of(existsFilter)));
  }

  @Test
  public void testGetOneInvalidEventById() throws Exception {
    when(siteServerApi.getEvent(eq(Collections.singletonList("8070616")), anyObject(), anyObject()))
        .thenReturn(Optional.empty());
    SiteServeEventValidationResultDto result =
        competitionController.validateAndGetEventsById("bma", "8070616", false);

    List<SiteServeMinimalEventDto> expectedValid = Collections.emptyList();
    List<String> expectedInvalid = Arrays.asList("8070616");
    SiteServeEventValidationResultDto expected =
        new SiteServeEventValidationResultDto(expectedValid, expectedInvalid);
    assertEquals(expected, result);
  }

  @Test
  public void testGetEventByOneValidAndOneInvalidId() throws Exception {
    Event event =
        TestUtil.deserializeWithJackson(
            "controller/private_api/validateSSIds/event_from_ss.json", Event.class);
    when(siteServerApi.getEvent(eq(Arrays.asList("8070616", "8070617")), anyObject(), anyObject()))
        .thenReturn(Optional.of(Collections.singletonList(event)));
    SiteServeEventValidationResultDto result =
        competitionController.validateAndGetEventsById("bma", "8070616,8070617", false);

    List<SiteServeMinimalEventDto> expectedValid =
        Arrays.asList(new SiteServeMinimalEventDto("8070616", "Brighton vs Leicester City"));
    List<String> expectedInvalid = Arrays.asList("8070617");
    SiteServeEventValidationResultDto expected =
        new SiteServeEventValidationResultDto(expectedValid, expectedInvalid);
    assertEquals(expected, result);
  }

  @Test
  public void testGetEventsByTypeId() throws Exception {
    List<Event> events =
        TestUtil.deserializeListWithJackson(
            "controller/private_api/validateSSIds/events_by_type_from_ss.json", Event.class);
    when(siteServerApi.getEventForType(
            eq(Collections.singletonList("442")), anyObject(), anyObject(), eq(false)))
        .thenReturn(Optional.of(events));

    List<Category> categories =
        TestUtil.deserializeListWithJackson(
            "controller/private_api/validateSSIds/category_by_type_from_ss.json", Category.class);
    when(siteServerApi.getClassToSubTypeForType(eq("442"), anyObject()))
        .thenReturn(Optional.of(categories));

    SiteServeEventValidationResultDto result =
        competitionController.validateTypeAndGetEventsByType("bma", "442", false);

    List<SiteServeMinimalEventDto> expectedValid =
        Arrays.asList(new SiteServeMinimalEventDto("8068435", "Little Reds v Syria"));
    List<String> expectedInvalid = Collections.emptyList();
    SiteServeEventValidationResultDto expected =
        new SiteServeEventValidationResultDto(expectedValid, expectedInvalid);
    assertEquals(expected, result);
  }

  @Test
  public void testGetEventsByInvalidTypeId() throws Exception {
    when(siteServerApi.getEventForType(
            eq(Collections.singletonList("442")), anyObject(), anyObject(), eq(false)))
        .thenReturn(Optional.empty());

    when(siteServerApi.getClassToSubTypeForType(eq("442"), anyObject()))
        .thenReturn(Optional.empty());

    SiteServeEventValidationResultDto result =
        competitionController.validateTypeAndGetEventsByType("bma", "442", false);

    List<SiteServeMinimalEventDto> expectedValid = Collections.emptyList();
    List<String> expectedInvalid = Collections.singletonList("442");
    SiteServeEventValidationResultDto expected =
        new SiteServeEventValidationResultDto(expectedValid, expectedInvalid);
    assertEquals(expected, result);
  }

  @Test
  public void testGetEventsByOneValidAndOneInvalidTypeId() throws Exception {
    List<Category> categories =
        TestUtil.deserializeListWithJackson(
            "controller/private_api/validateSSIds/category_by_type_from_ss.json", Category.class);
    when(siteServerApi.getClassToSubTypeForType(eq("442"), anyObject()))
        .thenReturn(Optional.of(categories));
    when(siteServerApi.getClassToSubTypeForType(eq("443"), anyObject()))
        .thenReturn(Optional.empty());

    List<Event> events =
        TestUtil.deserializeListWithJackson(
            "controller/private_api/validateSSIds/events_by_type_from_ss.json", Event.class);
    when(siteServerApi.getEventForType(
            eq(Arrays.asList("442", "443")), anyObject(), anyObject(), eq(false)))
        .thenReturn(Optional.of(events));

    SiteServeEventValidationResultDto result =
        competitionController.validateTypeAndGetEventsByType("bma", "442,443", false);

    List<SiteServeMinimalEventDto> expectedValid =
        Arrays.asList(new SiteServeMinimalEventDto("8068435", "Little Reds v Syria"));
    List<String> expectedInvalid = Collections.singletonList("443");
    SiteServeEventValidationResultDto expected =
        new SiteServeEventValidationResultDto(expectedValid, expectedInvalid);
    assertEquals(expected, result);
  }
}
