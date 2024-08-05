package com.ladbrokescoral.oxygen.bigcompetition.service.impl.module;

import com.ladbrokescoral.oxygen.bigcompetition.dto.module.NextEventsModuleDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.siteServe.EventDto;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.SiteServeEventDtoMapper;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.module.NextEventsModuleDtoMapper;
import com.ladbrokescoral.oxygen.bigcompetition.service.CmsApiService;
import com.ladbrokescoral.oxygen.bigcompetition.service.NextEventsIndividualModuleService;
import com.ladbrokescoral.oxygen.bigcompetition.service.SiteServeApiService;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import java.util.Set;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.Assert;

@Service
// @Slf4j
public class NextEventsIndividualModuleServiceImpl extends NextEventsAbstractService
    implements NextEventsIndividualModuleService {

  private final SiteServeApiService siteServeApiService;

  public NextEventsIndividualModuleServiceImpl(
      SiteServeApiService siteServeApiService,
      CmsApiService cmsApiService,
      @Value("${cms.brand}") String brand) {
    super(siteServeApiService, cmsApiService, brand);
    this.siteServeApiService = siteServeApiService;
  }

  @Override
  public NextEventsModuleDto process(CompetitionModule module) {
    NextEventsModuleDto moduleDto = NextEventsModuleDtoMapper.INSTANCE.toDto(module);

    Set<EventDto> events =
        this.siteServeApiService.getNextEventForEvent(module.getEventIds()).stream()
            .map(SiteServeEventDtoMapper.INSTANCE::toDto)
            .collect(Collectors.toSet());
    Assert.isTrue(
        !events.isEmpty(),
        String.format("Can't find events for next events individual module - %s", module.getId()));
    events = populateEventsWithParticipants(moduleDto.getCompetitionUriFromPath(), events);
    moduleDto.setEvents(events);
    moduleDto.setTypeId(module.getTypeId());

    return moduleDto;
  }
}
