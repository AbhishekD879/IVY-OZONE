package com.ladbrokescoral.cashout.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.when;

import com.coral.bpp.api.model.bet.api.request.AccountHistoryRequest;
import com.coral.bpp.api.model.bet.api.response.accountHistory.Paging;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.ExternalStatsLink;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.Leg;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.Outcome;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.Part;
import com.ladbrokescoral.cashout.model.response.InitialAccountHistoryBetResponse;
import java.util.Collections;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

@ExtendWith(MockitoExtension.class)
class BetDetailsServiceTest {

  @Mock private BppService bppServiceMock;

  private AccountHistoryService accountHistoryService;
  private AccountHistoryRequest accountHistoryRequest;

  @BeforeEach
  public void setUp() {
    accountHistoryService = new AccountHistoryServiceImpl(bppServiceMock, 20);
    accountHistoryRequest = AccountHistoryRequest.builder().build();
  }

  @Test
  void testGetBetDetails() {

    BetSummaryModel bet = new BetSummaryModel();
    bet.setId("12");
    InitialAccountHistoryBetResponse initialAccHistoryResp =
        new InitialAccountHistoryBetResponse(
            Collections.singletonList(bet), null, null, new Paging(), "OMNATGXMLEDPQ9878798", "1");
    when(bppServiceMock.accountHistory(accountHistoryRequest))
        .thenReturn(Mono.just(initialAccHistoryResp));

    Mono<InitialAccountHistoryBetResponse> result =
        accountHistoryService.accountHistoryInitBets(accountHistoryRequest);

    StepVerifier.create(result)
        .assertNext(
            bets -> {
              assertEquals(1, bets.getBets().size());
              assertEquals("12", bets.getBets().get(0).getId());
            })
        .expectComplete()
        .verify();
  }

  @Test
  void testAccountHistoryExternalData() {

    BetSummaryModel bet = new BetSummaryModel();
    bet.setId("123");
    Leg leg = new Leg();
    Part part = new Part();
    Outcome outcome = new Outcome();

    ExternalStatsLink externalStatsLink = new ExternalStatsLink();
    externalStatsLink.setContestantId("47");
    externalStatsLink.setPlayerId("3434");
    externalStatsLink.setStatCategory("16");
    externalStatsLink.setStatValue("abc");

    outcome.setExternalStatsLink(externalStatsLink);
    part.setOutcome(Collections.singletonList(outcome));
    leg.setPart(Collections.singletonList(part));
    bet.setLeg(Collections.singletonList(leg));

    Paging paging = new Paging();
    paging.setBlockSize("20");
    paging.setToken("BJUN23MNC56DTR888DY");

    InitialAccountHistoryBetResponse initialAccHistoryResp =
        new InitialAccountHistoryBetResponse(
            Collections.singletonList(bet), null, null, paging, "OMNATGXMLEDPQ9878798", "1");

    when(bppServiceMock.accountHistory(accountHistoryRequest))
        .thenReturn(Mono.just(initialAccHistoryResp));

    Mono<InitialAccountHistoryBetResponse> result =
        accountHistoryService.accountHistoryInitBets(accountHistoryRequest);

    StepVerifier.create(result)
        .assertNext(
            bets -> {
              assertEquals(1, bets.getBets().size());
              assertEquals("123", bets.getBets().get(0).getId());
              assertEquals(
                  "47",
                  bets.getBets()
                      .get(0)
                      .getLeg()
                      .get(0)
                      .getPart()
                      .get(0)
                      .getOutcome()
                      .get(0)
                      .getExternalStatsLink()
                      .getContestantId());
              assertEquals(
                  "3434",
                  bets.getBets()
                      .get(0)
                      .getLeg()
                      .get(0)
                      .getPart()
                      .get(0)
                      .getOutcome()
                      .get(0)
                      .getExternalStatsLink()
                      .getPlayerId());
              assertEquals(
                  "16",
                  bets.getBets()
                      .get(0)
                      .getLeg()
                      .get(0)
                      .getPart()
                      .get(0)
                      .getOutcome()
                      .get(0)
                      .getExternalStatsLink()
                      .getStatCategory());
              assertEquals(
                  "abc",
                  bets.getBets()
                      .get(0)
                      .getLeg()
                      .get(0)
                      .getPart()
                      .get(0)
                      .getOutcome()
                      .get(0)
                      .getExternalStatsLink()
                      .getStatValue());
            })
        .expectComplete()
        .verify();
  }
}
