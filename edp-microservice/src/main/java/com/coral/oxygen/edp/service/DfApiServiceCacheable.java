package com.coral.oxygen.edp.service;

import com.coral.oxygen.df.model.RaceEvent;
import com.coral.oxygen.edp.configuration.DFApiConfig;
import com.coral.oxygen.edp.model.mapping.GenericMapper;
import com.coral.oxygen.edp.tracking.model.RaceDTO;
import java.io.IOException;
import java.util.Collection;
import java.util.Map;
import java.util.Optional;
import org.modelmapper.TypeToken;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.CacheConfig;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

@Service
@CacheConfig(cacheNames = {"dfHorseInfo"})
public class DfApiServiceCacheable implements DfApiService {

  private DFApiConfig dfApiConfig;

  private GenericMapper<Map<Long, RaceEvent>, Map<Long, RaceDTO>> genericMapperr;

  @Autowired
  public DfApiServiceCacheable(
      DFApiConfig dfApiConfig, GenericMapper<Map<Long, RaceEvent>, Map<Long, RaceDTO>> mapper) {
    this.dfApiConfig = dfApiConfig;
    this.genericMapperr = mapper;
  }

  @Override
  @Cacheable
  public Optional<Map<Long, RaceDTO>> getNextRaces(int categoryId, Collection<Long> eventIds)
      throws IOException {
    Optional<Map<Long, RaceEvent>> raceEventMap = getNextRacesInfo(categoryId, eventIds);
    Map<Long, RaceDTO> racesInfo = null;
    if (raceEventMap.isPresent()) {
      racesInfo =
          genericMapperr.mapGenericClasses(
              raceEventMap.get(), new TypeToken<Map<Long, RaceDTO>>() {});
    }

    return Optional.ofNullable(racesInfo);
  }

  private Optional<Map<Long, RaceEvent>> getNextRacesInfo(int categoryId, Collection<Long> eventIds)
      throws IOException {
    return dfApiConfig.api().getRaceEvents(categoryId, eventIds);
  }
}
