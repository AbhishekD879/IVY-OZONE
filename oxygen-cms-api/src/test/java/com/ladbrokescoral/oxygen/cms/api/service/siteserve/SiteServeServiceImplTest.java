package com.ladbrokescoral.oxygen.cms.api.service.siteserve;

import static org.mockito.ArgumentMatchers.*;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.*;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventValidationResultDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.entity.TypeFlagCodes;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.NextRacesPublicService;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.NextEventsParameters.NextEventsParametersBuilder;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class SiteServeServiceImplTest {

  @Mock private SiteServeApiProvider siteServeApiProvider;

  @Mock private SiteServerApi api;

  @Test
  public void getNextRacesEvents() {
    Mockito.when(siteServeApiProvider.api("bma")).thenReturn(api);
    ArrayList<Category> categories = buildCategories();
    Mockito.when(api.getClasses(Mockito.any(), Mockito.any())).thenReturn(Optional.of(categories));
    ArrayList<Event> events = new ArrayList<>();
    events.add(buildEvent("1", "2020-03-26T15:30:00Z"));
    events.add(buildEvent("2", "2020-03-26T14:30:00Z"));
    Mockito.when(
            api.getEventToOutcomeForClass(
                Mockito.any(), Mockito.any(), Mockito.any(), Mockito.any()))
        .thenReturn(Optional.of(events));
    SiteServeServiceImpl service = new SiteServeServiceImpl(siteServeApiProvider);
    NextEventsParametersBuilder builder = NextEventsParameters.builder();
    builder.timePeriodMinutes(30);
    builder.categoryId(21);
    builder.comparator(NextRacesPublicService.START_TIME_COMPARATOR);
    builder.typeFlagCodes(TypeFlagCodes.of("INT"));
    builder.brand("bma");
    List<Event> resultedEvents = service.getNextEvents(builder.build());
    Assert.assertEquals(2, resultedEvents.size());
    Assert.assertEquals("2", resultedEvents.get(0).getId());
  }

  @Test
  public void testGetNextFiveMinsAndLiveEvents() {
    Mockito.when(siteServeApiProvider.api("ladbrokes")).thenReturn(api);
    Mockito.when(api.getEvent(Mockito.any(), Mockito.any(), Mockito.any()))
        .thenReturn(Optional.of(getEvents()));
    SiteServeServiceImpl service = new SiteServeServiceImpl(siteServeApiProvider);
    List<Event> resultedEvents =
        service.getNextFiveMinsAndLiveEvents("ladbrokes", 16, Arrays.asList("1"));
    Assert.assertEquals(4, resultedEvents.size());
  }

  @Test
  public void testValidateEventsByTypeId() {
    Mockito.when(siteServeApiProvider.api("ladbrokes")).thenReturn(api);
    Mockito.when(
            api.getEventForType(Mockito.any(), Mockito.any(), Mockito.any(), Mockito.anyBoolean()))
        .thenReturn(Optional.of(getEvents()));
    Mockito.when(api.getClassToSubTypeForType(Mockito.anyString(), Mockito.any()))
        .thenReturn(Optional.of(getCategories()));
    SiteServeServiceImpl service = new SiteServeServiceImpl(siteServeApiProvider);
    SiteServeEventValidationResultDto resultDto =
        service.validateEventsByTypeId("ladbrokes", Arrays.asList("1"), true);
    Assert.assertNotNull(resultDto);
  }

  @Test
  public void testValidateAndGetEventsById() {
    Mockito.when(siteServeApiProvider.api("ladbrokes")).thenReturn(api);
    Mockito.when(api.getEvent(Mockito.any(), Mockito.any(), Mockito.any()))
        .thenReturn(Optional.of(getEvents()));

    SiteServeServiceImpl service = new SiteServeServiceImpl(siteServeApiProvider);
    SiteServeEventValidationResultDto resultDto =
        service.validateAndGetEventsById("ladbrokes", Arrays.asList("1"), true);
    Assert.assertNotNull(resultDto);
  }

  @Test
  public void testValidateEventsByOutcomeId() {
    Mockito.when(siteServeApiProvider.api("ladbrokes")).thenReturn(api);
    Mockito.when(
            api.getEventToOutcomeForOutcome(
                Mockito.any(), Mockito.any(), Mockito.any(), Mockito.anyBoolean()))
        .thenReturn(Optional.of(getEvents()));

    SiteServeServiceImpl service = new SiteServeServiceImpl(siteServeApiProvider);
    SiteServeEventValidationResultDto resultDto =
        service.validateEventsByOutcomeId("ladbrokes", Arrays.asList("1"));
    Assert.assertNotNull(resultDto);
  }

  @Test
  public void anyLiveOrUpcomingEventsExists() {
    Mockito.when(siteServeApiProvider.api("ladbrokes")).thenReturn(api);
    Mockito.when(api.getClasses(Mockito.any(), Mockito.any()))
        .thenReturn(Optional.of(getCategories()));
    Mockito.when(
            api.getEventToOutcomeForClass(
                Mockito.any(),
                Mockito.any(),
                Mockito.any(),
                Mockito.any(),
                Mockito.any(),
                Mockito.any()))
        .thenReturn(Optional.of(getEvents()));
    SiteServeServiceImpl service = new SiteServeServiceImpl(siteServeApiProvider);
    Boolean result = service.anyLiveOrUpcomingEventsExists(getSportCategory());
    Assert.assertTrue(result);
  }

  SportCategory getSportCategory() {
    SportCategory sportCategory = new SportCategory();
    sportCategory.setBrand("ladbrokes");
    sportCategory.setCategoryId(1);
    return sportCategory;
  }

  List<Category> getCategories() {
    ArrayList<Category> categories = new ArrayList<>();
    Category cate1 = new Category();
    cate1.setId(1);
    cate1.setName("test");
    categories.add(cate1);
    return categories;
  }

  List<Event> getEvents() {
    ArrayList<Event> events = new ArrayList<>();
    events.add(buildEvent("1", "2020-03-26T15:30:00Z"));
    events.add(buildEvent("2", "2020-03-26T14:30:00Z"));
    return events;
  }

  private Event buildEvent(String id, String startTime) {
    Event event = new Event();
    event.setId(id);
    event.setName("test");
    event.setStartTime(startTime);
    Children children = new Children();
    children.setMarket(buildMarket(id));
    event.setChildren(Arrays.asList(children));
    return event;
  }

  private Market buildMarket(String id) {
    Market market = new Market();
    market.setId(id);
    market.setName("test");
    Children children = new Children();
    children.setOutcome(buildOutcome(id));
    market.setChildren(Arrays.asList(children));
    return market;
  }

  private Outcome buildOutcome(String id) {
    Outcome outcome = new Outcome();
    outcome.setId(id);
    outcome.setName("test");
    return outcome;
  }

  private ArrayList<Category> buildCategories() {
    ArrayList<Category> categories = new ArrayList<>();
    Category category = new Category();
    category.setId(12);
    categories.add(category);
    return categories;
  }

  @Test
  public void anyLiveOrUpcomingEventsExistsForGolf() {
    Mockito.when(siteServeApiProvider.api("ladbrokes")).thenReturn(api);
    Mockito.when(api.getClasses(any(), any())).thenReturn(Optional.of(getCategories()));
    Mockito.when(
            api.getEventToOutcomeForClass(
                Mockito.any(), Mockito.any(), Mockito.any(), Mockito.any(), Mockito.anyList()))
        .thenReturn(Optional.of(getEvents()));
    SiteServeServiceImpl service = new SiteServeServiceImpl(siteServeApiProvider);
    boolean result = service.anyUpcomingEventsExistsForGolf(getSportCategory());
    Assert.assertTrue(result);
  }

  @Test
  public void anyUpcomingEvents() {
    Mockito.when(siteServeApiProvider.api("ladbrokes")).thenReturn(api);
    Mockito.when(api.getClasses(any(), any())).thenReturn(Optional.of(getCategories()));
    Mockito.when(
            api.getEventToOutcomeForClass(
                Mockito.any(), Mockito.any(), Mockito.any(), Mockito.any(), Mockito.anyList()))
        .thenReturn(Optional.empty());
    SiteServeServiceImpl service = new SiteServeServiceImpl(siteServeApiProvider);
    boolean result = service.anyUpcomingEventsExistsForGolf(getSportCategory());
    Assert.assertFalse(result);
  }

  @Test
  public void anyUpcomingEventsActiveClassesNull() {
    Mockito.when(siteServeApiProvider.api("ladbrokes")).thenReturn(api);
    List<Category> categories = new ArrayList<>();
    Mockito.when(api.getClasses(any(), any())).thenReturn(Optional.of(categories));
    SiteServeServiceImpl service = new SiteServeServiceImpl(siteServeApiProvider);
    boolean result = service.anyUpcomingEventsExistsForGolf(getSportCategory());
    Assert.assertFalse(result);
  }

  @Test
  public void anyUpcomingEventsActiveClassesForMatchesTabNull() {
    Mockito.when(siteServeApiProvider.api("ladbrokes")).thenReturn(api);
    List<Category> categories = new ArrayList<>();
    Mockito.when(api.getClasses(any(), any())).thenReturn(Optional.of(categories));
    SiteServeServiceImpl service = new SiteServeServiceImpl(siteServeApiProvider);
    boolean result = service.anyUpcomingEventsExistsForMatchesTabGolf(getSportCategory());
    Assert.assertFalse(result);
  }

  @Test
  public void anyUpcomingEventsExistsForGolfUpcomingTrue() {
    Mockito.when(siteServeApiProvider.api("ladbrokes")).thenReturn(api);
    Mockito.when(api.getClasses(any(), any())).thenReturn(Optional.of(getCategories()));
    List<Event> list = new ArrayList<>();
    Mockito.when(
            api.getEventToOutcomeForClass(
                Mockito.any(), Mockito.any(), Mockito.any(), Mockito.any(), Mockito.anyList()))
        .thenReturn(Optional.of(getEvents()));
    SiteServeServiceImpl service = new SiteServeServiceImpl(siteServeApiProvider);
    boolean result = service.anyUpcomingEventsExistsForGolf(getSportCategory());
    Assert.assertTrue(result);
  }

  @Test
  public void anyUpcomingEventsExistsForGolfMatchesTabUpcomingTrue() {
    Mockito.when(siteServeApiProvider.api("ladbrokes")).thenReturn(api);
    Mockito.when(api.getClasses(any(), any())).thenReturn(Optional.of(getCategories()));
    Mockito.when(
            api.getEventToOutcomeForClass(
                Mockito.any(), Mockito.any(), Mockito.any(), Mockito.any(), Mockito.anyList()))
        .thenReturn(Optional.of(getEvents()));
    SiteServeServiceImpl service = new SiteServeServiceImpl(siteServeApiProvider);
    boolean result = service.anyUpcomingEventsExistsForMatchesTabGolf(getSportCategory());
    Assert.assertTrue(result);
  }

  @Test
  public void anyUpcomingEventsExistsForGolfUpcomingFalse() {
    Mockito.when(siteServeApiProvider.api("ladbrokes")).thenReturn(api);
    Mockito.when(api.getClasses(any(), any())).thenReturn(Optional.of(getCategories()));
    Optional<List<Event>> list = Optional.empty();

    Mockito.when(
            api.getEventToOutcomeForClass(
                Mockito.any(), Mockito.any(), Mockito.any(), Mockito.any(), Mockito.anyList()))
        .thenReturn(Optional.empty());
    SiteServeServiceImpl service = new SiteServeServiceImpl(siteServeApiProvider);
    boolean result = service.anyUpcomingEventsExistsForGolf(getSportCategory());
    Assert.assertFalse(result);
  }

  @Test
  public void anyUpcomingEventsExistsForGolfMatchesTabUpcomingFalse() {
    Mockito.when(siteServeApiProvider.api("ladbrokes")).thenReturn(api);
    Mockito.when(api.getClasses(any(), any())).thenReturn(Optional.of(getCategories()));
    List<Event> list = new ArrayList<>();
    Mockito.when(
            api.getEventToOutcomeForClass(
                Mockito.any(), Mockito.any(), Mockito.any(), Mockito.any(), Mockito.anyList()))
        .thenReturn(Optional.empty());
    SiteServeServiceImpl service = new SiteServeServiceImpl(siteServeApiProvider);
    boolean result = service.anyUpcomingEventsExistsForMatchesTabGolf(getSportCategory());
    Assert.assertFalse(result);
  }

  @Test
  public void anyLiveOrTodayUpcomingEventsExistsForGolfLiveFalseUpcomingTrue() {
    Mockito.when(siteServeApiProvider.api("ladbrokes")).thenReturn(api);
    Mockito.when(api.getClasses(any(), any())).thenReturn(Optional.of(getCategories()));
    List<Event> list = new ArrayList<>();
    Mockito.when(
            api.getEventToOutcomeForClass(
                Mockito.any(), Mockito.any(), Mockito.any(), Mockito.any(), Mockito.anyList()))
        .thenReturn(Optional.empty())
        .thenReturn(Optional.of(getEvents()));
    SiteServeServiceImpl service = new SiteServeServiceImpl(siteServeApiProvider);
    boolean result = service.anyLiveOrUpcomingTodaysEventsExistsForGolf(getSportCategory());
    Assert.assertTrue(result);
  }

  @Test
  public void anyLiveOrTodayUpcomingEventsExistsForGolfLiveTrueUpcomingTrue() {
    Mockito.when(siteServeApiProvider.api("ladbrokes")).thenReturn(api);
    Mockito.when(api.getClasses(any(), any())).thenReturn(Optional.of(getCategories()));
    Mockito.when(
            api.getEventToOutcomeForClass(
                Mockito.any(), Mockito.any(), Mockito.any(), Mockito.any(), Mockito.anyList()))
        .thenReturn(Optional.of(getEvents()))
        .thenReturn(Optional.of(getEvents()));
    SiteServeServiceImpl service = new SiteServeServiceImpl(siteServeApiProvider);
    boolean result = service.anyLiveOrUpcomingTodaysEventsExistsForGolf(getSportCategory());
    Assert.assertTrue(result);
  }

  @Test
  public void anyLiveOrTodayUpcomingEventsExistsForGolfLiveTrueUpcomingFalse() {

    Mockito.when(siteServeApiProvider.api("ladbrokes")).thenReturn(api);
    Mockito.when(api.getClasses(any(), any())).thenReturn(Optional.of(getCategories()));
    List<Event> list = new ArrayList<>();
    Mockito.when(
            api.getEventToOutcomeForClass(
                Mockito.any(), Mockito.any(), Mockito.any(), Mockito.any(), Mockito.anyList()))
        .thenReturn(Optional.of(getEvents()))
        .thenReturn(Optional.empty());
    SiteServeServiceImpl service = new SiteServeServiceImpl(siteServeApiProvider);
    boolean result = service.anyLiveOrUpcomingTodaysEventsExistsForGolf(getSportCategory());
    Assert.assertTrue(result);
  }

  @Test
  public void anyLiveOrTodayEventsExistsForGolfLiveFalseUpcomingFalse() {
    Mockito.when(siteServeApiProvider.api("ladbrokes")).thenReturn(api);
    Mockito.when(api.getClasses(any(), any())).thenReturn(Optional.of(getCategories()));
    Mockito.when(
            api.getEventToOutcomeForClass(
                Mockito.any(), Mockito.any(), Mockito.any(), Mockito.any(), Mockito.anyList()))
        .thenReturn(Optional.of(new ArrayList<>()))
        .thenReturn(Optional.of(new ArrayList<>()));
    SiteServeServiceImpl service = new SiteServeServiceImpl(siteServeApiProvider);
    boolean result = service.anyLiveOrUpcomingTodaysEventsExistsForGolf(getSportCategory());
    Assert.assertFalse(result);
  }

  @Test
  public void anyLiveEventsActiveClassesNull() {
    Mockito.when(siteServeApiProvider.api("ladbrokes")).thenReturn(api);
    List<Category> categories = new ArrayList<>();
    Mockito.when(api.getClasses(any(), any())).thenReturn(Optional.of(categories));
    SiteServeServiceImpl service = new SiteServeServiceImpl(siteServeApiProvider);
    boolean result = service.anyLiveOrUpcomingTodaysEventsExistsForGolf(getSportCategory());
    Assert.assertFalse(result);
  }

  @Test
  public void anyUpcomingEventsLiveTrueUpcomingFalse() {

    Mockito.when(siteServeApiProvider.api("ladbrokes")).thenReturn(api);
    Mockito.when(api.getClasses(any(), any())).thenReturn(Optional.of(getCategories()));
    List<Event> list = new ArrayList<>();
    Mockito.when(
            api.getEventToOutcomeForClass(
                Mockito.any(),
                Mockito.any(),
                Mockito.any(),
                Mockito.any(),
                Mockito.any(),
                Mockito.any()))
        .thenReturn(Optional.of(getEvents()))
        .thenReturn(Optional.of(list));
    SiteServeServiceImpl service = new SiteServeServiceImpl(siteServeApiProvider);
    boolean result = service.anyLiveOrUpcomingEventsExists(getSportCategory());
    Assert.assertTrue(result);
  }

  @Test
  public void anyUpcomingEventsLiveTrueUpcomingTrue() {

    Mockito.when(siteServeApiProvider.api("ladbrokes")).thenReturn(api);
    Mockito.when(api.getClasses(any(), any())).thenReturn(Optional.of(getCategories()));
    Mockito.when(
            api.getEventToOutcomeForClass(
                Mockito.any(),
                Mockito.any(),
                Mockito.any(),
                Mockito.any(),
                Mockito.any(),
                Mockito.any()))
        .thenReturn(Optional.of(getEvents()))
        .thenReturn(Optional.of(getEvents()));
    SiteServeServiceImpl service = new SiteServeServiceImpl(siteServeApiProvider);
    boolean result = service.anyLiveOrUpcomingEventsExists(getSportCategory());
    Assert.assertTrue(result);
  }

  @Test
  public void anyUpcomingEventsFalseTrueUpcomingTrue() {

    Mockito.when(siteServeApiProvider.api("ladbrokes")).thenReturn(api);
    Mockito.when(api.getClasses(any(), any())).thenReturn(Optional.of(getCategories()));
    List<Event> list = new ArrayList<>();
    Mockito.when(
            api.getEventToOutcomeForClass(
                Mockito.any(),
                Mockito.any(),
                Mockito.any(),
                Mockito.any(),
                Mockito.any(),
                Mockito.any()))
        .thenReturn(Optional.of(list))
        .thenReturn(Optional.of(getEvents()));
    SiteServeServiceImpl service = new SiteServeServiceImpl(siteServeApiProvider);
    boolean result = service.anyLiveOrUpcomingEventsExists(getSportCategory());
    Assert.assertTrue(result);
  }

  @Test
  public void anyUpcomingEventsFlaseTrueUpcomingFalse() {

    Mockito.when(siteServeApiProvider.api("ladbrokes")).thenReturn(api);
    Mockito.when(api.getClasses(any(), any())).thenReturn(Optional.of(getCategories()));
    List<Event> list = new ArrayList<>();
    Mockito.when(
            api.getEventToOutcomeForClass(
                Mockito.any(),
                Mockito.any(),
                Mockito.any(),
                Mockito.any(),
                Mockito.any(),
                Mockito.any()))
        .thenReturn(Optional.of(list))
        .thenReturn(Optional.of(list));
    SiteServeServiceImpl service = new SiteServeServiceImpl(siteServeApiProvider);
    boolean result = service.anyLiveOrUpcomingEventsExists(getSportCategory());
    Assert.assertFalse(result);
  }

  @Test
  public void anyLiveOrUpcomingEventsExistsClassesNull() {
    Mockito.when(siteServeApiProvider.api("ladbrokes")).thenReturn(api);
    List<Category> categories = new ArrayList<>();
    Mockito.when(api.getClasses(any(), any())).thenReturn(Optional.of(categories));
    SiteServeServiceImpl service = new SiteServeServiceImpl(siteServeApiProvider);
    boolean result = service.anyLiveOrUpcomingEventsExists(getSportCategory());
    Assert.assertFalse(result);
  }

  @Test
  public void anyLiveOrUpcomingEventsExistsClassesNotNull() {
    Mockito.when(siteServeApiProvider.api("ladbrokes")).thenReturn(api);
    List<Category> categories = new ArrayList<>();
    Mockito.when(api.getClasses(any(), any())).thenReturn(Optional.of(getCategories()));
    SiteServeServiceImpl service = new SiteServeServiceImpl(siteServeApiProvider);
    boolean result = service.anyLiveOrUpcomingEventsExists(getSportCategory());
    Assert.assertFalse(result);
  }

  @Test
  public void findPreviousEventsByCategoryIdTest() {
    Mockito.when(siteServeApiProvider.api("ladbrokes")).thenReturn(api);
    SiteServeServiceImpl service = new SiteServeServiceImpl(siteServeApiProvider);
    Mockito.when(api.getEvent(any(), any(), any())).thenReturn(Optional.ofNullable(getEvents()));
    Optional<List<Event>> result = service.findPreviousEventsByCategoryId("ladbrokes", 1);
    boolean a = result.get().isEmpty();
    Assert.assertFalse(a);
  }

  @Test
  public void anyUpcomingEventsForMatchesTabListEmpty() {
    Mockito.when(siteServeApiProvider.api("ladbrokes")).thenReturn(api);

    Mockito.when(api.getClasses(any(), any())).thenReturn(Optional.of(getCategories()));
    Mockito.when(
            api.getEventToOutcomeForClass(
                Mockito.any(), Mockito.any(), Mockito.any(), Mockito.any(), Mockito.anyList()))
        .thenReturn(Optional.of(new ArrayList<>()));
    SiteServeServiceImpl service = new SiteServeServiceImpl(siteServeApiProvider);
    boolean result = service.anyUpcomingEventsExistsForMatchesTabGolf(getSportCategory());
    Assert.assertFalse(result);
  }

  @Test
  public void anyUpcomingEventsExistsForGolfTabListEmpty() {
    Mockito.when(siteServeApiProvider.api("ladbrokes")).thenReturn(api);

    Mockito.when(api.getClasses(any(), any())).thenReturn(Optional.of(getCategories()));
    Mockito.when(
            api.getEventToOutcomeForClass(
                Mockito.any(), Mockito.any(), Mockito.any(), Mockito.any(), Mockito.anyList()))
        .thenReturn(Optional.of(new ArrayList<>()));
    SiteServeServiceImpl service = new SiteServeServiceImpl(siteServeApiProvider);
    boolean result = service.anyUpcomingEventsExistsForGolf(getSportCategory());
    Assert.assertFalse(result);
  }
}
