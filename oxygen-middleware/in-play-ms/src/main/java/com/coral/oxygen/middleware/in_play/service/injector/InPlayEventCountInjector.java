package com.coral.oxygen.middleware.in_play.service.injector;

import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData;
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayModel;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import com.coral.oxygen.middleware.pojos.model.output.inplay.TypeSegment;
import org.springframework.stereotype.Component;

@Component
public class InPlayEventCountInjector implements InPlayDataInjector {

  @Override
  public void injectData(InPlayData inPlayData) {
    collectEventCount(inPlayData.getLivenow());
    collectEventCount(inPlayData.getUpcoming());
    collectEventCount(inPlayData.getLiveStream());
  }

  private void collectEventCount(InPlayModel model) {
    model
        .getSportEvents()
        .forEach(
            sport -> {
              sport
                  .getEventsByTypeName()
                  .forEach(type -> type.setEventCount(type.getEvents().size()));
              int eventCount =
                  sport.getEventsByTypeName().stream().mapToInt(TypeSegment::getEventCount).sum();
              sport.setEventCount(eventCount);
            });
    int eventCount = model.getSportEvents().stream().mapToInt(SportSegment::getEventCount).sum();
    model.setEventCount(eventCount);
  }
}
