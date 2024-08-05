package com.ladbrokescoral.oxygen.bigcompetition.service.impl.module;

import static java.util.stream.Collectors.toMap;

import com.egalacoral.spark.siteserver.model.Aggregation;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.KnockoutModuleDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.knockout.CompetitionKnockoutEventDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.knockout.CompetitionKnockoutModuleDataDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.statsCenter.MatchResultDto;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.KnockoutModuleDataDtoMapper;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.MatchDetailsDtoMapper;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.SiteServeEventDtoMapper;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.module.KnockoutModuleDtoMapper;
import com.ladbrokescoral.oxygen.bigcompetition.service.CompetitionParticipantService;
import com.ladbrokescoral.oxygen.bigcompetition.service.KnockoutModuleService;
import com.ladbrokescoral.oxygen.bigcompetition.service.SiteServeApiService;
import com.ladbrokescoral.oxygen.bigcompetition.service.StatsCenterApiService;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;

@Service
// @Slf4j
public class KnockoutModuleServiceImpl implements KnockoutModuleService {

  private final StatsCenterApiService statsCenterApiService;
  private final SiteServeApiService siteServeApiService;

  private final CompetitionParticipantService participantService;
  private final MatchDetailsDtoMapper matchDetailsMapper;

  @Autowired
  public KnockoutModuleServiceImpl(
      @Qualifier("statsCenterApiServiceImpl") StatsCenterApiService statsCenterApiService,
      SiteServeApiService siteServeApiService,
      CompetitionParticipantService participantService,
      MatchDetailsDtoMapper matchDetailsMapper) {
    this.statsCenterApiService = statsCenterApiService;
    this.siteServeApiService = siteServeApiService;
    this.participantService = participantService;
    this.matchDetailsMapper = matchDetailsMapper;
  }

  @Override
  public KnockoutModuleDto process(CompetitionModule module) {
    KnockoutModuleDto knockoutModuleDto = KnockoutModuleDtoMapper.INSTANCE.toDto(module);

    CompetitionKnockoutModuleDataDto knockoutModuleData =
        KnockoutModuleDataDtoMapper.INSTANCE.toDto(module.getKnockoutModuleData());

    knockoutModuleDto.setKnockoutRounds(knockoutModuleData.getRounds());

    List<CompetitionKnockoutEventDto> events =
        knockoutModuleData.getEvents().stream()
            .map(this::populateWithOBEvent)
            .map(
                event ->
                    participantService.populateKnockoutEventWithParticipant(
                        event, knockoutModuleDto.getCompetitionUriFromPath()))
            .map(this::populateMatchResult)
            .collect(Collectors.toList());
    setMarketsCountField(events);
    knockoutModuleDto.setKnockoutEvents(events);
    return knockoutModuleDto;
  }

  private CompetitionKnockoutEventDto populateWithOBEvent(CompetitionKnockoutEventDto event) {
    siteServeApiService
        .getEventWithOutcomesForEventKnockout(String.valueOf(event.getEventId()))
        .map(SiteServeEventDtoMapper.INSTANCE::toDto)
        .ifPresent(event::setObEvent);
    return event;
  }

  private CompetitionKnockoutEventDto populateMatchResult(CompetitionKnockoutEventDto event) {
    statsCenterApiService
        .getMatchDetails(String.valueOf(event.getEventId()))
        .ifPresent(
            match -> {
              MatchResultDto dto = matchDetailsMapper.toDto(match);
              if (dto != null) {
                event.setResulted(true);
                event.setResult(dto);
                if (match.getTeamA() != null && Boolean.valueOf(match.getTeamA().getWinner())) {
                  event.getParticipants().get("HOME").setIsWinner(match.getTeamA().getWinner());
                }
                if (match.getTeamB() != null && Boolean.valueOf(match.getTeamB().getWinner())) {
                  event.getParticipants().get("AWAY").setIsWinner(match.getTeamB().getWinner());
                }
              }
            });
    return event;
  }

  private void setMarketsCountField(List<CompetitionKnockoutEventDto> events) {
    Optional<List<Aggregation>> aggregations =
        siteServeApiService.getMarketsCountForEvents(getEventIds(events));

    aggregations.ifPresent(
        agg -> {
          Map<String, Integer> marketCountForEventMap =
              agg.stream()
                  .collect(
                      toMap(item -> String.valueOf(item.getRefRecordId()), Aggregation::getCount));

          events.stream()
              .map(CompetitionKnockoutEventDto::getObEvent)
              .filter(Objects::nonNull)
              .map(obEv -> obEv.setMarketsCount(marketCountForEventMap.get(obEv.getId())))
              .collect(Collectors.toList());
        });
  }

  private List<Integer> getEventIds(List<CompetitionKnockoutEventDto> events) {
    return events.stream()
        .map(CompetitionKnockoutEventDto::getEventId)
        .collect(Collectors.toList());
  }
}
