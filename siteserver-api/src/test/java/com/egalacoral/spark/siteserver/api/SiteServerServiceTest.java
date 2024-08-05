package com.egalacoral.spark.siteserver.api;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;
import static org.mockito.Mockito.when;
import static org.mockserver.model.HttpRequest.request;
import static org.mockserver.model.HttpResponse.response;

import com.egalacoral.spark.siteserver.api.ExistsFilter.ExistsFilterBuilder;
import com.egalacoral.spark.siteserver.api.SimpleFilter.SimpleFilterBuilder;
import com.egalacoral.spark.siteserver.api.SiteServerApi.Builder;
import com.egalacoral.spark.siteserver.api.SiteServerApi.Level;
import com.egalacoral.spark.siteserver.model.*;
import com.egalacoral.spark.siteserver.parameter.RacingForm;
import java.io.IOException;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.EnumSet;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.stream.Collectors;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

/** Created by oleg.perushko@symphony-solutions.eu on 8/3/16 */
public class SiteServerServiceTest extends BasicIntegrationMock {

  private final String basePath = "/openbet-ssviewer/Drilldown/2.27";
  private final String basePathHistoricDrilldown = "/openbet-ssviewer/HistoricDrilldown/2.27";
  private SiteServerApi api;
  private Market market;

  @Before
  public void setUp() throws Exception {
    api =
        new Builder()
            .setUrl("http://127.0.0.1:8443")
            .setLoggingLevel(Level.BODY)
            .setConnectionTimeout(1)
            .setReadTimeout(1)
            .setMaxNumberOfRetries(1)
            .setVersion("2.27")
            .build();
  }

  @Test
  public void testNext3Events() {
    mockNext3Events("response/getNext3Events.json");
    Optional<List<Event>> nextNEventsForClass = requestNextNEvents(3);

    Assert.assertTrue(nextNEventsForClass.isPresent());
    List<Event> events = nextNEventsForClass.get();
    Assert.assertEquals(6, events.size());
  }

  @Test
  public void getReferenceEachWayTerms() {
    ReferenceEachWayTerms referenceEachWayTerms = new ReferenceEachWayTerms();
    referenceEachWayTerms.setId("1");
    referenceEachWayTerms.setPlaces(4);
    Children children = new Children();
    children.setReferenceEachWayTerms(referenceEachWayTerms);
    List<Children> childrenList = new ArrayList<>();
    childrenList.add(children);
    IdentityWithChildren identity =
        Mockito.mock(IdentityWithChildren.class, Mockito.CALLS_REAL_METHODS);
    identity.setChildren(childrenList);
    Market market = new Market();
    when(identity.getConcreteChildren(Children::getReferenceEachWayTerms))
        .thenReturn(Arrays.asList(referenceEachWayTerms));
    List<ReferenceEachWayTerms> referenceEachWayTermsList1 = market.getReferenceEachWayTerms();

    Assert.assertNotNull(referenceEachWayTerms);
  }

  @Test
  public void testNext3EventsWithEmptyClassIds() {
    Optional<List<Event>> nextNEventsForClass =
        requestNextNEventsWithReferenceEachwayTermsWithEmptyClassIds(3);
    Optional<List<Event>> nextNEventsForClass1 =
        requestNextNEventsWithReferenceEachwayTermsWithClassIdsNull(3);
    Assert.assertFalse(nextNEventsForClass.isPresent());
  }

  @Test
  public void testNext3EventsWithEmptyConfiguredNextNValues() {
    List<Integer> emptyConfiguredNextNValues = new ArrayList<>();

    try {
      SiteServerApi api1 =
          new Builder()
              .setUrl("http://127.0.0.1:8443")
              .setLoggingLevel(Level.BODY)
              .setConnectionTimeout(1)
              .setReadTimeout(1)
              .setMaxNumberOfRetries(2)
              .setVersion("2.27")
              .setConfiguredNextNValues(emptyConfiguredNextNValues)
              .build();
      Optional<List<Event>> nextNEventsForClass =
          api1.getNextNEventsForClass(
              3,
              Arrays.asList("288", "287", "999"),
              (SimpleFilter) new SimpleFilterBuilder().build(),
              new ExistsFilterBuilder().build(),
              false,
              true);
      Assert.assertFalse(nextNEventsForClass.isPresent());
    } catch (NoSuchAlgorithmException e) {
    } catch (KeyManagementException f) {
    }
  }

  @Test
  public void testNext3EventsWithReferenceEachWayTerms() {
    mockNext3EventsWithReferenceEachWayTerms("response/getNext3Events.json");
    Optional<List<Event>> nextNEventsForClass = requestNextNEventsWithReferenceEachwayTerms(3);

    Assert.assertTrue(nextNEventsForClass.isPresent());
    List<Event> events = nextNEventsForClass.get();
    Assert.assertEquals(6, events.size());
  }

  @Test
  public void testLessThen3EventsRequested() {
    mockNext3Events("response/getNext3Events.json");
    Optional<List<Event>> nextNEventsForClass = requestNextNEvents(2);
    Assert.assertTrue(nextNEventsForClass.isPresent());
    List<Event> events = nextNEventsForClass.get();
    Assert.assertEquals(4, events.size());
  }

  @Test
  public void testLessThen3EventsRequestedWithReferenceEachWayTerms() {
    mockNext3EventsWithReferenceEachWayTerms("response/getNext3Events.json");
    Optional<List<Event>> nextNEventsForClass = requestNextNEventsWithReferenceEachwayTerms(2);
    Assert.assertTrue(nextNEventsForClass.isPresent());
    List<Event> events = nextNEventsForClass.get();
    Assert.assertEquals(4, events.size());
  }

  @Test
  public void testTrimmingToRequestedNMaintainsOrderByStartTime() {
    mockNext3Events("response/getNext3Events.json");
    Optional<List<Event>> nextNTrimmed = requestNextNEvents(1);
    Optional<List<Event>> nextNFull = requestNextNEvents(3);
    Assert.assertTrue(nextNTrimmed.isPresent());
    List<Event> events = nextNTrimmed.get();
    Assert.assertEquals(2, events.size());

    Map<String, List<Event>> fullGroupedByClassId =
        nextNFull.get().stream().collect(Collectors.groupingBy(Event::getClassId));

    Map<String, List<Event>> trimmedGroupedByClassId =
        nextNTrimmed.get().stream().collect(Collectors.groupingBy(Event::getClassId));

    Assert.assertEquals(3, fullGroupedByClassId.get("288").size());
    Assert.assertEquals(1, trimmedGroupedByClassId.get("288").size());

    Assert.assertEquals("229415878", trimmedGroupedByClassId.get("288").get(0).getId());
  }

  @Test
  public void testTrimmingToRequestedNMaintainsOrderByStartTimeWithReferenceEachWayTerms() {
    mockNext3EventsWithReferenceEachWayTerms("response/getNext3Events.json");
    Optional<List<Event>> nextNTrimmed = requestNextNEventsWithReferenceEachwayTerms(1);
    Optional<List<Event>> nextNFull = requestNextNEventsWithReferenceEachwayTerms(3);
    Assert.assertTrue(nextNTrimmed.isPresent());
    List<Event> events = nextNTrimmed.get();
    Assert.assertEquals(2, events.size());

    Map<String, List<Event>> fullGroupedByClassId =
        nextNFull.get().stream().collect(Collectors.groupingBy(Event::getClassId));

    Map<String, List<Event>> trimmedGroupedByClassId =
        nextNTrimmed.get().stream().collect(Collectors.groupingBy(Event::getClassId));

    Assert.assertEquals(3, fullGroupedByClassId.get("288").size());
    Assert.assertEquals(1, trimmedGroupedByClassId.get("288").size());

    Assert.assertEquals("229415878", trimmedGroupedByClassId.get("288").get(0).getId());
  }

  @Test
  public void testTrimmingWhenNoEventsReturned() {
    mockNext3Events("response/emptyResponse.json");
    Optional<List<Event>> nextNEventsForClass = requestNextNEvents(2);
    Assert.assertTrue(nextNEventsForClass.isPresent());
    Assert.assertTrue(nextNEventsForClass.get().isEmpty());
  }

  @Test
  public void testTrimmingWhenNoEventsReturnedWithReferenceEachWayTerms() {
    mockNext3EventsWithReferenceEachWayTerms("response/emptyResponse.json");
    Optional<List<Event>> nextNEventsForClass = requestNextNEventsWithReferenceEachwayTerms(2);
    Assert.assertTrue(nextNEventsForClass.isPresent());
    Assert.assertTrue(nextNEventsForClass.get().isEmpty());
  }

  @Test
  public void testWrongNInObRequest() {
    mockNext3Events("response/invalidNParam.json");
    Optional<List<Event>> nextNEventsForClass = requestNextNEvents(2);
    Assert.assertTrue(nextNEventsForClass.isPresent());
    Assert.assertTrue(nextNEventsForClass.get().isEmpty());
  }

  @Test
  public void testWrongNInObRequestWithReferenceEachWayTerms() {
    mockNext3EventsWithReferenceEachWayTerms("response/invalidNParam.json");
    Optional<List<Event>> nextNEventsForClass = requestNextNEventsWithReferenceEachwayTerms(2);
    Assert.assertTrue(nextNEventsForClass.isPresent());
    Assert.assertTrue(nextNEventsForClass.get().isEmpty());
  }

  @Test
  public void testZeroNextEventsRequested() {
    Assert.assertFalse(requestNextNEvents(0).isPresent());
    Assert.assertFalse(requestNextNEvents(-1).isPresent());
  }

  @Test
  public void testZeroNextEventsRequestedWithReferenceEachWayTerms() {
    Assert.assertFalse(requestNextNEventsWithReferenceEachwayTerms(0).isPresent());
    Assert.assertFalse(requestNextNEventsWithReferenceEachwayTerms(-1).isPresent());
    Assert.assertFalse(requestNextNEventsWithReferenceEachwayTerms(15).isPresent());
  }

  private Optional<List<Event>> requestNextNEvents(int N) {
    return api.getNextNEventsForClass(
        N,
        Arrays.asList("288", "287", "999"),
        (SimpleFilter) new SimpleFilterBuilder().build(),
        new ExistsFilterBuilder().build(),
        false);
  }

  private Optional<List<Event>> requestNextNEventsWithReferenceEachwayTerms(int N) {
    return api.getNextNEventsForClass(
        N,
        Arrays.asList("288", "287", "999"),
        (SimpleFilter) new SimpleFilterBuilder().build(),
        new ExistsFilterBuilder().build(),
        false,
        true);
  }

  private Optional<List<Event>> requestNextNEventsWithReferenceEachwayTermsWithEmptyClassIds(
      int N) {
    List<String> emptylist = new ArrayList<>();
    return api.getNextNEventsForClass(
        N,
        emptylist,
        (SimpleFilter) new SimpleFilterBuilder().build(),
        new ExistsFilterBuilder().build(),
        false,
        true);
  }

  private Optional<List<Event>> requestNextNEventsWithReferenceEachwayTermsWithClassIdsNull(int N) {
    return api.getNextNEventsForClass(
        N,
        null,
        (SimpleFilter) new SimpleFilterBuilder().build(),
        new ExistsFilterBuilder().build(),
        false,
        true);
  }

  private void mockNext3Events(String responseFileName) {
    mock.when(
            request()
                .withMethod("GET")
                .withPath(basePath + "/NextNEventForClass/3/288,287,999")
                .withQueryStringParameter("translationLang", "en")
                .withQueryStringParameter("includeUndisplayed", "false"))
        .respond(
            response()
                .withStatusCode(200)
                .withBody(this.getResourceFileAsString(responseFileName)));
  }

  private void mockNext3EventsWithReferenceEachWayTerms(String responseFileName) {
    mock.when(
            request()
                .withMethod("GET")
                .withPath(basePath + "/NextNEventForClass/3/288,287,999")
                .withQueryStringParameter("translationLang", "en")
                .withQueryStringParameter("includeUndisplayed", "false")
                .withQueryStringParameter("referenceEachWayTerms", "true"))
        .respond(
            response()
                .withStatusCode(200)
                .withBody(this.getResourceFileAsString(responseFileName)));
  }

  private void mockNext3EventsWithReferenceEachWayTermsWithEmptyClassIds(String responseFileName) {
    mock.when(
            request()
                .withMethod("GET")
                .withPath(basePath + "/NextNEventForClass/3/")
                .withQueryStringParameter("translationLang", "en")
                .withQueryStringParameter("includeUndisplayed", "false")
                .withQueryStringParameter("referenceEachWayTerms", "true"))
        .respond(
            response()
                .withStatusCode(200)
                .withBody(this.getResourceFileAsString(responseFileName)));
  }

  @Test
  public void testEventForType()
      throws IOException, NoSuchAlgorithmException, KeyManagementException {
    final String serviceName = "EventForType";
    mock.when(
            request()
                .withMethod("GET")
                .withPath(basePath + "/" + serviceName + "/442")
                .withQueryStringParameter("translationLang", "en")
                .withQueryStringParameter("includeUndisplayed", "true"))
        .respond(
            response()
                .withStatusCode(200)
                .withBody(this.getResourceFileAsString("response/getEventForType.json")));

    final SimpleFilter simpleFilter = (SimpleFilter) new SimpleFilter.SimpleFilterBuilder().build();

    Optional<List<Event>> events = api.getEventForType("442", simpleFilter);
    assertEquals(true, events.isPresent());
    assertEquals(12, events.get().size());
  }

  @Test
  public void testEventToOutcomeForClassWithReferenceEachWayTerms()
      throws IOException, NoSuchAlgorithmException, KeyManagementException {
    final String serviceName = "EventToOutcomeForClass";
    mock.when(
            request()
                .withMethod("GET")
                .withPath(basePath + "/" + serviceName + "/123")
                .withQueryStringParameter("translationLang", "en")
                .withQueryStringParameter("referenceEachWayTerms", "true"))
        .respond(
            response()
                .withStatusCode(200)
                .withBody(this.getResourceFileAsString("response/getEventForType.json")));

    List<String> classIds = new ArrayList<>();
    classIds.add("123");
    final SimpleFilter simpleFilter = (SimpleFilter) new SimpleFilter.SimpleFilterBuilder().build();
    final LimitToFilter limitToFilter =
        (LimitToFilter) new LimitToFilter.LimitToFilterBuilder().build();
    final ExistsFilter existsFilter = (ExistsFilter) new ExistsFilter.ExistsFilterBuilder().build();

    Optional<List<Event>> events =
        api.getEventToOutcomeForClass(classIds, simpleFilter, limitToFilter, existsFilter, true);
    assertEquals(true, events.isPresent());
  }

  @Test
  public void testEventToOutcomeForClassWithReferenceEachWayTermsWithPrune()
      throws IOException, NoSuchAlgorithmException, KeyManagementException {
    final String serviceName = "EventToOutcomeForClass";
    mock.when(
            request()
                .withMethod("GET")
                .withPath(basePath + "/" + serviceName + "/123")
                .withQueryStringParameter("translationLang", "en")
                .withQueryStringParameter("referenceEachWayTerms", "true"))
        .respond(
            response()
                .withStatusCode(200)
                .withBody(this.getResourceFileAsString("response/getEventForType.json")));

    List<String> classIds = new ArrayList<>();
    classIds.add("123");
    final SimpleFilter simpleFilter = (SimpleFilter) new SimpleFilter.SimpleFilterBuilder().build();
    final LimitToFilter limitToFilter =
        (LimitToFilter) new LimitToFilter.LimitToFilterBuilder().build();
    final LimitRecordsFilter limitRecordsFilter =
        (LimitRecordsFilter) new LimitRecordsFilter.LimitRecordsFilterBuilder().build();
    final ExistsFilter existsFilter = (ExistsFilter) new ExistsFilter.ExistsFilterBuilder().build();
    List<String> prune = new ArrayList<>();
    Optional<List<Event>> events =
        api.getEventToOutcomeForClass(
            classIds, simpleFilter, limitToFilter, limitRecordsFilter, existsFilter, prune, true);
    assertEquals(true, events.isPresent());
  }

  @Test
  public void testEventToOutcomeForClassWithReferenceEachWayTermsWithPruneWithExternalKeys()
      throws IOException, NoSuchAlgorithmException, KeyManagementException {
    final String serviceName = "EventToOutcomeForClass";
    mock.when(
            request()
                .withMethod("GET")
                .withPath(basePath + "/" + serviceName + "/123")
                .withQueryStringParameter("translationLang", "en")
                .withQueryStringParameter("referenceEachWayTerms", "true"))
        .respond(
            response()
                .withStatusCode(200)
                .withBody(this.getResourceFileAsString("response/getEventForType.json")));

    List<String> classIds = new ArrayList<>();
    classIds.add("123");
    final SimpleFilter simpleFilter = (SimpleFilter) new SimpleFilter.SimpleFilterBuilder().build();
    final LimitToFilter limitToFilter =
        (LimitToFilter) new LimitToFilter.LimitToFilterBuilder().build();
    final LimitRecordsFilter limitRecordsFilter =
        (LimitRecordsFilter) new LimitRecordsFilter.LimitRecordsFilterBuilder().build();
    final ExistsFilter existsFilter = (ExistsFilter) new ExistsFilter.ExistsFilterBuilder().build();
    List<String> prune = new ArrayList<>();
    Optional<List<Children>> children =
        api.getEventToOutcomeForClass(
            classIds,
            simpleFilter,
            limitToFilter,
            limitRecordsFilter,
            existsFilter,
            prune,
            "",
            true);
    assertEquals(true, children.isPresent());
  }

  @Test
  public void testEventForObClass()
      throws IOException, NoSuchAlgorithmException, KeyManagementException {
    final String serviceName = "EventForClass";
    mock.when(
            request()
                .withMethod("GET")
                .withPath(basePath + "/" + serviceName + "/115")
                .withQueryStringParameter("translationLang", "en")
                .withQueryStringParameter("includeUndisplayed", "true"))
        .respond(
            response()
                .withStatusCode(200)
                .withBody(this.getResourceFileAsString("response/getEventForClass.json")));

    final SimpleFilter simpleFilter = (SimpleFilter) new SimpleFilter.SimpleFilterBuilder().build();

    Optional<List<Event>> events = api.getEventForOBClass("115", simpleFilter);
    assertEquals(true, events.isPresent());
    assertEquals(45, events.get().size());
  }

  @Test
  public void testEventForOBClass()
      throws IOException, NoSuchAlgorithmException, KeyManagementException {
    final String serviceName = "EventForClass";
    mock.when(
            request()
                .withMethod("GET")
                .withPath(basePath + "/" + serviceName + "/115")
                .withQueryStringParameter("translationLang", "en")
                .withQueryStringParameter("includeUndisplayed", "true"))
        .respond(
            response()
                .withStatusCode(200)
                .withBody(this.getResourceFileAsString("response/getEventForClass.json")));

    final SimpleFilter simpleFilter = (SimpleFilter) new SimpleFilter.SimpleFilterBuilder().build();

    Optional<List<Event>> events =
        api.getEventByClass(
            Arrays.asList("115"), Optional.of(simpleFilter), Optional.empty(), true);
    assertEquals(true, events.isPresent());
    assertEquals(45, events.get().size());
  }

  @Test
  public void testGetEventToMarketForClass()
      throws IOException, NoSuchAlgorithmException, KeyManagementException {
    final String serviceName = "EventToMarketForClass";
    mock.when(
            request()
                .withMethod("GET")
                .withPath(basePath + "/" + serviceName + "/115")
                .withQueryStringParameter("translationLang", "en")
                .withQueryStringParameter("includeUndisplayed", "true"))
        .respond(
            response()
                .withStatusCode(200)
                .withBody(this.getResourceFileAsString("response/getEventToMarketForClass.json")));

    final SiteServerApi api =
        new SiteServerApi.Builder()
            .setUrl("http://127.0.0.1:8443")
            .setLoggingLevel(SiteServerApi.Level.BODY)
            .setConnectionTimeout(1)
            .setReadTimeout(1)
            .setMaxNumberOfRetries(1)
            .setVersion("2.27")
            .build();

    final SimpleFilter simpleFilter = (SimpleFilter) new SimpleFilter.SimpleFilterBuilder().build();

    Optional<List<Event>> events =
        api.getEventToMarketForClass(
            Arrays.asList("115"), Optional.of(simpleFilter), Optional.empty(), true);
    assertEquals(true, events.isPresent());
    assertEquals(45, events.get().size());
  }

  @Test
  public void testEventsForCategory()
      throws IOException, NoSuchAlgorithmException, KeyManagementException {
    final String serviceName = "Event";
    mock.when(
            request()
                .withMethod("GET")
                .withPath(basePath + "/" + serviceName)
                .withQueryStringParameter("translationLang", "en")
                .withQueryStringParameter("includeUndisplayed", "true")
                .withQueryStringParameter("simpleFilter", "event.categoryId:equals:16"))
        .respond(
            response()
                .withStatusCode(200)
                .withBody(this.getResourceFileAsString("response/getEventForCategory.json")));

    final SimpleFilter simpleFilter =
        (SimpleFilter)
            new SimpleFilter.SimpleFilterBuilder()
                .addBinaryOperation("event.categoryId", BinaryOperation.equals, 16)
                .build();

    Optional<List<Event>> events = api.getEvents(simpleFilter);
    assertEquals(true, events.isPresent());
    assertEquals(66, events.get().size());
  }

  @Test
  public void testCoupons() throws NoSuchAlgorithmException, KeyManagementException {
    mock.when(
            request()
                .withMethod("GET")
                .withPath(basePath + "/Coupon")
                .withQueryStringParameter("translationLang", "en")
                .withQueryStringParameter("includeUndisplayed", "false")
                .withQueryStringParameter("simpleFilter", "coupon.categoryId:equals:16")
                .withQueryStringParameter(
                    "existsFilter", "coupon:simpleFilter:event.cashoutAvail:equals:Y"))
        .respond(
            response()
                .withStatusCode(200)
                .withBody(this.getResourceFileAsString("response/getCoupons.json")));

    final SimpleFilter simpleFilter =
        (SimpleFilter)
            new SimpleFilter.SimpleFilterBuilder()
                .addBinaryOperation("coupon.categoryId", BinaryOperation.equals, 16)
                .build();

    ExistsFilter existsFilter =
        (ExistsFilter)
            new ExistsFilterBuilder()
                .addBinaryOperation(
                    "coupon:simpleFilter:event.cashoutAvail", BinaryOperation.equals, "Y")
                .build();

    Optional<List<Coupon>> coupons =
        api.getCoupons(Optional.of(simpleFilter), Optional.of(existsFilter), false);

    assertTrue(coupons.isPresent());
    assertEquals(2, coupons.get().size());
    assertEquals("5", coupons.get().get(0).getId());
    assertEquals("159", coupons.get().get(1).getId());
  }

  @Test
  public void testCategories() throws NoSuchAlgorithmException, KeyManagementException {
    mock.when(
            request()
                .withMethod("GET")
                .withPath(basePath + "/Category")
                .withQueryStringParameter("includeUndisplayed", "false"))
        .respond(
            response()
                .withStatusCode(200)
                .withBody(this.getResourceFileAsString("response/getCategories.json")));

    Optional<List<CategoryEntity>> categories =
        api.getCategories(Optional.empty(), Optional.empty(), false);

    assertTrue(categories.isPresent());
    assertEquals(2, categories.get().size());
    assertEquals(Integer.valueOf(6), categories.get().get(0).getId());
    assertEquals(Integer.valueOf(160), categories.get().get(1).getId());
  }

  @Test
  public void testCoupon() throws NoSuchAlgorithmException, KeyManagementException {
    mock.when(
            request()
                .withMethod("GET")
                .withPath(basePath + "/Coupon/5")
                .withQueryStringParameter("translationLang", "en")
                .withQueryStringParameter("includeUndisplayed", "false")
                .withQueryStringParameter("simpleFilter", "coupon.categoryId:equals:16")
                .withQueryStringParameter(
                    "existsFilter", "coupon:simpleFilter:event.cashoutAvail:equals:Y"))
        .respond(
            response()
                .withStatusCode(200)
                .withBody(this.getResourceFileAsString("response/getCoupons.json")));

    final SimpleFilter simpleFilter =
        (SimpleFilter)
            new SimpleFilter.SimpleFilterBuilder()
                .addBinaryOperation("coupon.categoryId", BinaryOperation.equals, 16)
                .build();

    ExistsFilter existsFilter =
        (ExistsFilter)
            new ExistsFilterBuilder()
                .addBinaryOperation(
                    "coupon:simpleFilter:event.cashoutAvail", BinaryOperation.equals, "Y")
                .build();

    Optional<Coupon> coupon =
        api.getCoupon("5", Optional.of(simpleFilter), Optional.of(existsFilter), false);

    assertTrue(coupon.isPresent());
    assertEquals("5", coupon.get().getId());
  }

  @Test
  public void testResultedEvent() throws NoSuchAlgorithmException, KeyManagementException {
    final String serviceName = "ResultedEvent";
    mock.when(
            request()
                .withMethod("GET")
                .withPath(basePathHistoricDrilldown + "/" + serviceName + "/12365606")
                .withQueryStringParameter("includeUndisplayed", "true"))
        .respond(
            response()
                .withStatusCode(200)
                .withBody(this.getResourceFileAsString("response/getResultedEvent.json")));

    Optional<Event> event =
        api.getResultedEvent("12365606", Optional.empty(), Optional.empty(), true);
    assertTrue(event.isPresent());
    Market resultedMarket = event.get().getChildren().get(0).getResultedMarket();
    assertNotNull(resultedMarket);
    assertNotNull(resultedMarket.getChildren());
    List<Outcome> resultedOutcomes =
        resultedMarket.getChildren().stream()
            .map(Children::getResultedOutcome)
            .collect(Collectors.toList());
    assertTrue(!resultedOutcomes.isEmpty());
    assertEquals(18, resultedOutcomes.size());
    Optional<Outcome> winner =
        resultedOutcomes.stream().filter(outcome -> "1".equals(outcome.getPosition())).findFirst();
    assertTrue(winner.isPresent());
    assertEquals("W", winner.get().getResultCode());
  }

  @Test
  public void testRacingResultsForEvent() throws NoSuchAlgorithmException, KeyManagementException {
    final String serviceName = "RacingResultsForEvent";
    mock.when(
            request()
                .withMethod("GET")
                .withPath(basePathHistoricDrilldown + "/" + serviceName + "/12365606"))
        .respond(
            response()
                .withStatusCode(200)
                .withBody(this.getResourceFileAsString("response/getRacingResultsForEvent.json")));

    Optional<RacingResult> racingResult = api.getRacingResultsForEvent("12365606");
    assertTrue(racingResult.isPresent());
    assertNotNull(racingResult.get().getChildren());
    List<FinalPosition> finalPositions =
        racingResult.get().getChildren().stream()
            .map(Children::getFinalPosition)
            .filter(Objects::nonNull)
            .collect(Collectors.toList());
    assertTrue(!finalPositions.isEmpty());
    assertEquals(4, finalPositions.size());
    Optional<FinalPosition> winner =
        finalPositions.stream()
            .filter(finalPosition -> finalPosition.getPosition() == 1)
            .findFirst();
    assertTrue(winner.isPresent());
  }

  // http://127.0.0.1:8443/openbet-ssviewer/Drilldown/2.27/
  // EventToOutcomeForEvent/9954317?racingForm=outcome&racingForm=event&prune=event&prune=market
  // &translationLang=en&includeUndisplayed=false
  @Test
  public void testEventsRacingFormEvent()
      throws IOException, NoSuchAlgorithmException, KeyManagementException {
    final String serviceName = "EventToOutcomeForEvent";

    mock.when(
            request()
                .withMethod("GET")
                .withPath(basePath + "/" + serviceName + "/" + 9954317)
                .withQueryStringParameter("racingForm", "outcome")
                .withQueryStringParameter("racingForm", "event")
                .withQueryStringParameter("prune", "event")
                .withQueryStringParameter("prune", "market")
                .withQueryStringParameter("translationLang", "en")
                .withQueryStringParameter("includeUndisplayed", "false"))
        .respond(
            response()
                .withStatusCode(200)
                .withBody(this.getResourceFileAsString("response/getEventRacingFormEvent.json")));

    final Builder builder =
        new Builder()
            .setUrl("http://127.0.0.1:8443")
            .setLoggingLevel(Level.BODY)
            .setConnectionTimeout(1)
            .setReadTimeout(1)
            .setMaxNumberOfRetries(1)
            .setVersion("2.27");

    SiteServerImpl siteServer = new SiteServerImpl(builder);

    BaseFilter simpleFilter = new SimpleFilter.SimpleFilterBuilder().build();

    List<String> prune = new ArrayList<>();
    prune.add("event");
    prune.add("market");

    List<String> ids = new ArrayList<>();
    ids.add("9954317");

    EnumSet<RacingForm> forms = EnumSet.allOf(RacingForm.class);

    Optional<List<Children>> events =
        siteServer.getEventToOutcomeForEvent(ids, (SimpleFilter) simpleFilter, forms, prune);

    assertEquals(true, events.isPresent());
    assertEquals(11, events.get().size());
    assertNotNull(events.get().get(1).getRacingFormEvent());
  }
}
