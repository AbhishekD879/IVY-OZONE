package com.coral.oxygen.middleware.ms.quickbet.impl;

import static com.coral.oxygen.middleware.ms.quickbet.Messages.BUILD_BET_RESPONSE;

import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.ComplexSelection;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.BetBuildResponse;
import com.coral.oxygen.middleware.ms.quickbet.util.codes.ErrorDetailLevel;
import com.entain.oxygen.bettingapi.model.bet.api.common.YesNo;
import com.entain.oxygen.bettingapi.model.bet.api.request.buildBet.Bet;
import com.entain.oxygen.bettingapi.model.bet.api.request.buildBet.BetBuildDto;
import com.entain.oxygen.bettingapi.model.bet.api.request.buildBet.Leg;
import com.entain.oxygen.bettingapi.model.bet.api.request.buildBet.Outcome;
import com.entain.oxygen.bettingapi.model.bet.api.request.buildBet.OutcomeGroup;
import com.entain.oxygen.bettingapi.model.bet.api.request.buildBet.Part;
import com.entain.oxygen.bettingapi.model.bet.api.response.GeneralResponse;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.BetBuildResponseModel;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.BetFailure;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.BetFailureDetail;
import com.entain.oxygen.bettingapi.service.BettingService;
import io.vavr.collection.HashSet;
import io.vavr.collection.List;
import io.vavr.collection.Set;
import io.vavr.control.Option;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class BuildBetOperations {

  private final BettingService bettingService;
  private final SiteServerService siteServerService;

  public BetBuildResponseModel buildBet(Session session) {
    List<String> regularSelections = session.getSelectedOutcomeIds();
    List<ComplexSelection> complexSelections = session.getComplexSelections();

    BetBuildResponse betBuildResponse = sendBetBuild(regularSelections, complexSelections, session);

    session.setBetBuildResponse(betBuildResponse.getBetBuildResponseModel());
    session.sendData(BUILD_BET_RESPONSE.code(), betBuildResponse);
    session.save();

    return betBuildResponse.getBetBuildResponseModel();
  }

  private BetBuildResponse sendBetBuild(
      List<String> selections, List<ComplexSelection> complexSelections, Session session) {
    if (selections.isEmpty() && complexSelections.isEmpty()) {
      return new BetBuildResponse(new BetBuildResponseModel(), HashSet.empty());
    } else {
      Set<String> allFailedOutcomeIds = HashSet.empty();
      Set<String> latestFailedOutcomeIds;
      GeneralResponse<BetBuildResponseModel> bettingResponse;
      do {
        BetBuildDto buildBetDto = createBetBuildDto(session, selections, complexSelections);
        bettingResponse = bettingService.buildBetV2(session.getToken(), buildBetDto);
        latestFailedOutcomeIds = collectFailedOutcomeIds(bettingResponse);
        allFailedOutcomeIds = allFailedOutcomeIds.addAll(latestFailedOutcomeIds);
        selections = selections.removeAll(latestFailedOutcomeIds);
      } while (!latestFailedOutcomeIds.isEmpty() && !selections.isEmpty());

      return new BetBuildResponse(bettingResponse.getBody(), allFailedOutcomeIds);
    }
  }

  BetBuildDto createBetBuildDto(
      Session session, List<String> selections, List<ComplexSelection> complexSelections) {
    BetBuildDto buildBetDto = new BetBuildDto();

    Set<OutcomeGroup> outcomeGroups = createOutcomeGroups(session, selections);
    buildBetDto.setOutcomeGroup(outcomeGroups.toJavaSet());
    buildBetDto.setBet(
        createBetsForComplexSelections(complexSelections, outcomeGroups.size() + 1).toJavaSet());

    buildBetDto.setErrorDetail(ErrorDetailLevel.ALL.getCode());
    buildBetDto.setChannel("M");
    buildBetDto.setReturnOutcomeDetails(YesNo.Y.name());
    buildBetDto.setReturnOffers(YesNo.Y.name());

    if (session.getToken() != null) {
      buildBetDto.setReturnFreebetTokens(YesNo.Y.name());
    } else {
      buildBetDto.setAnonBet(YesNo.Y.name());
    }

    return buildBetDto;
  }

  private Set<Bet> createBetsForComplexSelections(
      List<ComplexSelection> complexSelections, Integer startingBetNo) {
    return complexSelections
        .zipWithIndex(
            (selection, index) -> {
              Bet bet = new Bet();
              bet.setBetNo(String.valueOf(startingBetNo + index));
              Leg leg = new Leg();
              leg.setLegNo("1");
              leg.setLegSort(selection.getType().getLegSortCode());
              List<Part> legParts = selection.getOutcomeIds().map(Part::new);
              leg.setPart(legParts.toJavaList());
              bet.getLeg().add(leg);
              return bet;
            })
        .toSet();
  }

  private Set<OutcomeGroup> createOutcomeGroups(Session session, List<String> selections) {
    Set<OutcomeGroup> outcomeGroups = createOutcomesWithSingleSelection(session, selections);
    if (selections.size() > 1) {
      return outcomeGroups.add(createOutcomeGroupWithAllSelections(session, selections));
    } else {
      return outcomeGroups;
    }
  }

  private Set<OutcomeGroup> createOutcomesWithSingleSelection(
      Session session, List<String> selections) {
    return selections
        .zipWithIndex(
            (outcomeId, index) -> {
              OutcomeGroup outcomeGroup = new OutcomeGroup();
              outcomeGroup.setBetNo(String.valueOf(index + 1));
              Outcome outcome = new Outcome();
              outcome.setValue(outcomeId);
              outcome.setPriceStream(
                  session.getRegularSelectionResponse().getSelectionPrice().getPriceStreamType());
              outcomeGroup.getOutcome().add(outcome);
              return outcomeGroup;
            })
        .toSet();
  }

  private OutcomeGroup createOutcomeGroupWithAllSelections(
      Session session, List<String> selections) {
    OutcomeGroup allOutcomes = new OutcomeGroup();
    allOutcomes.setBetNo(String.valueOf(selections.length() + 1));
    List<Outcome> outcomes = List.empty();
    selections.forEach(
        (String selection) -> {
          Outcome outcome = new Outcome();
          outcome.setValue(selection);
          outcome.setPriceStream(
              session.getRegularSelectionResponse().getSelectionPrice().getPriceStreamType());
          outcomes.append(outcome);
        });
    allOutcomes.getOutcome().addAll(outcomes.asJava());
    return allOutcomes;
  }

  private Set<String> collectFailedOutcomeIds(
      GeneralResponse<BetBuildResponseModel> betBuildResponse) {

    return List.ofAll(betBuildResponse.getBody().getBetFailure())
        .flatMap(BetFailure::getBetError)
        .flatMap(error -> Option.of(error.getBetFailureDetail()))
        .map(BetFailureDetail::getOutcomeId)
        .toSet();
  }
}
