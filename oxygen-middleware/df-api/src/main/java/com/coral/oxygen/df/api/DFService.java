package com.coral.oxygen.df.api;

import com.coral.oxygen.middleware.pojos.model.df.RaceEvent;
import java.util.Collection;
import java.util.Map;
import java.util.Optional;

public interface DFService {

  Optional<RaceEvent> getRaceEvent(Integer category, Long eventId);

  Optional<Map<Long, RaceEvent>> getRaceEvents(Integer category, Collection<Long> eventIds);

  HealthStatus getHealthStatus();
}
