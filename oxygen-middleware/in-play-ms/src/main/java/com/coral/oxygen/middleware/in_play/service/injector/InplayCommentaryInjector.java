package com.coral.oxygen.middleware.in_play.service.injector;

import com.coral.oxygen.cms.api.SystemConfigProvider;
import com.coral.oxygen.middleware.common.service.AbstractCommentaryInjector;
import com.coral.oxygen.middleware.in_play.service.siteserver.InplaySiteServeService;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData;
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayModel;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import com.coral.oxygen.middleware.pojos.model.output.inplay.TypeSegment;
import com.egalacoral.spark.siteserver.model.Event;
import java.util.Collection;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class InplayCommentaryInjector extends AbstractCommentaryInjector
    implements InPlayDataInjector {

  @Autowired
  public InplayCommentaryInjector(
      InplaySiteServeService inplaySiteServeService, SystemConfigProvider systemConfigProvider) {
    super(inplaySiteServeService, systemConfigProvider);
  }

  @Override
  public void injectData(InPlayData inPlayData) {

    InPlayModel livenow = inPlayData.getLivenow();

    List<EventsModuleData> events =
        livenow.getSportEvents().stream()
            .map(SportSegment::getEventsByTypeName)
            .flatMap(Collection::stream)
            .map(TypeSegment::getEvents)
            .flatMap(Collection::stream)
            .collect(Collectors.toList());

    List<Long> eventIds = events.stream().map(EventsModuleData::getId).collect(Collectors.toList());

    injectData(eventIds, events);

    injectUpcomingNameWithRemovedProviderMarker(inPlayData.getUpcoming());
  }

  /**
   * Removes (SS), (BG) and other provider markers from upcoming event names (i.e. Boston Red Sox @
   * Philadelphia Phillies(SS)) with the help of bipScoreParser. As these names do not contain
   * scores, parser will just remove provider marker and not parse the name without additional
   * performance overhead.
   *
   * @param upcoming - upcoming events without scores in name but with provider marker
   */
  private void injectUpcomingNameWithRemovedProviderMarker(InPlayModel upcoming) {
    List<EventsModuleData> events =
        upcoming.getSportEvents().stream()
            .map(SportSegment::getEventsByTypeName)
            .flatMap(Collection::stream)
            .map(TypeSegment::getEvents)
            .flatMap(Collection::stream)
            .collect(Collectors.toList());
    injectWithBipScoreParser(events);
  }

  @Override
  protected void populateEvent(EventsModuleData event, Event comments) {
    super.populateEvent(event, comments);
    String categoryCode = event.getCategoryCode();
    if (categoryCode == null) {
      categoryCode = "";
    }
    if ("football".equalsIgnoreCase(categoryCode)) {
      populateClockData(event, comments);
    }
  }
}
