package com.ladbrokescoral.oxygen.timeline.api.service;

import com.ladbrokescoral.oxygen.timeline.api.model.obevent.TimelineSelectionEvent;

public interface SelectionService {

  TimelineSelectionEvent subscribeOnUpdates(String selectionId);
}
