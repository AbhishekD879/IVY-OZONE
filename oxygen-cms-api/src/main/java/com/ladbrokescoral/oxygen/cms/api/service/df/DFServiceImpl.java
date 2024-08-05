package com.ladbrokescoral.oxygen.cms.api.service.df;

import com.coral.oxygen.df.model.RaceEvent;
import java.io.IOException;
import java.util.Collection;
import java.util.Map;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class DFServiceImpl implements DFService {

  private DFServiceProvider provider;

  @Autowired
  public DFServiceImpl(DFServiceProvider provider) {
    this.provider = provider;
  }

  @Override
  public Optional<Map<Long, RaceEvent>> getNextRaces(
      String brand, int categoryId, Collection<Long> eventIds) throws IOException {
    return provider.api(brand).getRaceEvents(categoryId, eventIds);
  }
}
