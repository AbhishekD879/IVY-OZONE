package com.ladbrokescoral.oxygen.timeline.api.service.impl;

import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.timeline.api.model.obevent.ObEvent;
import com.ladbrokescoral.oxygen.timeline.api.model.obevent.TimelineSelectionEvent;
import com.ladbrokescoral.oxygen.timeline.api.service.SelectionService;
import com.ladbrokescoral.oxygen.timeline.api.service.SubscriptionService;
import lombok.RequiredArgsConstructor;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class SelectionServiceImpl implements SelectionService {

  private final SubscriptionService subscriptionService;
  private final ModelMapper modelMapper;

  @Override
  public TimelineSelectionEvent subscribeOnUpdates(String selectionId) {
    return subscriptionService
        .subscribe(selectionId)
        .map(
            (Event ssEvent) -> {
              TimelineSelectionEvent event = new TimelineSelectionEvent();
              ObEvent obEvent = modelMapper.map(ssEvent, ObEvent.class);
              event.setObEvent(obEvent);
              return event;
            })
        .orElse(null);
  }
}
