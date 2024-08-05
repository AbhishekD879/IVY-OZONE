package com.coral.oxygen.middleware.ms.quickbet.connector;

import static com.coral.oxygen.middleware.ms.quickbet.Messages.*;
import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatCode;
import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.Mockito.*;

import com.coral.oxygen.middleware.ms.quickbet.Messages;
import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.configuration.OveraskReadBetConfiguration;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.ReceiptResponseDto;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.RegularPlaceBetResponse;
import com.coral.oxygen.middleware.ms.quickbet.converter.BetToReceiptResponseDtoConverter;
import com.coral.oxygen.middleware.ms.quickbet.converter.MultiReadBetResponseAdapter;
import com.coral.oxygen.middleware.ms.quickbet.converter.MultiReadBetResponseAdapterFactory;
import com.coral.oxygen.middleware.ms.quickbet.converter.PlaceBetResponseAdapter;
import com.coral.oxygen.middleware.ms.quickbet.impl.SelectionOperations;
import com.coral.oxygen.middleware.ms.quickbet.utils.TestUtils;
import com.entain.oxygen.bettingapi.model.bet.api.request.BetRef;
import com.entain.oxygen.bettingapi.model.bet.api.response.Bet;
import com.entain.oxygen.bettingapi.model.bet.api.response.BetsResponse;
import com.entain.oxygen.bettingapi.model.bet.api.response.ErrorBody;
import com.entain.oxygen.bettingapi.model.bet.api.response.GeneralResponse;
import com.entain.oxygen.bettingapi.service.BettingService;
import io.vavr.collection.List;
import java.util.Collection;
import java.util.Collections;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class OveraskReadBetTaskTest {

  @Mock private OveraskReadBetConfiguration overaskReadBetConfiguration;
  @Mock private BettingService bettingService;
  @Mock private SelectionOperations selectionOperations;
  @Mock private Session session;
  @Mock private BetToReceiptResponseDtoConverter betToReceiptConverter;
  @Mock private PlaceBetResponseAdapter placeBetResponseAdapter;
  @Mock private MultiReadBetResponseAdapterFactory multiReadBetResponseAdapterFactory;

  @InjectMocks private OveraskReadBetTask overaskReadBetTask;

  @BeforeEach
  void setUp() {
    when(placeBetResponseAdapter.getBetsToRead()).thenReturn(List.of(mock(BetRef.class)));
    when(overaskReadBetConfiguration.getMaxNumberOfRetries()).thenReturn(1);
    overaskReadBetTask =
        new OveraskReadBetTask(
            session,
            placeBetResponseAdapter.getBetsToRead(),
            new BetReader("123", bettingService),
            overaskReadBetConfiguration,
            multiReadBetResponseAdapterFactory,
            new OveraskResponseFactory(session, selectionOperations, betToReceiptConverter));
  }

  @Test
  void testOutcomeSuspendedDuringBir() {
    when(bettingService.readBet(any(), anyList()))
        .thenReturn(responseFromFile("outcomeSuspendedBirResponse.json"));

    overaskReadBetTask.run();

    RegularPlaceBetResponse response =
        RegularPlaceBetResponse.errorResponse(
            "EVENT_ERROR", "outcome is suspended", "OUTCOME_SUSPENDED", null, null, null);
    verifyMessageWasSent(Messages.PLACE_BET_ERROR_RESPONSE_CODE.code(), response);
  }

  @Test
  void testBirConfirmed() {
    GeneralResponse<BetsResponse> response = responseFromFile("birResponse.json");
    when(bettingService.readBet(any(), anyList())).thenReturn(response);

    MultiReadBetResponseAdapter adapter = mock(MultiReadBetResponseAdapter.class);
    when(adapter.allFinished()).thenReturn(true);
    when(multiReadBetResponseAdapterFactory.from(any())).thenReturn(adapter);

    overaskReadBetTask.run();

    RegularPlaceBetResponse.Data data = new RegularPlaceBetResponse.Data();
    Collection<ReceiptResponseDto> dtoList =
        betToReceiptConverter.convert(response.getBody().getBet());
    data.getReceipt().addAll(dtoList);

    verifyMessageWasSent(
        Messages.PLACE_BET_RESPONSE_CODE.code(), new RegularPlaceBetResponse(data));
  }

  @Test
  void shouldInformListenerWhenTaskIsCompleted() {
    // WHEN
    overaskReadBetTask.run();

    // THEN
    verify(session).finishTask(overaskReadBetTask.getTaskId());
  }

  @Test
  void shouldNotFailWhenNoListenerIsSet() {
    assertThatCode(() -> overaskReadBetTask.run()).doesNotThrowAnyException();
  }

  @Test
  @DisplayName("should send error message when max number of retries is passed")
  void retryLimitAchieved() {
    // given
    BetsResponse betsResponse = new BetsResponse();
    betsResponse.setBet(Collections.emptyList());
    GeneralResponse<BetsResponse> readBetResponse = new GeneralResponse<>(betsResponse, null);
    when(bettingService.readBet(any(), anyList())).thenReturn(readBetResponse);

    MultiReadBetResponseAdapter adapter = mock(MultiReadBetResponseAdapter.class);
    when(adapter.allFinished()).thenReturn(false);
    when(multiReadBetResponseAdapterFactory.from(any())).thenReturn(adapter);

    // when
    overaskReadBetTask.run();
    verify(session, never()).sendData(any(), any());

    overaskReadBetTask.run();

    // then
    ArgumentCaptor<RegularPlaceBetResponse> captor =
        ArgumentCaptor.forClass(RegularPlaceBetResponse.class);
    verify(session).sendData(eq(PLACE_BET_ERROR_RESPONSE_CODE.code()), captor.capture());

    RegularPlaceBetResponse response = captor.getValue();
    RegularPlaceBetResponse.Error error = response.getData().getError();
    assertThat(error.getCode()).isEqualTo(OVERASK_TIMEOUT_ERROR.code());
  }

  @Test
  @DisplayName("should send error response if errorBody present in readBet response")
  void errorBodyPresent() {
    // given
    ErrorBody errorBody = new ErrorBody();
    errorBody.setStatus("ERROR_STATUS");
    errorBody.setError("ERROR_MESSAGE");
    GeneralResponse<BetsResponse> readBetResponse = new GeneralResponse<>(null, errorBody);
    when(bettingService.readBet(any(), anyList())).thenReturn(readBetResponse);

    // when
    overaskReadBetTask.run();

    // then
    ArgumentCaptor<RegularPlaceBetResponse> captor =
        ArgumentCaptor.forClass(RegularPlaceBetResponse.class);
    verify(session).sendData(eq(PLACE_BET_ERROR_RESPONSE_CODE.code()), captor.capture());
    RegularPlaceBetResponse.Error error = captor.getValue().getData().getError();
    assertThat(error.getCode()).isEqualTo("ERROR_STATUS");
    assertThat(error.getDescription()).isEqualTo("ERROR_MESSAGE");
  }

  @Test
  @DisplayName("should send splitted response code")
  void splittedResponse() {
    // given
    BetsResponse betsResponse = new BetsResponse();
    Bet bet1 = mock(Bet.class);
    Bet bet2 = mock(Bet.class);
    Bet bet3 = mock(Bet.class);
    betsResponse.setBet(List.of(bet1, bet2, bet3).asJava());
    GeneralResponse<BetsResponse> readBetResponse = new GeneralResponse<>(betsResponse, null);
    when(bettingService.readBet(any(), anyList())).thenReturn(readBetResponse);

    // when
    overaskReadBetTask.run();

    // then
    ArgumentCaptor<RegularPlaceBetResponse> captor =
        ArgumentCaptor.forClass(RegularPlaceBetResponse.class);
    verify(session).sendData(eq(PLACE_BET_OVERASK_SPLITTED_RESPONSE_CODE.code()), captor.capture());
    RegularPlaceBetResponse response = captor.getValue();
    assertThat(response.getData().getError()).isNull();
    assertThat(response.getData().getReceipt()).isNotNull();
  }

  private void verifyMessageWasSent(String message, Object data) {
    verify(session).sendData(message, data);
  }

  private GeneralResponse<BetsResponse> responseFromFile(String path) {
    BetsResponse betsResponse = TestUtils.deserializeWithGson(path, BetsResponse.class);
    return new GeneralResponse<>(betsResponse, null);
  }
}
