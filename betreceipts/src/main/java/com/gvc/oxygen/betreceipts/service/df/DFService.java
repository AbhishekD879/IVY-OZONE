package com.gvc.oxygen.betreceipts.service.df;

import com.gvc.oxygen.betreceipts.dto.RaceDTO;
import java.io.IOException;
import java.util.Collection;
import java.util.Map;
import java.util.Optional;

public interface DFService {

  public Optional<Map<Long, RaceDTO>> getNextRaces(int categoryId, Collection<Long> eventIds)
      throws IOException;
}
