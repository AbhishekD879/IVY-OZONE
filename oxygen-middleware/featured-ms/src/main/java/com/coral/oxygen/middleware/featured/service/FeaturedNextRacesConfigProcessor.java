package com.coral.oxygen.middleware.featured.service;

import com.coral.oxygen.cms.api.CmsService;
import com.coral.oxygen.middleware.common.configuration.cfcache.DeliveryNetworkService;
import com.coral.oxygen.middleware.common.service.ModuleAdapter;
import com.coral.oxygen.middleware.common.utils.QueryFilterBuilder;
import com.coral.oxygen.middleware.featured.repository.NextRacesFilterRepository;
import com.coral.oxygen.middleware.pojos.model.NextRace;
import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig;
import com.coral.oxygen.middleware.pojos.model.cms.VirtualSportDto;
import com.coral.oxygen.middleware.pojos.model.cms.VirtualSportTrackDto;
import com.coral.oxygen.middleware.pojos.model.output.NextRaceFilterDto;
import com.coral.oxygen.middleware.pojos.model.output.NextRacesClfDto;
import com.egalacoral.spark.siteserver.api.*;
import com.egalacoral.spark.siteserver.model.Category;
import com.egalacoral.spark.siteserver.model.Event;
import com.google.gson.Gson;
import java.text.MessageFormat;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.function.Predicate;
import java.util.stream.Collectors;
import lombok.Data;
import lombok.experimental.UtilityClass;
import lombok.extern.slf4j.Slf4j;
import org.jetbrains.annotations.NotNull;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;
import org.springframework.util.StringUtils;

@Slf4j(topic = "next-races")
@Service
@ConditionalOnProperty(name = "featured.scheduled.task.enabled")
public class FeaturedNextRacesConfigProcessor extends ModuleAdapter {
  private final NextRacesFilterRepository repository;
  private final DeliveryNetworkService context;
  private final SiteServerApi siteServerApi;
  private final CmsService cmsService;
  private final QueryFilterBuilder queryFilterBuilder;
  private final String brand;

  private final int threshold;

  private final int eventsCount;

  private final int defaultTime;
  private final Gson gson = new Gson();

  @Autowired
  public FeaturedNextRacesConfigProcessor(
      DeliveryNetworkService context,
      SiteServerApi siteServerApi,
      NextRacesFilterRepository repository,
      CmsService cmsService,
      QueryFilterBuilder queryFilterBuilder,
      @Value("${cms.brand}") String brand,
      @Value("${next.races.threshold}") int threshold,
      @Value("${next.races.count}") int count,
      @Value("${next.races.default}") int defaultTime) {
    this.siteServerApi = siteServerApi;
    this.context = context;
    this.repository = repository;
    this.cmsService = cmsService;
    this.queryFilterBuilder = queryFilterBuilder;
    this.brand = brand;
    this.threshold = threshold;
    this.eventsCount = count;
    this.defaultTime = defaultTime;
  }

  public void processNextRaces(CmsSystemConfig cmsSystemConfig) {
    Arrays.stream(NextRace.values())
        .forEach(
            nextRace ->
                processEvents(cmsSystemConfig, nextRace.getCategoryId(), nextRace.getSportName()));
  }

  public void processEvents(CmsSystemConfig cmsConfig, String categoryId, String sportName) {
    log.info("process started for type {} {} ", categoryId, sportName);
    NextRaceFilterDto dto = getNextRaceFilterDto(categoryId);
    detectChangeInVirtualClassNames(dto, cmsConfig);
    for (Map.Entry<String, NextRacesClfDto> entry : dto.getNextRaces().entrySet()) {
      process(entry.getValue(), entry.getKey(), dto, sportName, cmsConfig);
    }
    NextRaceFilterDto savedDto = this.repository.save(dto);
    this.pushToCLF(savedDto);
  }

  private void detectChangeInVirtualClassNames(NextRaceFilterDto dto, CmsSystemConfig cmsConfig) {

    List<String> cms = getVirtualClassNames(dto.getCategoryId(), cmsConfig);
    String excludeTime = getVirtalExcludeTime(dto.getCategoryId(), cmsConfig);
    if (isVirtualConfigurationChanged(excludeTime, cms, dto)) {
      dto.setVirtualClassNames(cms);
      NextRacesClfDto allDto = dto.getNextRaces().get(TypeFlagCodes.ALL.getTypeCode());
      allDto.setLastEventTime(Instant.now());
      setExcludeTimes(dto, excludeTime);
      dto.setExcludeTimeRange(excludeTime);
    }
  }

  private void setExcludeTimes(NextRaceFilterDto dto, String time) {
    if (StringUtils.hasLength(time)) {
      Map<String, Object> timeObject = gson.fromJson(time, Map.class);
      dto.setExcludeFrom(
          createInstantFromTimeString(
              (Map<String, Object>) timeObject.get(CmsConfigConstants.FROM)));
      dto.setExcludeTo(
          createInstantFromTimeString((Map<String, Object>) timeObject.get(CmsConfigConstants.TO)));
    } else {
      // set some value that doesn't falls under today and tomorrow.
      dto.setExcludeFrom(Instant.now().minus(NextRacesConstants.ALTERNATE_TIME, ChronoUnit.HOURS));
      dto.setExcludeTo(Instant.now().minus(NextRacesConstants.ALTERNATE_TIME, ChronoUnit.HOURS));
    }
  }

  private Instant createInstantFromTimeString(Map<String, Object> timeMap) {
    int hh = parseString(timeMap.get(CmsConfigConstants.HOURS));
    int mm = parseString(timeMap.get(CmsConfigConstants.MINS));
    int ss = parseString(timeMap.get(CmsConfigConstants.SEC));
    return Instant.now()
        .truncatedTo(ChronoUnit.DAYS)
        .plus(hh, ChronoUnit.HOURS)
        .plus(mm, ChronoUnit.MINUTES)
        .plus(ss, ChronoUnit.SECONDS);
  }

  private int parseString(Object time) {
    try {
      return (int) Double.parseDouble(String.valueOf(time));
    } catch (Exception ex) {
      return 0;
    }
  }

  private boolean isVirtualConfigurationChanged(
      String excludeTime, List<String> cms, NextRaceFilterDto dto) {
    return !excludeTime.equals(dto.getExcludeTimeRange())
        || !org.apache.commons.collections4.CollectionUtils.isEqualCollection(
            dto.getVirtualClassNames(), cms);
  }

  private NextRaceFilterDto getNextRaceFilterDto(String categoryId) {
    return this.repository
        .findByCategoryId(categoryId)
        .orElse(createNewNextRaceFilterDto(categoryId));
  }

  private NextRaceFilterDto createNewNextRaceFilterDto(String categoryId) {
    NextRaceFilterDto dto = new NextRaceFilterDto();
    dto.setCategoryId(categoryId);
    Map<String, NextRacesClfDto> nextRaces = new HashMap<>();
    NextRacesConstants.TYPE_CODES.forEach(code -> updateMap(code, nextRaces));
    dto.setNextRaces(nextRaces);
    return dto;
  }

  private void updateMap(String type, Map<String, NextRacesClfDto> nextRacesMap) {
    NextRacesClfDto clfDto = new NextRacesClfDto();
    clfDto.setLastEventTime(Instant.now());
    nextRacesMap.put(type, clfDto);
  }

  /** Method to pre-check the condition to fetch events from site server in one go. */
  private void fetchNewEvents(
      NextRacesClfDto clf,
      String typeFlagCodes,
      NextRaceFilterDto dto,
      String sportName,
      CmsSystemConfig cmsConfig) {
    List<EventInfoDto> filteredEvents =
        getEventsByCategory(
                dto.getCategoryId(),
                sportName,
                dto.getVirtualClassNames(),
                typeFlagCodes,
                cmsConfig)
            .stream()
            .filter(getEventInfoDtoPredicate(typeFlagCodes, dto))
            .toList();
    clf.setLastEventTime(Instant.now().plus(defaultTime, ChronoUnit.MINUTES));
    clf.setEnabled(Boolean.FALSE);
    if (!CollectionUtils.isEmpty(filteredEvents)) {
      clf.setLastEventTime(getTheLastEventStartTime(filteredEvents));
      clf.setEnabled(Boolean.TRUE);
    }
  }

  private boolean evaluateAllFlag(EventInfoDto eventInfoDto, NextRaceFilterDto dto) {

    return eventInfoDto.getTypeFlagCodes().contains(TypeFlagCodes.UK.getTypeCode())
        || eventInfoDto.getTypeFlagCodes().contains(TypeFlagCodes.IE.getTypeCode())
        || eventInfoDto.getTypeFlagCodes().contains(TypeFlagCodes.INT.getTypeCode())
        || processForVRFlag(eventInfoDto, dto);
  }

  private boolean processForVRFlag(EventInfoDto eventInfoDto, NextRaceFilterDto dto) {
    return NextRacesConstants.VIRTUALS_ID.equalsIgnoreCase(eventInfoDto.getCategoryId())
        && eventInfoDto.getTypeFlagCodes().contains(TypeFlagCodes.VR.getTypeCode())
        && !(Instant.parse(eventInfoDto.getStartTime())
                .isAfter(
                    dto.getExcludeFrom()
                        .minus(NextRacesConstants.ALTERNATE_TIME, ChronoUnit.SECONDS))
            && Instant.parse(eventInfoDto.getStartTime())
                .isBefore(
                    dto.getExcludeTo()
                        .plus(NextRacesConstants.ALTERNATE_TIME, ChronoUnit.SECONDS)));
  }

  @NotNull
  private Predicate<EventInfoDto> getEventInfoDtoPredicate(
      String typeFlagCode, NextRaceFilterDto dto) {
    if (TypeFlagCodes.ALL.getTypeCode().equalsIgnoreCase(typeFlagCode)) {
      return eventInfoDto -> evaluateAllFlag(eventInfoDto, dto);
    }
    return eventInfoDto -> eventInfoDto.getTypeFlagCodes().contains(typeFlagCode);
  }

  private void process(
      NextRacesClfDto nextRacesClfDto,
      String typeFlagCode,
      NextRaceFilterDto dto,
      String sportName,
      CmsSystemConfig cmsConfig) {
    if (isWithinThreshold(nextRacesClfDto.getLastEventTime())) {
      fetchNewEvents(nextRacesClfDto, typeFlagCode, dto, sportName, cmsConfig);
    }
  }

  private boolean isWithinThreshold(Instant eventTime) {
    return Instant.now().plus(threshold, ChronoUnit.MINUTES).isAfter(eventTime);
  }

  public void pushToCLF(NextRaceFilterDto dto) {
    Map<String, Boolean> clfMap =
        dto.getNextRaces().entrySet().stream()
            .collect(Collectors.toMap(Map.Entry::getKey, e -> e.getValue().isEnabled()));
    log.info(
        "FeaturedNextRacesConfigProcessor::Publishing to the Cloudflare::{} and category::{}",
        clfMap,
        dto.getCategoryId());
    context.upload(
        brand,
        MessageFormat.format(NextRacesConstants.PATH_TEMPLATE, brand),
        dto.getCategoryId(),
        clfMap);
  }

  private List<EventInfoDto> getEventsByCategory(
      String categoryId,
      String sportName,
      List<String> virtualClassNames,
      String typeFlagCode,
      CmsSystemConfig cmsConfig) {
    Set<String> activeClassIds = getActiveClassIds(categoryId);
    Set<String> virtualClassIds = new HashSet<>();
    String virtualEnabled;

    if (typeFlagCode.equalsIgnoreCase(TypeFlagCodes.VR.getTypeCode())) {
      virtualClassIds = getVirtualClassIds(sportName, null);
    }
    if (typeFlagCode.equalsIgnoreCase(TypeFlagCodes.ALL.getTypeCode())) {
      virtualEnabled = isVirtualsEnabled(categoryId, cmsConfig);
      if (NextRacesConstants.VIRTUALS_ENABLED.equalsIgnoreCase(virtualEnabled)) {
        virtualClassIds = getVirtualClassIds(sportName, virtualClassNames);
      }
      typeFlagCode = mapTypeFlagCodes(virtualEnabled);
    }
    activeClassIds.addAll(virtualClassIds);

    return getNextRacesFromSiteServe(activeClassIds.stream().toList(), typeFlagCode);
  }

  private String isVirtualsEnabled(String categoryId, CmsSystemConfig cmsSystemConfig) {
    try {
      return NextRace.HR.getCategoryId().equalsIgnoreCase(categoryId)
          ? (String) cmsSystemConfig.getNextRaces().get(CmsConfigConstants.VIRTUALS_ENABLED)
          : (String)
              cmsSystemConfig.getGreyhoundNextRaces().get(CmsConfigConstants.VIRTUALS_ENABLED);
    } catch (Exception e) {
      log.error("Parsing Exception from cms config");
      return "No";
    }
  }

  private Set<String> getVirtualClassIds(String sportName, List<String> virtualClassNames) {
    return this.cmsService.getVirtualSportsByBrand().stream()
        .filter(e -> e.getTitle().equalsIgnoreCase(sportName))
        .findAny()
        .map(VirtualSportDto::getTracks)
        .filter(org.apache.commons.collections4.CollectionUtils::isNotEmpty)
        .orElse(new ArrayList<>())
        .stream()
        .filter(predicate(virtualClassNames))
        .map(VirtualSportTrackDto::getClassId)
        .collect(Collectors.toSet());
  }

  private Predicate<VirtualSportTrackDto> predicate(List<String> virtualClassNames) {
    if (org.apache.commons.collections4.CollectionUtils.isEmpty(virtualClassNames)) {
      return e -> true;
    }
    return e -> virtualClassNames.contains(e.getTitle().trim());
  }

  private List<String> getVirtualClassNames(String categoryId, CmsSystemConfig cmsSystemConfig) {
    try {
      return NextRace.HR.getCategoryId().equalsIgnoreCase(categoryId)
          ? ((List<String>)
                  cmsSystemConfig.getNextRaces().get(CmsConfigConstants.VIRTUALS_INCLUDED))
              .stream().map(String::trim).toList()
          : ((List<String>)
                  cmsSystemConfig.getGreyhoundNextRaces().get(CmsConfigConstants.VIRTUALS_INCLUDED))
              .stream().map(String::trim).toList();
    } catch (Exception ex) {
      log.info("cms config null {} ", cmsSystemConfig);
      return Collections.emptyList();
    }
  }

  private String getVirtalExcludeTime(String categoryId, CmsSystemConfig cmsSystemConfig) {
    return String.valueOf(
        (NextRace.HR.getCategoryId().equalsIgnoreCase(categoryId)
            ? cmsSystemConfig.getNextRaces().get(CmsConfigConstants.VIRTUALS_EXCLUDED)
            : cmsSystemConfig.getGreyhoundNextRaces().get(CmsConfigConstants.VIRTUALS_EXCLUDED)));
  }

  private Set<String> getActiveClassIds(String categoryId) {
    SimpleFilter simpleFilter = this.queryFilterBuilder.getActiveClassesForTheCategory(categoryId);
    ExistsFilter existsFilter = QueryFilterBuilder.getEmptyExistingFilter();
    return this.siteServerApi
        .getClasses(simpleFilter, existsFilter)
        .orElse(new ArrayList<>())
        .stream()
        .map(Category::getId)
        .map(Object::toString)
        .collect(Collectors.toSet());
  }

  private List<EventInfoDto> getNextRacesFromSiteServe(
      List<String> classIds, String typeFlagCodes) {
    SimpleFilter simpleFilter =
        this.queryFilterBuilder.buildSimpleFilterForNextRaces(typeFlagCodes);
    ExistsFilter existsFilter = this.queryFilterBuilder.buildExistsFilterForNextRaces();
    LimitRecordsFilter limitRecordsFilter =
        this.queryFilterBuilder.buildLimitRecordsFilterForNextRaces();
    LimitToFilter limitToFilter = new LimitToFilter.LimitToFilterBuilder().build();
    return this.siteServerApi
        .getNextNEventToOutcomeForClass(
            eventsCount,
            classIds,
            simpleFilter,
            existsFilter,
            limitToFilter,
            limitRecordsFilter,
            true,
            false)
        .map(events -> events.stream().map(EventInfoMapper::eventInfoDto).toList())
        .orElse(new ArrayList<>());
  }

  private Instant getTheLastEventStartTime(List<EventInfoDto> events) {
    return events.stream()
        .sorted(NextRacesConstants.startTimeComparator)
        .map(EventInfoDto::getStartTime)
        .map(Instant::parse)
        .findFirst()
        .orElse(Instant.now());
  }

  private static List<String> getTypeFlagCodes() {
    return Arrays.stream(TypeFlagCodes.values())
        .map(TypeFlagCodes::getTypeCode)
        .map(String::trim)
        .toList();
  }

  private String mapTypeFlagCodes(String virtualsEnabled) {
    List<String> unSupportedCodes =
        NextRacesConstants.VIRTUALS_ENABLED.equalsIgnoreCase(virtualsEnabled)
            ? List.of(TypeFlagCodes.ALL.getTypeCode())
            : List.of(TypeFlagCodes.ALL.getTypeCode(), TypeFlagCodes.VR.getTypeCode());

    return Arrays.stream(TypeFlagCodes.values())
        .map(TypeFlagCodes::getTypeCode)
        .map(String::trim)
        .filter(code -> !unSupportedCodes.contains(code))
        .collect(Collectors.joining(","));
  }

  enum TypeFlagCodes {
    ALL("ALL"),

    UK("UK"),

    IE("IE"),
    INT("INT"),
    VR("VR");

    private final String typeCode;

    TypeFlagCodes(String typeCode) {
      this.typeCode = typeCode;
    }

    private String getTypeCode() {
      return typeCode;
    }
  }

  @Data
  static class EventInfoDto {
    String id;
    String typeFlagCodes;
    String startTime;
    String categoryId;
  }

  private static class EventInfoMapper {
    static EventInfoDto eventInfoDto(Event obEvent) {
      EventInfoDto dto = new EventInfoDto();
      dto.setId(obEvent.getId());
      dto.setStartTime(obEvent.getStartTime());
      dto.setTypeFlagCodes(obEvent.getTypeFlagCodes());
      dto.setCategoryId(obEvent.getCategoryId());
      return dto;
    }
  }

  @UtilityClass
  static class CmsConfigConstants {
    static final String VIRTUALS_INCLUDED = "virtualRacesIncluded";
    static final String VIRTUALS_EXCLUDED = "VirtualsExcludeTimeRange";

    static final String FROM = "from";

    static final String TO = "to";

    static final String HOURS = "hh";

    static final String MINS = "mm";

    static final String SEC = "ss";

    static final String VIRTUALS_ENABLED = "isVirtualRacesEnabled";
  }

  @UtilityClass
  static class NextRacesConstants {
    static final String VIRTUALS_ENABLED = "Yes";

    static final String VIRTUALS_ID = "39";

    static final List<String> TYPE_CODES = getTypeFlagCodes();

    static final String PATH_TEMPLATE = "api/{0}/next_races";

    static final int ALTERNATE_TIME = 1;

    static final Comparator<EventInfoDto> startTimeComparator =
        Comparator.comparing(
            EventInfoDto::getStartTime, Comparator.nullsLast(Comparator.reverseOrder()));
  }
}
