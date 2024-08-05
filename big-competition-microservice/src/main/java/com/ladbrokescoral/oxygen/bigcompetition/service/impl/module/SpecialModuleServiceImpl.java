package com.ladbrokescoral.oxygen.bigcompetition.service.impl.module;

import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.SpecialsModuleDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.siteServe.EventDto;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.SiteServeEventDtoMapper;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.module.SpecialsModuleDtoMapper;
import com.ladbrokescoral.oxygen.bigcompetition.service.SiteServeApiService;
import com.ladbrokescoral.oxygen.bigcompetition.service.SpecialModuleService;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionSpecialModuleData;
import java.util.*;
import java.util.function.Function;
import java.util.stream.Collectors;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.util.Assert;

@Service
// @Slf4j
@AllArgsConstructor
public class SpecialModuleServiceImpl implements SpecialModuleService {

  private final SiteServeApiService siteServeApiService;

  @Override
  public SpecialsModuleDto process(CompetitionModule module) {
    SpecialsModuleDto moduleDto = SpecialsModuleDtoMapper.INSTANCE.toDto(module);

    Set<Event> events = new HashSet<>();
    events.addAll(
        getEventsWithOutcomes(
            module,
            CompetitionSpecialModuleData::getTypeIds,
            siteServeApiService::getEventWithOutcomesForTypeSpecial));
    events.addAll(
        getEventsWithOutcomes(
            module,
            CompetitionSpecialModuleData::getEventIds,
            siteServeApiService::getEventWithOutcomesForEventSpecial));

    Set<EventDto> result =
        events.stream().map(SiteServeEventDtoMapper.INSTANCE::toDto).collect(Collectors.toSet());
    Assert.isTrue(
        !result.isEmpty(),
        String.format(
            "Can't retrieve special events for special module %s with special data %s ",
            module.getId(), module.getSpecialModuleData()));
    moduleDto.setEvents(result);

    return moduleDto;
  }

  private List<Event> getEventsWithOutcomes(
      CompetitionModule competitionModule,
      Function<CompetitionSpecialModuleData, List<Integer>> getIds,
      Function<List<Integer>, List<Event>> getEventWithOutcomesForTypeSpecial) {
    return Optional.ofNullable(competitionModule.getSpecialModuleData())
        .map(getIds)
        .filter(list -> !list.isEmpty())
        .map(getEventWithOutcomesForTypeSpecial)
        .orElseGet(Collections::emptyList);
  }
}
