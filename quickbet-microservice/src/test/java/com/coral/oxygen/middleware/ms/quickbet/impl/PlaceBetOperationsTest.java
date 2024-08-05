package com.coral.oxygen.middleware.ms.quickbet.impl;

import static com.coral.oxygen.middleware.ms.quickbet.Messages.PLACE_BET_ERROR_RESPONSE_CODE;
import static com.coral.oxygen.middleware.ms.quickbet.Messages.PLACE_BET_RESPONSE_CODE;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;

import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.UIPlaceBetRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3.UIBet;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3.UILeg;
import com.coral.oxygen.middleware.ms.quickbet.converter.MultiPlaceBetResponseAdapter;
import com.coral.oxygen.middleware.ms.quickbet.converter.MultiPlaceBetResponseAdapterFactory;
import com.coral.oxygen.middleware.ms.quickbet.converter.PlaceBetRequestConverter;
import com.entain.oxygen.bettingapi.model.bet.api.request.placeBetV2.PlaceBetDto;
import com.entain.oxygen.bettingapi.model.bet.api.response.ErrorBody;
import com.entain.oxygen.bettingapi.model.bet.api.response.GeneralResponse;
import com.entain.oxygen.bettingapi.model.bet.api.response.placeBetV2.RespBetPlace;
import com.entain.oxygen.bettingapi.service.BettingService;
import io.vavr.collection.List;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class PlaceBetOperationsTest {

  private static final String TOKEN = "token";

  @Mock private PlaceBetRequestConverter placeBetRequestConverter;
  @Mock private BettingService bettingService;
  @Mock private NotConfirmedBetsHandler notConfirmedBetsHandler;
  @Mock private MultiPlaceBetResponseAdapterFactory multiPlaceBetResponseAdapterFactory;

  @InjectMocks private PlaceBetOperations placeBetOperations;

  @Test
  void shouldPlaceBetSuccessfully() {
    // given
    Session session = mockSession();
    UIPlaceBetRequest request = defaultRequest();
    PlaceBetDto placeBetDto = PlaceBetDto.builder().build();
    when(placeBetRequestConverter.convert(eq(session), eq(request))).thenReturn(placeBetDto);
    GeneralResponse<RespBetPlace> response = mock(GeneralResponse.class);
    RespBetPlace responseBody = mock(RespBetPlace.class);
    when(response.getBody()).thenReturn(responseBody);
    when(bettingService.placeBetV2(eq(TOKEN), eq(placeBetDto))).thenReturn(response);

    MultiPlaceBetResponseAdapter adapter = mock(MultiPlaceBetResponseAdapter.class);
    when(adapter.allFinished()).thenReturn(true);
    when(multiPlaceBetResponseAdapterFactory.from(responseBody)).thenReturn(adapter);

    // when
    placeBetOperations.placeBet(session, request);

    // then
    verify(session).sendData(PLACE_BET_RESPONSE_CODE.code(), responseBody);
  }

  @Test
  void shouldHandleNotConfirmedBets() {
    // given
    Session session = mockSession();
    UIPlaceBetRequest request = defaultRequest();
    PlaceBetDto placeBetDto = PlaceBetDto.builder().build();
    when(placeBetRequestConverter.convert(eq(session), eq(request))).thenReturn(placeBetDto);
    GeneralResponse<RespBetPlace> response = mock(GeneralResponse.class);
    RespBetPlace responseBody = mock(RespBetPlace.class);
    when(response.getBody()).thenReturn(responseBody);
    when(bettingService.placeBetV2(eq(TOKEN), eq(placeBetDto))).thenReturn(response);

    MultiPlaceBetResponseAdapter adapter = mock(MultiPlaceBetResponseAdapter.class);
    when(adapter.allFinished()).thenReturn(false);
    when(multiPlaceBetResponseAdapterFactory.from(responseBody)).thenReturn(adapter);

    // when
    placeBetOperations.placeBet(session, request);

    // then
    verify(notConfirmedBetsHandler).handle(eq(session), any(), eq(TOKEN));
  }

  @Test
  void shouldHandleErrorsIfErrorBodyPresent() {
    // given
    Session session = mockSession();
    UIPlaceBetRequest request = defaultRequest();
    PlaceBetDto placeBetDto = PlaceBetDto.builder().build();
    when(placeBetRequestConverter.convert(eq(session), eq(request))).thenReturn(placeBetDto);
    GeneralResponse<RespBetPlace> response = mock(GeneralResponse.class);
    ErrorBody errorBody = mock(ErrorBody.class);
    when(response.getErrorBody()).thenReturn(errorBody);
    when(bettingService.placeBetV2(eq(TOKEN), eq(placeBetDto))).thenReturn(response);

    // when
    placeBetOperations.placeBet(session, request);

    // then
    verify(session).sendData(PLACE_BET_ERROR_RESPONSE_CODE.code(), errorBody);
  }

  @Test
  void shouldHandleErrorsIfNoErrorBodyAndNoRegularBody() {
    // given
    Session session = mockSession();
    UIPlaceBetRequest request = defaultRequest();
    PlaceBetDto placeBetDto = PlaceBetDto.builder().build();
    when(placeBetRequestConverter.convert(eq(session), eq(request))).thenReturn(placeBetDto);
    GeneralResponse<RespBetPlace> response = mock(GeneralResponse.class);
    when(bettingService.placeBetV2(eq(TOKEN), eq(placeBetDto))).thenReturn(response);

    // when
    placeBetOperations.placeBet(session, request);

    // then
    verify(session).sendData(PLACE_BET_ERROR_RESPONSE_CODE.code(), null);
  }

  private UIPlaceBetRequest defaultRequest() {
    UILeg leg =
        UILeg.builder().priceNum(1).priceDen(1).outcomeIds(List.of("1234")).priceType("L").build();
    UIBet bet =
        UIBet.builder()
            .betNo("1")
            .winType("WIN")
            .stakePerLine("1.00")
            .betType("SGL")
            .legs(List.of(leg))
            .build();
    return new UIPlaceBetRequest("channel", "userAgent", "GBP", List.of(bet));
  }

  private Session mockSession() {
    Session session = mock(Session.class);
    when(session.getToken()).thenReturn(TOKEN);
    return session;
  }
}
