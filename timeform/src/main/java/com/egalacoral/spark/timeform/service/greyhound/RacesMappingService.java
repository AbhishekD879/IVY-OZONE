package com.egalacoral.spark.timeform.service.greyhound;

import com.egalacoral.spark.siteserver.api.SiteServerAPI;
import com.egalacoral.spark.timeform.model.greyhound.Meeting;
import com.egalacoral.spark.timeform.service.greyhound.mapper.MeetingOpenBetIdMapper;
import com.egalacoral.spark.timeform.service.greyhound.mapper.MeetingSelectionMapper;
import java.util.ArrayList;
import java.util.List;
import javax.annotation.PostConstruct;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/** Created by Igor.Domshchikov on 8/18/2016. */
@Service
public class RacesMappingService {

  private static final Logger LOGGER = LoggerFactory.getLogger(RacesMappingService.class);

  private SiteServerAPI siteServerAPI;
  private List<MeetingDataMapper> dataMapperList = new ArrayList<>();

  @Autowired
  public RacesMappingService(SiteServerAPI siteServerAPI) {
    this.siteServerAPI = siteServerAPI;
  }

  public void initMappers() {
    dataMapperList.forEach(mapper -> mapper.init());
  }

  @PostConstruct
  public void init() {
    dataMapperList.add(new MeetingOpenBetIdMapper(siteServerAPI));
    dataMapperList.add(new MeetingSelectionMapper(siteServerAPI));
  }

  public void map(Meeting meeting) {
    dataMapperList.forEach(mapper -> map(meeting, mapper));
  }

  protected void map(Meeting meeting, MeetingDataMapper handler) {
    handler.map(meeting);
  }

  public void map(List<Meeting> meetings) {
    meetings.stream().forEach(meeting -> map(meeting));
  }
}
