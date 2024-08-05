package com.coral.oxygen.middleware.in_play.service;

import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData;
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayModel;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import com.coral.oxygen.middleware.pojos.model.output.inplay.TypeSegment;
import java.util.Comparator;
import java.util.List;
import org.springframework.stereotype.Component;

@Component
public class InPlayDataSorter {

  private final Comparator<SportSegment> sportsComparator =
      Comparator.comparing(
          SportSegment::getDisplayOrder, Comparator.nullsLast(Comparator.naturalOrder()));

  private final Comparator<TypeSegment> typesComparator =
      Comparator.comparing(
              TypeSegment::getClassDisplayOrder, Comparator.nullsLast(Comparator.naturalOrder()))
          .thenComparing(
              TypeSegment::getTypeDisplayOrder, Comparator.nullsLast(Comparator.naturalOrder()));

  private final Comparator<EventsModuleData> eventsComparator =
      Comparator.comparing(
              EventsModuleData::getStartTime, Comparator.nullsLast(Comparator.naturalOrder()))
          .thenComparing(
              EventsModuleData::getDisplayOrder, Comparator.nullsLast(Comparator.naturalOrder()))
          .thenComparing(
              EventsModuleData::getName, Comparator.nullsLast(Comparator.naturalOrder()));

  public void sort(InPlayData inPlayData) {
    sort(inPlayData.getLivenow());
    sort(inPlayData.getUpcoming());
    sort(inPlayData.getLiveStream());
  }

  private void sort(InPlayModel model) {
    model.getSportEvents().sort(sportsComparator);
    model
        .getSportEvents()
        .forEach(
            sport -> {
              sport.getEventsByTypeName().sort(typesComparator);
              sport.getEventsByTypeName().forEach(type -> type.getEvents().sort(eventsComparator));
            });
  }

  public void sort(List<SportSegment> sportSegmentList) {
    sportSegmentList.sort(sportsComparator);
    sportSegmentList.forEach(
        (SportSegment sportSegment) -> {
          sportSegment.getEventsByTypeName().sort(typesComparator);
          sportSegment
              .getEventsByTypeName()
              .forEach(type -> type.getEvents().sort(eventsComparator));
        });
  }
}
