package com.egalacoral.spark.timeform.service.horseracing.mapper;

import com.egalacoral.spark.siteserver.api.BinaryOperation;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerAPI;
import com.egalacoral.spark.siteserver.model.Type;
import com.egalacoral.spark.timeform.model.horseracing.HRMeeting;
import com.egalacoral.spark.timeform.service.greyhound.MeetingAbbreviationService;
import java.util.*;
import java.util.stream.Collectors;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class HorseRacingMeetingTypeMapper {

  private static final Logger LOGGER = LoggerFactory.getLogger(HorseRacingMeetingTypeMapper.class);
  private static final String SITE_SERVER_FIELD_CLASS_ID = "class.id";

  private final SiteServerAPI siteServeAPI;
  private final String classId;
  private final MeetingAbbreviationService abbreviationService;

  private Optional<List<Type>> list = Optional.empty();

  @Autowired
  public HorseRacingMeetingTypeMapper(
      SiteServerAPI siteServeAPI,
      @Value("${siteserver.horseracing.live.class.id}") String classId,
      MeetingAbbreviationService abbreviationService) {
    this.siteServeAPI = siteServeAPI;
    this.classId = classId;
    this.abbreviationService = abbreviationService;
  }

  public Set<Integer> getOBIdsForMeeting(HRMeeting meeting) {
    meeting.getKey();
    String name = meeting.getCourseName();
    Set<Integer> set;
    if (list.isPresent()) {
      set =
          list.get().stream()
              .filter(t -> containsName(name, t))
              .map(Type::getId)
              .collect(Collectors.toSet());
    } else {
      LOGGER.warn("Cannot map HorseRacing meeting with course name {}", name);
      throw new RuntimeException("Can't get events with outcomes from SiteServer API");
    }
    return set;
  }

  protected boolean containsName(String name, Type type) {
    boolean containsAbbreviation = false;
    List<String> names = abbreviationService.getAbbreviations(name);
    for (String abbreviation : names) {
      if (containsName(type, abbreviation)) {
        containsAbbreviation = true;
        break;
      }
    }
    return containsName(type, name) || containsAbbreviation;
  }

  protected boolean containsName(Type t, String abbreviation) {
    return t.getName().toLowerCase().contains(abbreviation.toLowerCase())
        || abbreviation.toLowerCase().contains(t.getName().toLowerCase());
  }

  public void loadTypesFromOB() {
    list = getSiteServeTypes();
  }

  protected Optional<List<Type>> getSiteServeTypes() {
    SimpleFilter.SimpleFilterBuilder builder = new SimpleFilter.SimpleFilterBuilder();
    builder.addBinaryOperation(SITE_SERVER_FIELD_CLASS_ID, BinaryOperation.equals, classId);
    final SimpleFilter simpleFilter = builder.build();
    Optional<List<Type>> typeList = siteServeAPI.getClassToSubType(simpleFilter);
    return typeList;
  }
}
