package com.ladbrokescoral.oxygen.bigcompetition.service.impl.module;

import com.ladbrokescoral.oxygen.bigcompetition.dto.module.NextEventsModuleDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.siteServe.EventDto;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.SiteServeEventDtoMapper;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.module.NextEventsModuleDtoMapper;
import com.ladbrokescoral.oxygen.bigcompetition.service.CmsApiService;
import com.ladbrokescoral.oxygen.bigcompetition.service.NextEventsModuleService;
import com.ladbrokescoral.oxygen.bigcompetition.service.SiteServeApiService;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import java.util.Set;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
// @Slf4j
public class NextEventsModuleServiceImpl extends NextEventsAbstractService
    implements NextEventsModuleService {

  private final SiteServeApiService siteServeApiService;

  @Autowired
  public NextEventsModuleServiceImpl(
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
        this.siteServeApiService.getNextEventForType(module.getTypeId()).stream()
            .map(SiteServeEventDtoMapper.INSTANCE::toDto)
            .collect(Collectors.toSet());

    events = populateEventsWithParticipants(moduleDto.getCompetitionUriFromPath(), events);
    moduleDto.setEvents(events);
    moduleDto.setTypeId(module.getTypeId());

    return moduleDto;
  }
}
