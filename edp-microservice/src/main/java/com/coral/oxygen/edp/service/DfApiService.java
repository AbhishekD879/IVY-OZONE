package com.coral.oxygen.edp.service;

import com.coral.oxygen.edp.tracking.model.RaceDTO;
import java.io.IOException;
import java.util.Collection;
import java.util.Map;
import java.util.Optional;

public interface DfApiService {

  public Optional<Map<Long, RaceDTO>> getNextRaces(int categoryId, Collection<Long> eventIds)
      throws IOException;
}
