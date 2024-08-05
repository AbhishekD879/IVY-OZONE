package com.coral.oxygen.edp.tracking.sports

import com.coral.oxygen.edp.configuration.SportsDataConsumerConfiguration
import com.coral.oxygen.edp.model.mapping.EventMapper
import com.coral.oxygen.edp.model.output.OutputEvent
import com.coral.oxygen.edp.tracking.UpdateScheduler
import com.coral.oxygen.edp.tracking.model.CategoryToUpcomingEvent
import com.coral.oxygen.edp.service.CmsApiService
import com.egalacoral.spark.siteserver.api.*
import com.egalacoral.spark.siteserver.model.Category
import com.egalacoral.spark.siteserver.model.Event
import com.ladbrokescoral.oxygen.cms.client.model.StreamAndBetDto
import spock.lang.Specification

import java.util.stream.Collectors

import static com.coral.oxygen.edp.TestUtil.deserializeListWithJackson

class SportsDataConsumerSpec extends Specification {

  def VIRTUAL_CLASS_ID = 39
  def VIRTUAL_TENNIS_ID = 291

  def QUEUE_SIZE = 5
  def THREADS_COUNT = 3

  List<CategoryToUpcomingEvent> categoriesToUpcomingEvents =
  deserializeListWithJackson("/virtuals/sports.json", CategoryToUpcomingEvent.class)

  List<CategoryToUpcomingEvent> categoriesToUpcomingEventsSorted =
  deserializeListWithJackson("/virtuals/sports_sorted.json", CategoryToUpcomingEvent.class)
  List<Category> categories = deserializeListWithJackson("/virtuals/sport_categories.json", Category.class)
  List<String> categoryIds = deserializeListWithJackson("/virtuals/category_ids.json", String.class)
  List<OutputEvent> outputEvents = deserializeListWithJackson("/virtuals/events.json", OutputEvent.class)

  List<Event> events = deserializeListWithJackson("/virtuals/events.json", Event.class)
  SiteServerApi siteServerApiStub
  EventMapper eventMapperMock
  UpdateScheduler updateSchedulerMock
  CmsApiService cmsApiService

  SportsDataConsumer sportsDataConsumer

  def setup() {
    siteServerApiStub = Mock(SiteServerApi)
    eventMapperMock = Mock(EventMapper)
    updateSchedulerMock = Mock(UpdateScheduler)
    cmsApiService = Stub(CmsApiService)

    siteServerApiStub.getNextNEventsForClass(1, Collections.singletonList(String.valueOf(VIRTUAL_TENNIS_ID)),
        _ as SimpleFilter,
        _ as ExistsFilter,
        false) >> Optional.of(events
        .stream()
        .filter({ event -> (event.getClassId() == String.valueOf(VIRTUAL_TENNIS_ID)) })
        .collect(Collectors.toList()))

    siteServerApiStub.getNextNEventsForClass(1, categoryIds,
        _ as SimpleFilter,
        _ as ExistsFilter,
        false) >> Optional.of(events)


    siteServerApiStub.getClasses(getCategoriesSimpleFilter(Collections.emptyList(), Collections.singletonList(VIRTUAL_TENNIS_ID)),
        SiteServerImpl.EMPTY_EXISTS_FILTER) >>
        Optional.of(categories
        .stream()
        .filter({ category -> category.getId() == VIRTUAL_TENNIS_ID })
        .collect(Collectors.toList()))

    siteServerApiStub.getClasses(
        _ as SimpleFilter,
        new ExistsFilter.ExistsFilterBuilder().build()) >>
        Optional.of(categories)

    for (Event event : events) {
      eventMapperMock.map(_ as OutputEvent, events.get(events.indexOf(event))) >>
          outputEvents.get(events.indexOf(event))
    }

    def configuration = new SportsDataConsumerConfiguration()
    configuration.maxQueueSize = QUEUE_SIZE
    configuration.threadsCount = THREADS_COUNT
    configuration.virtualCategoryId = 39
    sportsDataConsumer = new SportsDataConsumer(
        configuration,
        siteServerApiStub,
        eventMapperMock,
        updateSchedulerMock,
        cmsApiService,
        new UniqueCategoryToEventComposer())
  }

  def getVirtualSport(int id, boolean enabled, boolean categoryEnabled) {
    def virtualClass = getEmptyVirtualDto(VIRTUAL_CLASS_ID, categoryEnabled)
    def virtualSport = getEmptyVirtualDto(id, enabled)
    virtualClass.setChildren(Collections.singletonList(virtualSport))
    return virtualClass
  }

  def getEmptyVirtualDto(int id, boolean categoryEnabled) {
    StreamAndBetDto dto = new StreamAndBetDto()
    dto.setId(id)
    dto.setAndroidActive(categoryEnabled)
    dto.setIosActive(categoryEnabled)
    dto.setChildren(Collections.emptyList())
    return dto
  }

  def getEmptyIdSet() {
    def idSet = new HashSet<String>()
    idSet.add("")
    return idSet
  }

  def filterCategoriesList(List<CategoryToUpcomingEvent> categories, int id) {
    return categories
        .stream()
        .filter({ category -> category.getId() != id })
        .collect(Collectors.toList())
  }

  /**
   * Compare each element by id of category and id of the upcoming event
   *
   * @return true , if each element in one list is equal another
   * by event id, and by category id, otherwise - return false
   */

  def compareCategories(List<CategoryToUpcomingEvent> one, List<CategoryToUpcomingEvent> another) {

    if (!Objects.nonNull(one) || !Objects.nonNull(another))
      return false

    for (CategoryToUpcomingEvent category : one) {
      if (!(category.getId() == another.get(one.indexOf(category)).getId() &&
          category.getEvent().getId() == another.get(one.indexOf(category)).getEvent().getId()))
        return false
    }
    return true
  }

  def "Test the scheduling on the minimal event.millisUntilStart"() {
    when: 'call #scheduleDataRefresh()'
    sportsDataConsumer.scheduleDataRefresh(outputEvents)
    then: 'updateScheduler receives a call to #schedule with the minimal millisUntilStart among events'
    1 * updateSchedulerMock.schedule(202407)
  }

  def "Test extraction of ids from categories"() {
    when: 'call #extractIdsFromCategories()'
    def result = sportsDataConsumer.extractIdsFromCategories(categories)
    then: 'method returns a list of strings with ids'
    for (String id : result) {
      assert categoryIds.get(result.indexOf(id)) == id
    }
  }

  def "Test interaction inside the Consumer, call to doConsume should return List of categoriesToUpcomingEvents"() {
    given: 'stub cms to return no deactivated sports'

    cmsApiService.getStreamAndBetDto() >>
        Optional.of(Collections.singletonList(getEmptyVirtualDto(VIRTUAL_CLASS_ID, true)))

    when: 'consumer consume'
    def result = sportsDataConsumer.doConsume(getEmptyIdSet())
    List<CategoryToUpcomingEvent> resultCategories = result.get("")

    then: 'consumer returns a Map with sorted list of CategoryToUpcomingEvent as a value, and schedules refresh'
    1 * updateSchedulerMock.schedule(_ as Long)
    compareCategories(resultCategories, categoriesToUpcomingEventsSorted)
  }

  def "Test sport exclusion"() {
    given: 'stub cms to return deactivated virtual tennis'

    cmsApiService.getStreamAndBetDto() >>
        Optional.of(Collections.singletonList(getVirtualSport(VIRTUAL_TENNIS_ID, false, true)))

    List<CategoryToUpcomingEvent> filteredCategories =
        filterCategoriesList(categoriesToUpcomingEventsSorted, VIRTUAL_TENNIS_ID)

    when: 'consumer consume'

    def result = sportsDataConsumer.doConsume(getEmptyIdSet())
    List<CategoryToUpcomingEvent> resultCategories = result.get("")

    then: 'consumer does not return virtual tennis in list of sports'
    compareCategories(filteredCategories, resultCategories)
  }

  def "Test exclude every sport except of one"() {
    given: 'stub cms to return deactivated virtual tennis'

    cmsApiService.getStreamAndBetDto() >>
        Optional.of(Collections.singletonList(getVirtualSport(VIRTUAL_TENNIS_ID, true, false)))

    when: 'consumer consume'
    def result = sportsDataConsumer.doConsume(getEmptyIdSet())
    List<CategoryToUpcomingEvent> resultCategories = result.get("")

    then: 'consumer only tennis, as the whole category is disabled except tennis'
    resultCategories.size() == 1 &&
        resultCategories.get(0).getEvent().getClassId() == String.valueOf(VIRTUAL_TENNIS_ID)
  }

  def getCategoriesSimpleFilter(List<Integer> idsToExclude, List<Integer> idsToInclude) {
    SimpleFilter.SimpleFilterBuilder builder = new SimpleFilter.SimpleFilterBuilder()
        .addBinaryOperation("class.categoryId", BinaryOperation.equals, VIRTUAL_CLASS_ID)
        .addUnaryOperation("class.isActive", UnaryOperation.isTrue)
        .addUnaryOperation("class.hasNext24HourEvent", UnaryOperation.isTrue)
        .addUnaryOperation("class.hasOpenEvent", UnaryOperation.isTrue)
    for (int i : idsToExclude) {
      builder.addBinaryOperation("class.id", BinaryOperation.notEquals, i)
    }
    for (int i : idsToInclude) {
      builder.addBinaryOperation("class.id", BinaryOperation.equals, i)
    }
    return (SimpleFilter) builder.build()
  }
}
