package com.ladbrokescoral.oxygen.bigcompetition.service.impl.module;

import com.ladbrokescoral.oxygen.bigcompetition.dto.module.OutrightsModuleDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.group.CompetitionMarketDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.siteServe.EventDto;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.SiteServeEventDtoMapper;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.module.OutrigtsModuleDtoMapper;
import com.ladbrokescoral.oxygen.bigcompetition.service.CompetitionParticipantService;
import com.ladbrokescoral.oxygen.bigcompetition.service.OutrightsModuleService;
import com.ladbrokescoral.oxygen.bigcompetition.service.SiteServeApiService;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import java.util.Optional;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.util.Assert;

@Service
@AllArgsConstructor
public class OutrightsModuleServiceImpl implements OutrightsModuleService {

  private final SiteServeApiService siteServeApiService;
  private final CompetitionParticipantService competitionParticipantService;

  @Override
  public OutrightsModuleDto process(CompetitionModule module) {
    OutrightsModuleDto moduleDto = OutrigtsModuleDtoMapper.INSTANCE.toDto(module);

    Assert.isTrue(
        !moduleDto.getMarkets().isEmpty(), "Markets should be configured for outright module");
    moduleDto
        .getMarkets()
        .forEach(
            marketDto -> {
              Optional<EventDto> outcome =
                  getSiteServeOutcome(marketDto, moduleDto.getCompetitionUriFromPath());
              outcome.ifPresent(marketDto::setData);
            });
    return moduleDto;
  }

  private Optional<EventDto> getSiteServeOutcome(
      CompetitionMarketDto input, String competitionUri) {
    return siteServeApiService
        .getEventWithOutcomesForMarket(input.getMarketId())
        .map(SiteServeEventDtoMapper.INSTANCE::toDto)
        .map(
            eventDto ->
                competitionParticipantService.populateEventWithParticipants(
                    eventDto, competitionUri));
  }
}
