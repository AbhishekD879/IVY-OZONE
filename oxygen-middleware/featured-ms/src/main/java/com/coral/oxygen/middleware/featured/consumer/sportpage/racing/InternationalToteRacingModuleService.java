package com.coral.oxygen.middleware.featured.consumer.sportpage.racing;

import static java.util.Comparator.*;

import com.coral.oxygen.middleware.common.mappers.ExternalKeyMapper;
import com.coral.oxygen.middleware.common.mappers.RacingModuleDataMapper;
import com.coral.oxygen.middleware.common.mappers.SiteServeChildrenMapper;
import com.coral.oxygen.middleware.featured.consumer.sportpage.RacingModuleType;
import com.coral.oxygen.middleware.featured.service.injector.FeaturedSiteServerService;
import com.coral.oxygen.middleware.pojos.model.cms.featured.CmsRacingModule;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule;
import com.coral.oxygen.middleware.pojos.model.output.InternationalToteRaceData;
import com.coral.oxygen.middleware.pojos.model.output.featured.InternationalToteRaceModule;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.ExternalKeys;
import java.time.Duration;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.ObjectUtils;
import org.jetbrains.annotations.NotNull;
import org.springframework.stereotype.Service;

@Slf4j
@Service
@RequiredArgsConstructor
public class InternationalToteRacingModuleService
    extends AbstractRacingModuleService<InternationalToteRaceData, InternationalToteRaceModule> {

  private static final String TOTE_EXTERNAL_KEY_CODE = "OBEvLinkNonTote";
  private static final int TOTE_SELECTION_RANGE_HOURS = 24;
  private static final Comparator<InternationalToteRaceData> TOTE_EVENTS_COMPARATOR =
      comparing(InternationalToteRaceData::getResulted, nullsLast(reverseOrder()))
          .thenComparing(InternationalToteRaceData::getStartTime, nullsLast(naturalOrder()))
          .thenComparing(InternationalToteRaceData::getTypeName, nullsLast(naturalOrder()));

  private final FeaturedSiteServerService siteServerService;
  private final RacingModuleDataMapper racingEventMapper;
  private final ExternalKeyMapper externalKeysMapper;
  private final SiteServeChildrenMapper childrenMapper;

  @Override
  protected InternationalToteRaceModule createModule(
      SportModule cmsModule, RacingModuleType racingModuleType, boolean active) {
    return new InternationalToteRaceModule(cmsModule, active);
  }

  @Override
  protected List<InternationalToteRaceData> getData(
      SportModule cmsModule,
      List<CmsRacingModule> racingConfigs,
      RacingModuleType racingModuleType) {
    return getInternationalToteEvents(racingConfigs);
  }

  private List<InternationalToteRaceData> getInternationalToteEvents(
      List<CmsRacingModule> racingConfigs) {
    List<String> classes = getInternationalToteClasses(racingConfigs);
    if (ObjectUtils.isEmpty(classes)) {
      return Collections.emptyList();
    }

    int selectionRange = getEventsSelectionRange(racingConfigs);
    List<Children> eventsAndExternalKeys =
        siteServerService.getInternationalToteRacingEventsAndExternalKeys(
            classes, Duration.ofHours(selectionRange));
    List<Event> events = childrenMapper.map(eventsAndExternalKeys, Children::getEvent);
    List<ExternalKeys> externalKeys =
        childrenMapper.map(eventsAndExternalKeys, Children::getExternalKeys);
    Map<String, String> externalKeyEvents =
        externalKeys.stream()
            .filter(k -> TOTE_EXTERNAL_KEY_CODE.equalsIgnoreCase(k.getExternalKeyTypeCode()))
            .flatMap(k -> externalKeysMapper.mapToEventIds(k).entrySet().stream())
            .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));

    return events.stream()
        .filter(e -> externalKeyEvents.containsKey(e.getId()))
        .map(e -> toToteRaceData(e, externalKeyEvents))
        .sorted(TOTE_EVENTS_COMPARATOR)
        .collect(Collectors.toList());
  }

  private InternationalToteRaceData toToteRaceData(
      Event event, Map<String, String> externalKeyEvents) {
    return racingEventMapper.mapInternationalToteData(
        event, TOTE_EXTERNAL_KEY_CODE, externalKeyEvents.get(event.getId()));
  }

  private int getEventsSelectionRange(List<CmsRacingModule> racingConfigs) {
    return racingConfigs.stream()
        .mapToInt(c -> c.getRacingConfig().getTimeRangeHours())
        .filter(v -> v > 0)
        .max()
        .orElse(TOTE_SELECTION_RANGE_HOURS);
  }

  @NotNull
  private List<String> getInternationalToteClasses(List<CmsRacingModule> racingConfigs) {
    return racingConfigs.stream()
        .mapToInt(c -> c.getRacingConfig().getClassId())
        .filter(v -> v > 0)
        .mapToObj(String::valueOf)
        .collect(Collectors.toList());
  }
}
