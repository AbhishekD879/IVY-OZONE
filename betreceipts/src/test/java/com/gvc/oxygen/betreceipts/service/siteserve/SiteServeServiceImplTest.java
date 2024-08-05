package com.gvc.oxygen.betreceipts.service.siteserve;

import com.egalacoral.spark.siteserver.api.ExistsFilter;
import com.egalacoral.spark.siteserver.api.LimitToFilter;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Category;
import com.egalacoral.spark.siteserver.model.Event;
import com.gvc.oxygen.betreceipts.entity.TypeFlagCodes;
import com.gvc.oxygen.betreceipts.service.siteserve.NextEventsParameters.NextEventsParametersBuilder;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import org.assertj.core.api.WithAssertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.BDDMockito;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
public class SiteServeServiceImplTest extends BDDMockito implements WithAssertions {

  @Mock private SiteServerApi api;

  @Test
  public void getNextRacesEvents() {
    ArrayList<Event> events = new ArrayList<>();
    events.add(buildEvent("1", "2020-03-26T15:30:00Z"));
    events.add(buildEvent("2", "2020-03-26T14:30:00Z"));
    when(api.getEventToOutcomeForClass(
            anyList(), any(SimpleFilter.class), any(LimitToFilter.class), any(ExistsFilter.class)))
        .thenReturn(Optional.of(events));
    SiteServeServiceImpl service = new SiteServeServiceImpl(api);
    NextEventsParametersBuilder builder = getNextEventsParametersBuilder();
    List<Event> resultedEvents =
        service.doGetNextRacesEvents(builder.build(), Collections.emptyList());
    assertThat(resultedEvents).hasSize(2).element(0).hasFieldOrPropertyWithValue("id", "1");
  }

  @Test
  public void getNextRacesEventsForEmptyClasses() {
    when(api.getEventToOutcomeForClass(
            anyList(), any(SimpleFilter.class), any(LimitToFilter.class), any(ExistsFilter.class)))
        .thenReturn(Optional.empty());
    ArrayList<Event> events = new ArrayList<>();
    events.add(buildEvent("1", "2020-03-26T15:30:00Z"));
    events.add(buildEvent("2", "2020-03-26T14:30:00Z"));
    SiteServeServiceImpl service = new SiteServeServiceImpl(api);
    NextEventsParametersBuilder builder = getNextEventsParametersBuilder();
    List<Event> resultedEvents =
        service.doGetNextRacesEvents(builder.build(), Collections.emptyList());
    assertThat(resultedEvents).hasSize(0);
  }

  private NextEventsParametersBuilder getNextEventsParametersBuilder() {
    NextEventsParametersBuilder builder = NextEventsParameters.builder();
    builder.timePeriodMinutes(30);
    builder.categoryId(21);
    builder.typeFlagCodes(TypeFlagCodes.of("INT"));
    return builder;
  }

  private Event buildEvent(String id, String startTime) {
    Event event = new Event();
    event.setId(id);
    event.setName("test");
    event.setStartTime(startTime);
    return event;
  }

  private ArrayList<Category> buildCategories() {
    ArrayList<Category> categories = new ArrayList<>();
    Category category = new Category();
    category.setId(12);
    categories.add(category);
    return categories;
  }
}
