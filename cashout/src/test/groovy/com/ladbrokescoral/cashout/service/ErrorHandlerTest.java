package com.ladbrokescoral.cashout.service;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.coral.bpp.api.exception.BppConnectionException;
import com.coral.bpp.api.exception.BppUnauthorizedException;
import com.ladbrokescoral.cashout.api.client.exception.OpenBetCashoutServiceConnectionException;
import com.ladbrokescoral.cashout.api.client.exception.OpenBetCashoutServiceFailedRequestException;
import com.ladbrokescoral.cashout.api.client.exception.OpenBetCashoutServiceFailedResponseException;
import com.ladbrokescoral.cashout.exception.BppFailedGetBetDetailsRequestException;
import com.ladbrokescoral.cashout.model.Code;
import com.ladbrokescoral.cashout.model.SSEType;
import com.ladbrokescoral.cashout.model.response.BetResponse;
import com.ladbrokescoral.cashout.model.response.ErrorBetResponse;
import java.time.Duration;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.http.codec.ServerSentEvent;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

public class ErrorHandlerTest {

  ErrorHandler errorHandler;

  @BeforeEach
  public void setUp() {
    errorHandler = new DefaultErrorHandler();
  }

  @Test
  public void errorHandlerTest() {

    verifyExceptionIsConvertedToErrorCode(
        null,
        new OpenBetCashoutServiceConnectionException(),
        Code.OPEN_BET_CASHOUT_SERVICE_CONNECTION_ERROR,
        SSEType.CASHOUT_UPDATE);

    verifyExceptionIsConvertedToErrorCode(
        null,
        new OpenBetCashoutServiceFailedRequestException(),
        Code.OPEN_BET_CASHOUT_SERVICE_FAILED_REQUEST_ERROR,
        SSEType.CASHOUT_UPDATE);

    verifyExceptionIsConvertedToErrorCode(
        null,
        new OpenBetCashoutServiceFailedResponseException(),
        Code.OPEN_BET_CASHOUT_SERVICE_FAILED_RESPONSE_ERROR,
        SSEType.CASHOUT_UPDATE);

    verifyExceptionIsConvertedToErrorCode(
        SSEType.BET_UPDATE,
        new BppUnauthorizedException("Unauthorized"),
        Code.UNAUTHORIZED_ACCESS,
        SSEType.BET_UPDATE);
    verifyExceptionIsConvertedToErrorCode(
        SSEType.INITIAL,
        new BppUnauthorizedException("Unauthorized"),
        Code.UNAUTHORIZED_ACCESS,
        SSEType.INITIAL);

    verifyExceptionIsConvertedToErrorCode(
        SSEType.BET_UPDATE,
        new BppConnectionException(),
        Code.BET_PLACEMENT_CONNECTION_ERROR,
        SSEType.BET_UPDATE);

    verifyExceptionIsConvertedToErrorCode(
        SSEType.INITIAL,
        new BppConnectionException(),
        Code.BET_PLACEMENT_CONNECTION_ERROR,
        SSEType.INITIAL);

    verifyExceptionIsConvertedToErrorCode(
        SSEType.BET_UPDATE,
        new BppFailedGetBetDetailsRequestException(),
        Code.BET_PLACEMENT_FAILED_GET_BET_DETAILS_ERROR,
        SSEType.BET_UPDATE);
    verifyExceptionIsConvertedToErrorCode(
        SSEType.INITIAL,
        new BppFailedGetBetDetailsRequestException(),
        Code.BET_PLACEMENT_FAILED_GET_BET_DETAILS_ERROR,
        SSEType.INITIAL);

    verifyExceptionIsConvertedToErrorCode(
        SSEType.BET_UPDATE,
        new IllegalArgumentException(), // example of unexpected exception
        Code.UNKNOWN_SERVICE_ERROR,
        SSEType.BET_UPDATE);
    verifyExceptionIsConvertedToErrorCode(
        SSEType.INITIAL,
        new IllegalArgumentException(), // example of unexpected exception
        Code.UNKNOWN_SERVICE_ERROR,
        SSEType.INITIAL);
  }

  private void verifyExceptionIsConvertedToErrorCode(
      SSEType inputSseType, Exception inputException, Code outputErrorCode, SSEType outputSseType) {
    Flux<ServerSentEvent<BetResponse>> resultFlux =
        errorHandler.handleFlux(inputException, inputSseType);
    StepVerifier.withVirtualTime(() -> resultFlux)
        .thenAwait(Duration.ofMinutes(1))
        .assertNext(
            sse -> {
              assertEquals(outputSseType.getValue(), sse.event());
              ErrorBetResponse data = (ErrorBetResponse) sse.data();
              assertEquals(outputErrorCode, data.getError().getCode());
            })
        .thenCancel()
        .verify();

    Mono<ServerSentEvent<BetResponse>> resultMono =
        errorHandler.handleMono(inputException, inputSseType);
    StepVerifier.create(resultMono)
        .assertNext(
            sse -> {
              assertEquals(outputSseType.getValue(), sse.event());
              ErrorBetResponse data = (ErrorBetResponse) sse.data();
              assertEquals(outputErrorCode, data.getError().getCode());
            })
        .verifyComplete();
  }
}
