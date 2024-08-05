package com.ladbrokescoral.oxygen.bigcompetition.service.impl;

import static com.egalacoral.spark.siteserver.api.SiteServerApi.COMPETITION_OUTCOME_NAME_DELIMITERS;
import static com.ladbrokescoral.oxygen.bigcompetition.util.Utils.buildCompetitionParticipant;

import com.ladbrokescoral.oxygen.bigcompetition.dto.ParticipantDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.knockout.CompetitionKnockoutEventDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.siteServe.EventDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.siteServe.MarketDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.siteServe.OutcomeDto;
import com.ladbrokescoral.oxygen.bigcompetition.service.CmsApiService;
import com.ladbrokescoral.oxygen.bigcompetition.service.CompetitionParticipantService;
import com.ladbrokescoral.oxygen.cms.client.model.Competition;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionParticipant;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
// @Slf4j
public class CompetitionParticipantServiceImpl implements CompetitionParticipantService {

  private final CmsApiService cmsApiService;
  private final String brand;

  public CompetitionParticipantServiceImpl(
      CmsApiService cmsApiService, @Value("${cms.brand}") String brand) {
    this.cmsApiService = cmsApiService;
    this.brand = brand;
  }

  @Override
  public EventDto populateEventWithParticipants(EventDto event, String competitionUri) {
    List<CompetitionParticipant> participants = getParticipantsForModule(competitionUri);
    event.getMarkets().stream()
        .map(MarketDto::getOutcomes)
        .flatMap(List::stream)
        .forEach(outcome -> populateOutcomeWithParticipant(outcome, participants));
    return event;
  }

  private void populateOutcomeWithParticipant(
      OutcomeDto outcome, List<CompetitionParticipant> competitionParticipants) {
    List<String> names =
        Arrays.stream(outcome.getName().replace("|", "").split(COMPETITION_OUTCOME_NAME_DELIMITERS))
            .map(String::trim)
            .collect(Collectors.toList());
    if (names.isEmpty()) {
      return;
    }
    ParticipantDto firstParticipantDto =
        buildCompetitionParticipant(competitionParticipants, names.get(0));
    outcome.getParticipants().put("HOME", firstParticipantDto);
    if (names.size() == 2) {
      ParticipantDto secondParticipantDto =
          buildCompetitionParticipant(competitionParticipants, names.get(1));
      outcome.getParticipants().put("AWAY", secondParticipantDto);
    }
  }

  private List<CompetitionParticipant> getParticipantsForModule(String competitionUri) {
    return cmsApiService
        .findCompetitionByBrandAndUri(brand, competitionUri)
        .map(Competition::getCompetitionParticipants)
        .orElseGet(ArrayList::new);
  }

  @Override
  public CompetitionKnockoutEventDto populateKnockoutEventWithParticipant(
      CompetitionKnockoutEventDto knockoutEventDto, String competitionUri) {
    List<CompetitionParticipant> participants = getParticipantsForModule(competitionUri);
    Optional.ofNullable(knockoutEventDto.getHomeTeam())
        .map(teamName -> buildCompetitionParticipant(participants, teamName))
        .ifPresent(participant -> knockoutEventDto.getParticipants().put("HOME", participant));

    Optional.ofNullable(knockoutEventDto.getAwayTeam())
        .map(teamName -> buildCompetitionParticipant(participants, teamName))
        .ifPresent(participant -> knockoutEventDto.getParticipants().put("AWAY", participant));
    return knockoutEventDto;
  }
}
