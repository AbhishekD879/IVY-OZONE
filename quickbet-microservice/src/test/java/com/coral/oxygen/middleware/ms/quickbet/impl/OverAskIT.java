package com.coral.oxygen.middleware.ms.quickbet.impl;

import static com.coral.oxygen.middleware.ms.quickbet.Messages.*;
import static com.coral.oxygen.middleware.ms.quickbet.utils.TestUtils.getResourceByPath;
import static java.util.Arrays.asList;
import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.Mockito.when;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.BetDto;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.RegularPlaceBetResponse;
import com.coral.oxygen.middleware.ms.quickbet.utils.WebSocketTestClient;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;
import com.entain.oxygen.bettingapi.model.bet.api.common.IdRef;
import com.entain.oxygen.bettingapi.model.bet.api.common.LegPart;
import com.entain.oxygen.bettingapi.model.bet.api.common.Stake;
import com.entain.oxygen.bettingapi.model.bet.api.common.YesNo;
import com.entain.oxygen.bettingapi.model.bet.api.request.BetsDto;
import com.entain.oxygen.bettingapi.model.bet.api.response.Bet;
import com.entain.oxygen.bettingapi.model.bet.api.response.BetsResponse;
import com.entain.oxygen.bettingapi.model.bet.api.response.CashoutValue;
import com.entain.oxygen.bettingapi.model.bet.api.response.GeneralResponse;
import com.entain.oxygen.bettingapi.model.bet.api.response.Leg;
import com.entain.oxygen.bettingapi.model.bet.api.response.Payout;
import com.entain.oxygen.bettingapi.model.bet.api.response.Price;
import com.entain.oxygen.bettingapi.model.bet.api.response.SportsLeg;
import com.entain.oxygen.bettingapi.service.BettingService;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit.jupiter.SpringExtension;

@ExtendWith(SpringExtension.class)
@IntegrationTest
public class OverAskIT {

  private static final String OVERASK_SELECTION_REQUEST_JSON = "overaskSelectionRequest.json";
  private static final String OVERASK_PLACE_BET_REQUEST_JSON = "overaskPlaceBetRequest.json";

  @MockBean private SiteServerService siteServerService;

  @MockBean private BettingService bettingService;

  @Autowired private WebSocketTestClient client;

  @Disabled(
      "Temporary exclude of failing tests to make develop green and work on fix for it in the meantime.")
  @Test
  void testOverask_whenAcceptedByTrader() {
    // given
    Bet overaskedBet = createBetWithOverask();
    Bet acceptedBet = acceptByTrader(createBetWithOverask());

    when(siteServerService.getEventToOutcomeForOutcome(any()))
        .thenReturn(Optional.of(createEvents()));
    when(bettingService.placeBet(any(), any(BetsDto.class))).thenReturn(responseFor(overaskedBet));
    when(bettingService.readBet(any(), anyList())).thenReturn(responseFor(acceptedBet));

    // when
    client.emit(OUTCOME_REQUEST_CODE, getResourceByPath(OVERASK_SELECTION_REQUEST_JSON));
    client.wait(REGULAR_OUTCOME_RESPONSE_CODE);
    client.emit(PLACE_BET_REQUEST_CODE, getResourceByPath(OVERASK_PLACE_BET_REQUEST_JSON));

    // then
    Bet bet = client.wait(PLACE_BET_OVERASK_RESPONSE_CODE, BetsResponse.class).getBet().get(0);

    assertThat(bet).isEqualToComparingFieldByFieldRecursively(overaskedBet);

    BetDto betDto =
        client
            .wait(PLACE_BET_RESPONSE_CODE, RegularPlaceBetResponse.class)
            .getData()
            .getReceipt()
            .get(0)
            .getBet();

    assertThat(betDto.getId()).isEqualTo(acceptedBet.getId());
    assertThat(betDto.getIsConfirmed()).isEqualTo(acceptedBet.getIsConfirmed());
    assertThat(betDto.getIsReffered()).isEqualTo(acceptedBet.getIsReferred());
    assertThat(betDto.getCashoutValue()).isEqualTo(acceptedBet.getCashoutValue());
  }

  private Bet createBetWithOverask() {
    Bet bet = createBet();
    bet.setIsReferred(YesNo.Y);
    bet.setIsConfirmed(YesNo.N);
    bet.setConfirmationExpectedAt("5");
    return bet;
  }

  private Bet createBet() {
    Stake stake = new Stake();
    stake.setAmount("5");

    Price price = new Price();
    price.setPriceDen("5");
    price.setPriceNum("10");
    price.setPriceTypeRef(new IdRef());

    LegPart legPart = new LegPart();

    SportsLeg sportsLeg = new SportsLeg();
    sportsLeg.setPrice(price);
    sportsLeg.setLegPart(asList(legPart));

    Leg leg = new Leg();
    leg.setSportsLeg(sportsLeg);

    CashoutValue cashoutValue = new CashoutValue();
    cashoutValue.setAmount("10");

    Payout payout = new Payout();
    payout.setPotential("10");

    Bet bet = new Bet();
    bet.setId(12345678L);
    bet.setCashoutValue(cashoutValue.getAmount());
    bet.setReceipt("10");
    bet.setTimeStamp("1479249799770");
    bet.setPayout(asList(payout));
    bet.setStake(stake);
    bet.setLeg(asList(leg));

    return bet;
  }

  private Bet acceptByTrader(Bet bet) {
    bet.setIsConfirmed(YesNo.Y);
    return bet;
  }

  private List<Event> createEvents() {
    Outcome outcome = new Outcome();
    outcome.setId("549210360");

    Children outcomeChild = new Children();
    outcomeChild.setOutcome(outcome);

    List<Children> outcomeChildren = new LinkedList<>();
    outcomeChildren.add(outcomeChild);

    Market market = new Market();
    market.setId("142");
    market.setChildren(outcomeChildren);
    market.getOutcomes().add(outcome);

    Children marketChild = new Children();
    marketChild.setMarket(market);

    List<Children> marketChildren = new LinkedList<>();
    marketChildren.add(marketChild);

    Event event = new Event();
    event.setId("27417");
    event.setChildren(marketChildren);

    List<Event> events = new ArrayList<>();
    events.add(event);

    return events;
  }

  private GeneralResponse<BetsResponse> responseFor(Bet bet) {
    BetsResponse betsResponse = new BetsResponse();
    betsResponse.setBet(asList(bet));

    return new GeneralResponse<>(betsResponse, null);
  }
}
