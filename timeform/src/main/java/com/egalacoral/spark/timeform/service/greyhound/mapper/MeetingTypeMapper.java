package com.egalacoral.spark.timeform.service.greyhound.mapper;

import com.egalacoral.spark.siteserver.api.BinaryOperation;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerAPI;
import com.egalacoral.spark.siteserver.model.Type;
import com.egalacoral.spark.timeform.model.greyhound.Meeting;
import com.egalacoral.spark.timeform.service.greyhound.MeetingAbbreviationService;
import com.egalacoral.spark.timeform.service.greyhound.MeetingDataMapper;
import java.util.HashSet;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class MeetingTypeMapper implements MeetingDataMapper {

  private static final String SITE_SERVER_FIELD_CLASS_ID = "class.id";
  private SiteServerAPI siteServeAPI;
  private String classId;
  private Optional<List<Type>> list = Optional.empty();
  private static final Logger LOGGER = LoggerFactory.getLogger(MeetingTypeMapper.class);
  private MeetingAbbreviationService abbreviationService;

  public MeetingTypeMapper(
      SiteServerAPI siteServeAPI, String classId, MeetingAbbreviationService abbreviationService) {
    this.siteServeAPI = siteServeAPI;
    this.classId = classId;
    this.abbreviationService = abbreviationService;
  }

  @Override
  public void map(Meeting meeting) {
    if (list.isPresent()) {
      String name = meeting.getName();
      List<Type> types =
          list.get().stream().filter(t -> containsName(name, t)).collect(Collectors.toList());
      if (types != null && !types.isEmpty()) {
        types.stream().forEachOrdered(type -> map(type, meeting, name));
      } else {
        LOGGER.info("Can't find types by name {}. Available types {}", name, list.get());
      }
    } else {
      LOGGER.error("Can't find types for classId {}", classId);
      throw new RuntimeException("Can't get types from SiteServer API");
    }
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
    return t.getName().toLowerCase().contains(abbreviation.toLowerCase());
  }

  protected Optional<List<Type>> getSiteServeTypes() {
    SimpleFilter.SimpleFilterBuilder builder = new SimpleFilter.SimpleFilterBuilder();
    builder.addBinaryOperation(SITE_SERVER_FIELD_CLASS_ID, BinaryOperation.equals, classId);
    final SimpleFilter simpleFilter = builder.build();
    Optional<List<Type>> listType = siteServeAPI.getClassToSubType(simpleFilter);
    return listType;
  }

  private void map(Type type, Meeting meeting, String name) {
    LOGGER.info("Found type {} by type name {}", type, name);
    if (meeting.getOpenBetIds() == null) {
      meeting.setOpenBetIds(new HashSet<>());
    }
    meeting.getOpenBetIds().add(type.getId());
    LOGGER.info("Mapped event type id {} to {} ", type.getId(), meeting);
  }

  @Override
  public void init() {
    this.list = getSiteServeTypes();
  }
}
