package com.coral.oxygen.middleware.in_play.service.injector;

import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData;
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayModel;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import com.coral.oxygen.middleware.pojos.model.output.inplay.TypeSegment;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Component;

@Component
public class InPlayEventIdsInjector implements InPlayDataInjector {

  @Override
  public void injectData(InPlayData inPlayData) {
    collectEventIds(inPlayData.getLivenow());
    collectEventIds(inPlayData.getUpcoming());
    collectEventIds(inPlayData.getLiveStream());
  }

  private void collectEventIds(InPlayModel model) {
    model
        .getSportEvents()
        .forEach(
            sport -> {
              sport
                  .getEventsByTypeName()
                  .forEach(
                      type -> {
                        List eventsIds =
                            new ArrayList(
                                type.getEvents().stream()
                                    .map(EventsModuleData::getId)
                                    .collect(Collectors.toSet()));
                        eventsIds.sort(Comparator.naturalOrder());
                        type.setEventsIds(eventsIds);
                      });
              ArrayList<Long> eventsIds =
                  new ArrayList<>(
                      sport.getEventsByTypeName().stream()
                          .map(TypeSegment::getEventsIds)
                          .flatMap(Collection::stream)
                          .collect(Collectors.toSet()));
              eventsIds.sort(Comparator.naturalOrder());
              sport.setEventsIds(eventsIds);
            });
    List eventsIds =
        new ArrayList(
            model.getSportEvents().stream()
                .map(SportSegment::getEventsIds)
                .flatMap(Collection::stream)
                .collect(Collectors.toSet()));
    eventsIds.sort(Comparator.naturalOrder());
    model.setEventsIds(eventsIds);
  }
}
