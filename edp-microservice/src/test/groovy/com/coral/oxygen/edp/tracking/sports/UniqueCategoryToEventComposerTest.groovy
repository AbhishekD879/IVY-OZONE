package com.coral.oxygen.edp.tracking.sports

import com.coral.oxygen.edp.model.output.OutputEvent
import com.coral.oxygen.edp.tracking.model.CategoryToUpcomingEvent
import com.egalacoral.spark.siteserver.model.Category
import spock.lang.Specification

import static java.util.Collections.emptyList

class UniqueCategoryToEventComposerTest extends Specification {
  private composer = new UniqueCategoryToEventComposer()

  def "Empty list returned"() {
    expect:
    composer.composeCategoriesToEvents(categories, events).isEmpty()
    where:
    categories         | events
    null               | null
    emptyList()        | emptyList()
    null               | emptyList()
    emptyList()        | null
    categories([1, 2]) | null
    null               | [event(1, 1)]
  }

  def "If event and category matches"() {
    given:
    def categories = categories([1, 1])
    def events = [event(111, 1)]
    when:
    def result = composer.composeCategoriesToEvents(categories, events)
    then:
    result.size() == 1
    CategoryToUpcomingEvent catToEvent = result.get(0)
    catToEvent.id == 1
    catToEvent.event == events[0]
  }

  def "When two events for same category present, only one with lowest display order returned"() {
    given:
    def categories = categories([1, 2, 3])
    def events = [
      event(111, 1),
      event(222, 2),
      event(221, 2)
    ]
    when:
    def result = composer.composeCategoriesToEvents(categories, events)
    then:
    result.size() == 2
    result[0].id == 1
    result[0].event.id == 111

    result[1].id == 2
    result[1].event.id == 221
  }

  def "Event with category not present in the list is ignored"() {
    given:
    def categories = categories([1])
    def events = [event(222, 2)]
    when:
    def result = composer.composeCategoriesToEvents(categories, events)
    then:
    result.size() == 0
  }

  private List<Category> categories(List<Integer> ids) {
    ids.collect {
      def category = new Category()
      category.id = it
      category
    }
  }

  private OutputEvent event(int eventId, int categoryId) {
    OutputEvent.builder()
        .id(eventId)
        .displayOrder(eventId)
        .classId(String.valueOf(categoryId)) // In SS library category wrongly refers to OB's class
        .build()

  }
}
