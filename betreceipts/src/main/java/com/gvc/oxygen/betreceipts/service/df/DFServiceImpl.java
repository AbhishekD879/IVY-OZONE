package com.gvc.oxygen.betreceipts.service.df;

import com.coral.oxygen.df.model.RaceEvent;
import com.gvc.oxygen.betreceipts.config.DFApiConfig;
import com.gvc.oxygen.betreceipts.dto.RaceDTO;
import com.gvc.oxygen.betreceipts.mapping.GenericMapper;
import java.io.IOException;
import java.util.*;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.TypeToken;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class DFServiceImpl implements DFService {

  private DFApiConfig dfApiConfig;

  private GenericMapper<Map<Long, RaceEvent>, Map<Long, RaceDTO>> mapper;

  @Autowired
  public DFServiceImpl(
      DFApiConfig dfApiConfig, GenericMapper<Map<Long, RaceEvent>, Map<Long, RaceDTO>> mapper) {
    this.dfApiConfig = dfApiConfig;
    this.mapper = mapper;
  }

  @Override
  public Optional<Map<Long, RaceDTO>> getNextRaces(int categoryId, Collection<Long> eventIds)
      throws IOException {
    log.info("calling df api with values category {}", categoryId);
    Optional<Map<Long, RaceEvent>> raceEventMap = getNextRacesInfo(categoryId, eventIds);
    Map<Long, RaceDTO> racesInfo = null;

    if (raceEventMap.isPresent()) {
      racesInfo =
          mapper.mapGenericClasses(raceEventMap.get(), new TypeToken<Map<Long, RaceDTO>>() {});
    }

    return Optional.ofNullable(racesInfo);
  }

  private Optional<Map<Long, RaceEvent>> getNextRacesInfo(int categoryId, Collection<Long> eventIds)
      throws IOException {
    return dfApiConfig.api().getRaceEvents(categoryId, eventIds);
  }
}
