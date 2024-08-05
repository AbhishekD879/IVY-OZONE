package com.ladbrokescoral.oxygen.timeline.api.service;

import com.egalacoral.spark.siteserver.model.Event;
import java.util.Optional;

public interface SubscriptionService {

  Optional<Event> subscribe(String selectionId);
}
