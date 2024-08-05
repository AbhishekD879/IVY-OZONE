package com.coral.oxygen.middleware.ms.quickbet.impl;

import static com.coral.oxygen.middleware.ms.quickbet.utils.BetBuildUtils.outcomeToEvent;
import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.when;

import com.coral.oxygen.middleware.ms.quickbet.Messages;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.UIPlaceBetRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3.AddSelectionRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3.UIBet;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3.UILeg;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.BetBuildResponse;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.RegularPlaceBetResponse;
import com.coral.oxygen.middleware.ms.quickbet.utils.WebSocketTestClient;
import com.entain.oxygen.bettingapi.model.bet.api.common.IdRef;
import com.entain.oxygen.bettingapi.model.bet.api.common.LegPart;
import com.entain.oxygen.bettingapi.model.bet.api.common.Stake;
import com.entain.oxygen.bettingapi.model.bet.api.common.YesNo;
import com.entain.oxygen.bettingapi.model.bet.api.common.placeBetV2.BetId;
import com.entain.oxygen.bettingapi.model.bet.api.response.*;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.BetBuild;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.BetBuildResponseModel;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.BetCombination;
import com.entain.oxygen.bettingapi.model.bet.api.response.placeBetV2.BetDelay;
import com.entain.oxygen.bettingapi.model.bet.api.response.placeBetV2.BetPlacement;
import com.entain.oxygen.bettingapi.model.bet.api.response.placeBetV2.RespBetPlace;
import com.entain.oxygen.bettingapi.model.bet.api.response.placeBetV2.RespStatus;
import com.entain.oxygen.bettingapi.service.BettingService;
import io.vavr.collection.List;
import java.util.Collections;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit.jupiter.SpringExtension;

@ExtendWith(SpringExtension.class)
@IntegrationTest
class DelayedMultiBetsIT {

  private static final String TOKEN =
      "053f166a31c499d95d6ef2062d3ac1c92aa119981e2e694550378e8de5850e83";
  private static final String OUTCOME_ID = "553375164";

  @Autowired private WebSocketTestClient client;

  @MockBean private BettingService bettingService;
  @MockBean private SiteServerService siteServerService;

  @BeforeEach
  void setUp() {
    client.login(TOKEN);
    when(bettingService.readBet(anyString(), anyList())).thenReturn(createBetReadResponse());
    when(bettingService.buildBetV2(any(), any())).thenReturn(createBetBuild());
    when(siteServerService.getEventsForOutcomeIds(List.of(OUTCOME_ID)))
        .thenReturn(outcomeToEvent(OUTCOME_ID));
    client.emitWithWaitForResponse(
        Messages.CLEAR_SELECTION_REQUEST_CODE,
        "{}",
        Messages.CLEAR_SELECTION_RESPONSE_CODE,
        Void.class);
  }

  @Test
  void shouldConfirmBir() {
    // GIVEN
    when(bettingService.placeBetV2(any(), any())).thenReturn(createBetPlaceBirResponse());

    AddSelectionRequest request = new AddSelectionRequest(OUTCOME_ID);
    client.emitWithWaitForResponse(
        Messages.ADD_SELECTION, request, Messages.BUILD_BET_RESPONSE, BetBuildResponse.class);

    UIPlaceBetRequest uiPlaceBetRequest =
        new UIPlaceBetRequest("I", "S|H|O0000000", "GBP", buildBet(createLegs(OUTCOME_ID, 1, 25)));

    // WHEN
    RegularPlaceBetResponse response =
        client.emitWithWaitForResponse(
            Messages.PLACE_BET,
            uiPlaceBetRequest,
            Messages.PLACE_BET_RESPONSE_CODE,
            RegularPlaceBetResponse.class);

    // THEN
    assertThat(response.getData().getReceipt().get(0).getBet().getIsConfirmed()).isEqualTo(YesNo.Y);
  }

  private GeneralResponse<BetsResponse> createBetReadResponse() {
    BetsResponse response = new BetsResponse();
    Bet bet = new Bet();
    bet.setStake(new Stake());
    bet.setIsConfirmed(YesNo.Y);
    bet.setPayout(Collections.singletonList(new Payout()));
    String cashoutValue = new String();
    bet.setCashoutValue(cashoutValue);

    Leg leg = new Leg();
    SportsLeg sportsLeg = new SportsLeg();
    Price price = new Price();
    price.setPriceTypeRef(new IdRef());

    sportsLeg.setPrice(price);

    LegPart legPart = new LegPart();
    sportsLeg.setLegPart(Collections.singletonList(legPart));
    leg.setSportsLeg(sportsLeg);
    bet.setLeg(Collections.singletonList(leg));

    response.setBet(Collections.singletonList(bet));
    return new GeneralResponse<>(response, null);
  }

  private GeneralResponse<RespBetPlace> createBetPlaceBirResponse() {
    RespBetPlace response = new RespBetPlace();
    BetDelay betDelay = new BetDelay();
    betDelay.setDelay("2");

    response.getBetDelay().add(betDelay);
    return new GeneralResponse<>(response, null);
  }

  private GeneralResponse<BetBuildResponseModel> createBetBuild() {
    BetBuildResponseModel response = new BetBuildResponseModel();
    response.getBetBuild().add(createBet());
    return new GeneralResponse<>(response, null);
  }

  private BetBuild createBet() {
    BetBuild betBuild = new BetBuild();
    betBuild.setBetNo("1");
    BetCombination betCombination = new BetCombination();
    betCombination.setBetType("SGL");
    betCombination.setBetNoOfLines("1");

    betBuild.getBetCombination().add(betCombination);

    return betBuild;
  }

  @Test
  void shouldReadBetWhenItsOverask() {
    // GIVEN
    when(bettingService.placeBetV2(any(), any())).thenReturn(createBetPlaceOveraskResponse());

    AddSelectionRequest request = new AddSelectionRequest(OUTCOME_ID);
    client.emitWithWaitForResponse(
        Messages.ADD_SELECTION, request, Messages.BUILD_BET_RESPONSE, BetBuildResponse.class);

    UIPlaceBetRequest uiPlaceBetRequest =
        new UIPlaceBetRequest("I", "S|H|O0000000", "GBP", buildBet(createLegs(OUTCOME_ID, 1, 1)));

    // WHEN
    RegularPlaceBetResponse response =
        client.emitWithWaitForResponse(
            Messages.PLACE_BET,
            uiPlaceBetRequest,
            Messages.PLACE_BET_RESPONSE_CODE,
            RegularPlaceBetResponse.class);

    // THEN
    assertThat(response.getData().getReceipt().get(0).getBet().getIsConfirmed()).isEqualTo(YesNo.Y);
  }

  private GeneralResponse<RespBetPlace> createBetPlaceOveraskResponse() {
    RespBetPlace response = new RespBetPlace();
    BetPlacement betPlacement = new BetPlacement();

    com.entain.oxygen.bettingapi.model.bet.api.response.placeBetV2.Bet bet =
        new com.entain.oxygen.bettingapi.model.bet.api.response.placeBetV2.Bet();
    bet.setStatus(RespStatus.P);
    bet.setBetId(new BetId());

    betPlacement.setBet(bet);

    response.getBetPlacement().add(betPlacement);
    return new GeneralResponse<>(response, null);
  }

  @Test
  void shouldReturnErrorWhenBppReturnsError() {
    // GIVEN
    ErrorBody error = new ErrorBody();
    error.setCode("code");
    error.setError("error");

    GeneralResponse<RespBetPlace> errorResponse = new GeneralResponse<>(null, error);
    when(bettingService.placeBetV2(any(), any())).thenReturn(errorResponse);

    AddSelectionRequest request = new AddSelectionRequest(OUTCOME_ID);
    client.emitWithWaitForResponse(
        Messages.ADD_SELECTION, request, Messages.BUILD_BET_RESPONSE, BetBuildResponse.class);

    UIPlaceBetRequest uiPlaceBetRequest =
        new UIPlaceBetRequest("I", "S|H|O0000000", "GBP", buildBet(createLegs(OUTCOME_ID, 1, 25)));

    // WHEN
    ErrorBody response =
        client.emitWithWaitForResponse(
            Messages.PLACE_BET,
            uiPlaceBetRequest,
            Messages.PLACE_BET_ERROR_RESPONSE_CODE,
            ErrorBody.class);

    // THEN
    assertThat(response).isEqualToComparingFieldByField(error);
  }

  private List<UIBet> buildBet(UILeg... legs) {
    return List.of(legs)
        .zipWithIndex(
            (leg, i) ->
                UIBet.builder()
                    .betNo(String.valueOf(i + 1))
                    .winType("W")
                    .stakePerLine("6")
                    .betType("SGL")
                    .legs(List.of(legs[i]))
                    .build());
  }

  private UILeg createLegs(String outcomeId, int priceNum, int priceDen) {
    return UILeg.builder()
        .priceNum(priceNum)
        .priceDen(priceDen)
        .outcomeIds(io.vavr.collection.List.of(outcomeId))
        .priceType("L")
        .build();
  }
}
