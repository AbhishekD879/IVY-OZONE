package com.ladbrokescoral.oxygen.cms.api.service.df;

import com.coral.oxygen.df.model.RaceEvent;
import java.io.IOException;
import java.util.Collection;
import java.util.Map;
import java.util.Optional;

public interface DFService {

  public Optional<Map<Long, RaceEvent>> getNextRaces(
      String brand, int categoryId, Collection<Long> eventIds) throws IOException;
}
