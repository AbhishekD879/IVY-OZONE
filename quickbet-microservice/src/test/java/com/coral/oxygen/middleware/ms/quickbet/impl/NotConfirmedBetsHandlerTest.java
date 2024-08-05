package com.coral.oxygen.middleware.ms.quickbet.impl;

import static com.coral.oxygen.middleware.ms.quickbet.Messages.PLACE_BET_ERROR_RESPONSE_CODE;
import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.tuple;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;

import com.coral.oxygen.middleware.ms.quickbet.Messages;
import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.connector.ErrorMessageFactory;
import com.coral.oxygen.middleware.ms.quickbet.connector.OveraskReadBetExecutionService;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.BirResponse;
import com.coral.oxygen.middleware.ms.quickbet.converter.MultiReadBetResponseAdapter;
import com.coral.oxygen.middleware.ms.quickbet.converter.PlaceBetResponseAdapter;
import com.coral.oxygen.middleware.ms.quickbet.util.BetUtils;
import com.entain.oxygen.bettingapi.model.bet.api.common.YesNo;
import com.entain.oxygen.bettingapi.model.bet.api.request.BetRef;
import com.entain.oxygen.bettingapi.model.bet.api.response.Bet;
import com.entain.oxygen.bettingapi.model.bet.api.response.BetsResponse;
import io.vavr.collection.List;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import org.apache.commons.lang3.RandomUtils;
import org.assertj.core.groups.Tuple;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;

class NotConfirmedBetsHandlerTest {
  private Session session;
  private OveraskReadBetExecutionService readBetExecutionService;
  private NotConfirmedBetsHandler handler;

  @BeforeEach
  void setUp() {
    session = mock(Session.class);
    readBetExecutionService = mock(OveraskReadBetExecutionService.class);
    handler = new NotConfirmedBetsHandler(readBetExecutionService);
  }

  @Test
  void testOverask() {
    MultiReadBetResponseAdapter betsResponse = overaskResponse();
    handler.handle(session, betsResponse, "123");

    verifyMessageWasSent(
        Messages.PLACE_BET_OVERASK_RESPONSE_CODE.code(), betsResponse.getResponse());
  }

  @Test
  void testBetInRun() {
    MultiReadBetResponseAdapter response = betInRunResponse();
    handler.handle(session, response, "123");

    verify(session)
        .sendData(
            Messages.PLACE_BET_BIR.code(), new BirResponse("10", BetUtils.OPEN_BET_BIR_PROVIDER));
    ArgumentCaptor<List<BetRef>> captor = ArgumentCaptor.forClass(List.class);
    verify(readBetExecutionService)
        .scheduleReadBet(
            eq(session), captor.capture(), eq("123"), eq(response.getConfirmationExpectedAt()));

    List<Tuple> expected =
        response.getBetsToRead().map(betRef -> tuple(betRef.getId(), betRef.getProvider()));
    assertThat(captor.getValue())
        .extracting(BetRef::getId, BetRef::getProvider)
        .containsExactlyInAnyOrderElementsOf(expected);
  }

  @Test
  void testBetInRunWithOtherProvider() {
    MultiReadBetResponseAdapter response = betInRunResponseWithOtherProvider();
    handler.handle(session, response, "123");

    verify(session)
        .sendData(
            PLACE_BET_ERROR_RESPONSE_CODE.code(),
            ErrorMessageFactory.internalError(
                "Bet isn't confirmed, but isn't an overask nor bet in run"));

    assertThat(response.getProvider()).isNotNull();
  }

  @Test
  @DisplayName("should send error message to the socket when neither BiR nor Overask")
  void testError() {
    // given
    String token = "token";
    PlaceBetResponseAdapter response = mock(PlaceBetResponseAdapter.class);
    when(response.isBetInRun()).thenReturn(false);
    when(response.isOverask()).thenReturn(false);

    // when
    handler.handle(session, response, token);

    // then
    verify(session).sendData(eq(PLACE_BET_ERROR_RESPONSE_CODE.code()), any());
  }

  @Test
  void testAllFinished() {
    MultiReadBetResponseAdapter response = allFinishedResponse();
    handler.handle(session, response, "123");

    boolean result = response.allFinished();
    assertThat(result).isTrue();
  }

  @Test
  void testGetIds() {
    MultiReadBetResponseAdapter response = getIdsResponse();

    List<Long> ids = response.getIds();
    assertThat(ids).containsExactlyInAnyOrder(1L, 2L);
  }

  private MultiReadBetResponseAdapter allFinishedResponse() {
    BetsResponse betsResponse = new BetsResponse();
    Bet bet1 = new Bet();
    bet1.setId(1L);
    bet1.setIsConfirmed(YesNo.Y);
    bet1.setIsReferred(YesNo.N);

    betsResponse.setBet(Collections.singletonList(bet1));
    return new MultiReadBetResponseAdapter(betsResponse);
  }

  private MultiReadBetResponseAdapter getIdsResponse() {
    BetsResponse betsResponse = new BetsResponse();
    Bet bet1 = new Bet();
    bet1.setId(1L);

    Bet bet2 = new Bet();
    bet2.setId(2L);

    betsResponse.setBet(new ArrayList<>(Arrays.asList(bet1, bet2)));
    return new MultiReadBetResponseAdapter(betsResponse);
  }

  private MultiReadBetResponseAdapter overaskResponse() {
    BetsResponse betsResponse = new BetsResponse();
    Bet bet = new Bet();
    bet.setId(RandomUtils.nextLong());
    bet.setIsConfirmed(YesNo.N);
    bet.setIsReferred(YesNo.Y);
    betsResponse.setBet(Collections.singletonList(bet));
    return new MultiReadBetResponseAdapter(betsResponse);
  }

  private MultiReadBetResponseAdapter betInRunResponse() {
    BetsResponse response = new BetsResponse();
    Bet bet = new Bet();
    bet.setId(RandomUtils.nextLong());
    bet.setIsConfirmed(YesNo.N);
    bet.setConfirmationExpectedAt("10");
    bet.setProvider(BetUtils.OPEN_BET_BIR_PROVIDER);
    response.setBet(Collections.singletonList(bet));
    return new MultiReadBetResponseAdapter(response);
  }

  private MultiReadBetResponseAdapter betInRunResponseWithOtherProvider() {
    BetsResponse response = new BetsResponse();
    Bet bet = new Bet();
    bet.setId(RandomUtils.nextLong());
    bet.setIsConfirmed(YesNo.N);
    bet.setConfirmationExpectedAt("10");
    response.setBet(Collections.singletonList(bet));
    return new MultiReadBetResponseAdapter(response);
  }

  private void verifyMessageWasSent(String message, Object data) {
    verify(session).sendData(message, data);
  }
}
