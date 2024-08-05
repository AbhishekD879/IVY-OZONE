package com.egalacoral.spark.timeform.service.greyhound;

import com.egalacoral.spark.siteserver.api.SiteServerAPI;
import com.egalacoral.spark.timeform.model.greyhound.Meeting;
import com.egalacoral.spark.timeform.service.greyhound.mapper.MeetingNameMapper;
import com.egalacoral.spark.timeform.service.greyhound.mapper.MeetingTypeMapper;
import java.util.ArrayList;
import java.util.List;
import javax.annotation.PostConstruct;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class MeetingMappingService {

  private static final Logger LOGGER = LoggerFactory.getLogger(MeetingMappingService.class);

  @Autowired private SiteServerAPI siteServerAPI;

  private List<MeetingDataMapper> dataMappersList = new ArrayList<>();

  @Value("${siteserver.class.id}")
  private String categoryId = "198";

  @Autowired private MeetingAbbreviationService abbreviationService;

  @PostConstruct
  public void init() {
    dataMappersList.add(new MeetingNameMapper());
    dataMappersList.add(new MeetingTypeMapper(siteServerAPI, categoryId, abbreviationService));
  }

  public void initMappers() {
    dataMappersList.forEach(mapper -> mapper.init());
  }

  public void map(Meeting meeting) {
    dataMappersList.forEach(mapper -> map(meeting, mapper));
  }

  protected void map(Meeting meeting, MeetingDataMapper handler) {
    handler.map(meeting);
  }

  public void map(List<Meeting> meetings) {
    meetings.stream().forEach(meeting -> map(meeting));
  }
}
