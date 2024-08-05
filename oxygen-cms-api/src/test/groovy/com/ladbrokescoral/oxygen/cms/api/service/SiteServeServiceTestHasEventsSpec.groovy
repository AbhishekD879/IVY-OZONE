
package com.ladbrokescoral.oxygen.cms.api.service

import com.egalacoral.spark.siteserver.api.*
import com.egalacoral.spark.siteserver.model.Category
import com.egalacoral.spark.siteserver.model.Event
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeServiceImpl
import com.ladbrokescoral.oxygen.cms.util.Util

import java.time.*
import java.time.temporal.*

import spock.lang.Specification

import static com.ladbrokescoral.oxygen.cms.util.CollectionUtilX.setOf
import static com.ladbrokescoral.oxygen.cms.util.CollectionUtilX.unionSet

class SiteServeServiceTestHasEventsSpec extends Specification {
  private static final int TIER_2_SPORT_ID = 10
  private static final Set<Integer> ALL_TIER_2_SPORTS = setOf(TIER_2_SPORT_ID, 2, 4, 5, 7, 8, 9, 11, 12, 13, 14, 15, 17, 18, 19)
  private static final String CORAL_BRAND = "bma"
  private static final String OUTRIGHT_SORT_CODES = "TNMT,TR01,TR02,TR03,TR04,TR05,TR06,TR07,TR08,TR09,TR10,TR11,TR12,TR13,TR14,TR15,TR16,TR17,TR18,TR19,TR20"
  public static final String PRIMARY_MARKETS = "|Match Betting|,|Handicap Match Result|"
  public static final String DISP_SORT_NAMES = "HH,MH"
  public static final String EVENT_SORT_CODE = "TNMT,MTCH"

  SiteServerApi siteServerApiMock
  SiteServeService siteServeService

  def setup() {
    siteServerApiMock = Mock(SiteServerApi)
    SiteServeApiProvider serveApiProviderMock = Mock(SiteServeApiProvider)
    serveApiProviderMock.api(CORAL_BRAND) >> siteServerApiMock
    siteServeService = new SiteServeServiceImpl(serveApiProviderMock)
  }

  def "test any Live Events Exists" () {
    given: "API Filter for Live events"

    and: "SS has active Classes"
    List<String> classesIds = ["1", "2", "3"]
    mockSsHasActiveClassesForCategory(TIER_2_SPORT_ID, classesIds)

    and: "SS has Live events"
    SimpleFilter liveEventsFilter = liveEventsFilter(TIER_2_SPORT_ID)
    ExistsFilter eventMarketIsAvailableFilter = liveEventToMarketFilter()
    def liveEvents = Collections.singletonList(new Event())
    mockEventsForClassRequest(liveEvents, classesIds, liveEventsFilter, eventMarketIsAvailableFilter)

    when: "request for events by built filter"
    boolean liveEventsExists = siteServeService.anyLiveOrUpcomingEventsExists(category(TIER_2_SPORT_ID))

    then: "SS retrieves Live events"
    liveEventsExists
  }

  def "test any Upcoming Events Exists" () {
    given: "API Filter for Upcoming events"

    and: "SS has active Classes"
    List<String> classesIds = ["1", "2", "3"]
    mockSsHasActiveClassesForCategory(TIER_2_SPORT_ID, classesIds)

    and: "SS has NO Live events"
    SimpleFilter liveEventsFilter = liveEventsFilter(TIER_2_SPORT_ID)
    ExistsFilter liveEventToMarketFilter = liveEventToMarketFilter()
    mockEventsForClassRequest(Collections.emptyList(), classesIds, liveEventsFilter, liveEventToMarketFilter)

    and: "SS has Upcoming events"
    SimpleFilter upcomingEventsFilter = upcomingEventsFilter(TIER_2_SPORT_ID)
    ExistsFilter upcomingEventToMarketFilter = upcomingEventToMarketFilter()
    Event upcomingEvent = new Event()
    mockEventsForClassRequest(Collections.singletonList(upcomingEvent), classesIds, upcomingEventsFilter, upcomingEventToMarketFilter)

    when: "request for events by built filter"
    boolean upcomingEventsExists = siteServeService.anyLiveOrUpcomingEventsExists(category(TIER_2_SPORT_ID))

    then: "SS retrieves Upcoming events"
    upcomingEventsExists
  }

  private void mockEventsForClassRequest(List<Event> expectedEvents, List<String> classesIds, SimpleFilter simpleFilter, ExistsFilter existsFilter) {
    siteServerApiMock.getEventToOutcomeForClass(classesIds,
        _ as SimpleFilter,
        _ as LimitToFilter,
        _ as LimitRecordsFilter,
        existsFilter,
        Arrays.asList("event", "market")) >> Optional.of(expectedEvents)
  }

  private static SimpleFilter liveEventsFilter(Integer categoryId) {
    Instant now = nowUtcWithoutMillis()
    return (SimpleFilter) new SimpleFilter.SimpleFilterBuilder()
        .addBinaryOperation(SSApiFilterFields.EVENT_CATEGORY_ID, BinaryOperation.equals, categoryId)
        .addBinaryOperation(SSApiFilterFields.EVENT_SITE_CHANNELS, BinaryOperation.contains, "M")
        .addBinaryOperation(SSApiFilterFields.EVENT_SORT_CODE, BinaryOperation.intersects, EVENT_SORT_CODE)
        .addBinaryOperation(SSApiFilterFields.EVENT_DRILLDOWN_TAG_NAMES, BinaryOperation.intersects, "EVFLAG_BL")
        .addField(SSApiFilterFields.EVENT_IS_STARTED)
        .addField(SSApiFilterFields.EVENT_IS_LIVE_NOW)
        .addBinaryOperation(SSApiFilterFields.EVENT_SUSPEND_AT_TIME, BinaryOperation.greaterThan, now)
        .addBinaryOperation(SSApiFilterFields.DISP_SORT_NAME, BinaryOperation.intersects, DISP_SORT_NAMES)
        .addBinaryOperation(SSApiFilterFields.TEMPLATE_MARKET_NAME, BinaryOperation.intersects, PRIMARY_MARKETS)
        .build()
  }

  private static ExistsFilter liveEventToMarketFilter() {
    return (ExistsFilter) new ExistsFilter.ExistsFilterBuilder()
        .addField("event:simpleFilter:market.isMarketBetInRun")
        .addField("event:simpleFilter:market.isDisplayed")
        .addUnaryOperation("event:simpleFilter:market.isResulted", UnaryOperation.isFalse)
        .build()
  }

  private static SimpleFilter upcomingEventsFilter(Integer categoryId) {
    Instant now = nowUtcWithoutMillis()
    Instant in48Hours = now.plus(Duration.ofHours(48))
    return (SimpleFilter) new SimpleFilter.SimpleFilterBuilder()
        .addField(SSApiFilterFields.EVENT_IS_ACTIVE)
        .addBinaryOperation(SSApiFilterFields.EVENT_CATEGORY_ID, BinaryOperation.equals, categoryId)
        .addBinaryOperation(SSApiFilterFields.EVENT_SITE_CHANNELS, BinaryOperation.contains, "M")
        .addBinaryOperation(SSApiFilterFields.EVENT_SORT_CODE, BinaryOperation.equals, "MTCH")
        .addUnaryOperation(SSApiFilterFields.EVENT_IS_STARTED, UnaryOperation.isFalse)
        .addBinaryOperation(SSApiFilterFields.EVENT_START_TIME, BinaryOperation.greaterThan, now)
        .addBinaryOperation(SSApiFilterFields.EVENT_START_TIME, BinaryOperation.lessThan, in48Hours)
        .addBinaryOperation(SSApiFilterFields.EVENT_SUSPEND_AT_TIME, BinaryOperation.greaterThan, now)
        .addBinaryOperation(SSApiFilterFields.DISP_SORT_NAME, BinaryOperation.intersects, DISP_SORT_NAMES)
        .addBinaryOperation(SSApiFilterFields.TEMPLATE_MARKET_NAME, BinaryOperation.intersects, PRIMARY_MARKETS)
        .build()
  }

  private static ExistsFilter upcomingEventToMarketFilter() {
    (ExistsFilter) new ExistsFilter.ExistsFilterBuilder()
        .addField("event:simpleFilter:market.isDisplayed")
        .addUnaryOperation("event:simpleFilter:market.isResulted", UnaryOperation.isFalse)
        .build()
  }

  def "should retrieve false there're no active classes for Matches"() {
    given: "SS has NO active Classes"
    mockSsHasActiveClassesForCategory(TIER_2_SPORT_ID, [])

    when: "filtering existing categories for Matches existence"
    boolean hasEvents = siteServeService.anyLiveOrUpcomingEventsExists(category(TIER_2_SPORT_ID))

    then: "retrieving only categories with Outrights"
    !hasEvents
  }

  def "should filter categories with Outright Events"() {
    given: "SS has active Classes"
    Set<Integer> existingCategoryIds = ALL_TIER_2_SPORTS
    Set<Integer> categoryIdsWithOutrights = [TIER_2_SPORT_ID]
    List<String> classesIds = ["1", "2"]
    mockSsHasActiveClassesForCategories(existingCategoryIds, classesIds)

    and: "SS has Outright events for Classes"
    mockSsHasOutrightEvents(classesIds, existingCategoryIds, categoryIdsWithOutrights)

    when: "filtering existing categories for Outrights existence"
    Set<Integer> actualCategories = siteServeService.filterByOutrightEvents(CORAL_BRAND, existingCategoryIds)

    then: "retrieving only categories with Outrights"
    actualCategories.size() != existingCategoryIds.size()
    actualCategories.size() == categoryIdsWithOutrights.size()
    actualCategories.iterator().next() == categoryIdsWithOutrights[0]
  }

  private void mockSsHasActiveClassesForCategory(Integer categoryId, List<String> expectedClassesIds) {
    SimpleFilter activeClassesFilter = (SimpleFilter) new SimpleFilter.SimpleFilterBuilder()
        .addBinaryOperation("class.categoryId", BinaryOperation.equals, categoryId)
        .addBinaryOperation("class.siteChannels", BinaryOperation.contains, "M")
        .addField("class.isActive")
        .build()
    def categoryClasses = categoryClasses(expectedClassesIds)
    siteServerApiMock.getClasses(activeClassesFilter,
        new ExistsFilter.ExistsFilterBuilder().build()) >> Optional.ofNullable(categoryClasses.isEmpty() ? null : categoryClasses)
  }

  private void mockSsHasActiveClassesForCategories(Set<Integer> categoryIdsToCheck, List<String> expectedClassesIds) {
    SimpleFilter activeClassesFilter = activeClassesFilter(categoryIdsToCheck)
    siteServerApiMock.getClasses(activeClassesFilter,
        new ExistsFilter.ExistsFilterBuilder().build()) >> Optional.ofNullable(categoryClasses(expectedClassesIds))
  }

  private static SimpleFilter activeClassesFilter(Set<Integer> categoryIds) {
    String categoryIdsCsv = Util.join(",", categoryIds)
    return (SimpleFilter) new SimpleFilter.SimpleFilterBuilder()
        .addBinaryOperation("class.categoryId", BinaryOperation.intersects, categoryIdsCsv)
        .addBinaryOperation("class.siteChannels", BinaryOperation.contains, "M")
        .addField("class.isActive")
        .build()
  }


  private void mockSsHasOutrightEvents(List<String> classesIds, Set<Integer> categoryIdsToCheck, Set<Integer> categoryIdsWithOutrights) {
    def outrightEvents = new ArrayList()
    for (int categoryId : categoryIdsWithOutrights) {
      outrightEvents.add(event(categoryId))
    }

    SimpleFilter outrightEventsFilter = outrightEventsFilter(categoryIdsToCheck)
    siteServerApiMock.getEventToOutcomeForClass(classesIds, outrightEventsFilter,
        _ as LimitToFilter,
        _ as LimitRecordsFilter,
        new ExistsFilter.ExistsFilterBuilder().build(),
        Arrays.asList("event", "market")
        ) >> Optional.of(outrightEvents)
  }

  private static Event event(Integer categoryId) {
    Event event = new Event()
    event.categoryId = categoryId
    return event
  }

  private SimpleFilter outrightEventsFilter(Set<Integer> categoryIds) {

    Instant now = nowUtcWithoutMillis()
    String categoryIdsCsv = Util.join(",", categoryIds)
    return (SimpleFilter) new SimpleFilter.SimpleFilterBuilder()
        .addBinaryOperation(SSApiFilterFields.EVENT_CATEGORY_ID, BinaryOperation.in, categoryIdsCsv)
        .addBinaryOperation(SSApiFilterFields.EVENT_SITE_CHANNELS, BinaryOperation.contains, "M")
        .addBinaryOperation(SSApiFilterFields.EVENT_SORT_CODE, BinaryOperation.intersects, OUTRIGHT_SORT_CODES)
        .addBinaryOperation(SSApiFilterFields.EVENT_SUSPEND_AT_TIME, BinaryOperation.greaterThan, now)
        .build()
  }

  def "should retrieve 0 categories with Outrights if there're no active classes"() {
    given: "SS does NOT have active Classes"
    Set<Integer> existingCategoryIds = ALL_TIER_2_SPORTS
    List<String> classesIds = []
    mockSsHasActiveClassesForCategories(existingCategoryIds, classesIds)

    when: "filtering existing categories for Outrights existence"
    Set<Integer> actualCategories = siteServeService.filterByOutrightEvents(CORAL_BRAND, existingCategoryIds)

    then: "retrieving only categories with Outrights"
    actualCategories.size() == 0
  }

  def "should filter categories with Competition Events"() {
    given: "SS has active Classes"
    Set<Integer> categoriesToCheck = ALL_TIER_2_SPORTS

    List<String> classesIds = ["1", "2", "3"]
    mockSsHasActiveClassesForCategories(categoriesToCheck, classesIds)

    and: "SS has Outrights events for Classes"
    Set<Integer> categoriesWithOutrights = [TIER_2_SPORT_ID, 12, 14, 15]
    mockSsHasOutrightEvents(classesIds, categoriesToCheck, categoriesWithOutrights)

    and: "Check for Matches only categories without Outrights"
    Set<Integer> categoriesToCheckForMatches = new HashSet<>(categoriesToCheck)
    categoriesToCheckForMatches.removeAll(categoriesWithOutrights)

    and: "SS has Matches events"
    Set<Integer> categoriesWithMatches = [11, 13]
    mockSsHasMatchesEvents(categoriesToCheckForMatches, categoriesWithMatches)

    and: "where result is union of categories with Matches or Outrights"
    Set<Integer> expectedCategories = unionSet(categoriesWithMatches, categoriesWithOutrights)

    when: "filtering existing categories for Competitions existence"
    Set<Integer> actualCategories = siteServeService.filterByCompetitionEvents(CORAL_BRAND, categories(categoriesToCheck))

    then: "retrieving only categories with Competitions"
    actualCategories == expectedCategories
  }

  private void mockSsHasMatchesEvents(HashSet<Integer> categoriesToCheckForMatches, Set<Integer> categoriesWithMatches) {
    for (Integer categoryId : categoriesToCheckForMatches) {
      List<String> classesIds = ["1", "2"]
      mockSsHasActiveClassesForCategories(setOf(categoryId), classesIds)

      List<Event> events = new ArrayList<>()
      if (categoriesWithMatches.contains(categoryId)) {
        events.add(event(categoryId))
      }

      siteServerApiMock.getEventToOutcomeForClass(classesIds, matchesEventsFilter(categoryId),
          _ as LimitToFilter,
          _ as LimitRecordsFilter,
          new ExistsFilter.ExistsFilterBuilder().build(),
          Arrays.asList("event", "market")
          ) >> Optional.of(events)
    }
  }

  private SimpleFilter matchesEventsFilter(Integer categoryId) {

    return (SimpleFilter) new SimpleFilter.SimpleFilterBuilder()
        .addField(SSApiFilterFields.EVENT_IS_OPEN)
        .addField(SSApiFilterFields.EVENT_IS_ACTIVE)
        .addBinaryOperation(SSApiFilterFields.EVENT_SORT_CODE, BinaryOperation.notIn, OUTRIGHT_SORT_CODES)
        .addBinaryOperation(SSApiFilterFields.EVENT_DRILLDOWN_TAG_NAMES, BinaryOperation.notIntersects, "EVFLAG_SP")
        .addBinaryOperation(SSApiFilterFields.EVENT_CATEGORY_ID, BinaryOperation.equals, categoryId)
        .addBinaryOperation(SSApiFilterFields.EVENT_SUSPEND_AT_TIME, BinaryOperation.greaterThan, nowUtcWithoutMillis())
        .addBinaryOperation(SSApiFilterFields.DISP_SORT_NAME, BinaryOperation.intersects, DISP_SORT_NAMES)
        .addBinaryOperation(SSApiFilterFields.TEMPLATE_MARKET_NAME, BinaryOperation.intersects, PRIMARY_MARKETS)
        .build()
  }

  private static List<SportCategory> categories(Collection<Integer> categoryIds) {
    List<SportCategory> sports = new ArrayList<>()
    for (Integer categoryId : categoryIds) {
      sports.add(category(categoryId))
    }
    return sports
  }

  private static SportCategory category(Integer categoryId) {
    def sport = new SportCategory()
    sport.setCategoryId(categoryId)
    sport.setBrand(CORAL_BRAND)
    sport.setDispSortNames(DISP_SORT_NAMES)
    sport.setPrimaryMarkets(PRIMARY_MARKETS)
    sport
  }

  List<Category> categoryClasses(List<String> classesIds) {
    List<Category> categories = new ArrayList<>()
    for (int i = 0; i < classesIds.size(); i++) {
      def category = new Category()
      category.id = Integer.valueOf(classesIds.get(i))
      categories.add(category)
    }
    return categories
  }

  private static Instant nowUtcWithoutMillis() {
    return Instant.now().truncatedTo(ChronoUnit.SECONDS);
  }

  static class SSApiFilterFields {
    public static final String EVENT_CATEGORY_ID = "event.categoryId"
    public static final String EVENT_SITE_CHANNELS = "event.siteChannels"
    public static final String EVENT_SUSPEND_AT_TIME = "event.suspendAtTime"
    public static final String EVENT_IS_STARTED = "event.isStarted"
    public static final String EVENT_DRILLDOWN_TAG_NAMES = "event.drilldownTagNames"
    public static final String EVENT_IS_ACTIVE = "event.isActive"
    public static final String EVENT_START_TIME = "event.startTime"
    public static final String EVENT_IS_LIVE_NOW = "event.isLiveNowEvent"
    public static final String EVENT_SORT_CODE = "event.eventSortCode"
    public static final String EVENT_IS_OPEN = "event.isOpenEvent"

    public static final String TEMPLATE_MARKET_NAME = "market.templateMarketName";
    public static final String DISP_SORT_NAME = "market.dispSortName"
  }
}
