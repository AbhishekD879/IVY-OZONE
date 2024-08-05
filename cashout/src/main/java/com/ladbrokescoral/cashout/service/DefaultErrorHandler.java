package com.ladbrokescoral.cashout.service;

import com.ladbrokescoral.cashout.api.client.exception.OpenBetCashoutServiceConnectionException;
import com.ladbrokescoral.cashout.api.client.exception.OpenBetCashoutServiceFailedRequestException;
import com.ladbrokescoral.cashout.api.client.exception.OpenBetCashoutServiceFailedResponseException;
import com.ladbrokescoral.cashout.model.Code;
import com.ladbrokescoral.cashout.model.SSEType;
import com.ladbrokescoral.cashout.model.response.BetResponse;
import com.ladbrokescoral.cashout.util.SSEFactory;
import com.newrelic.api.agent.NewRelic;
import java.time.Duration;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.http.codec.ServerSentEvent;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Service
public class DefaultErrorHandler implements ErrorHandler {

  private static final String UNKNOWN_SERVICE_ERROR_MESSAGE =
      "Something went wrong. Unexpected exception";

  private static final Duration TIME_INTERVAL = Duration.ofHours(10000);
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  @Override
  public Mono<ServerSentEvent<BetResponse>> handleMono(Throwable error, SSEType sseType) {
    return Mono.just(handle(error, sseType));
  }

  /*-
   *
   * @param error - exception that was throws
   * @param sseType - event id to be returned via SSE
   * @return error object (infinite connection is holded to may the client close it!)
   */
  @Override
  public Flux<ServerSentEvent<BetResponse>> handleFlux(Throwable error, SSEType sseType) {
    return Flux.just(handle(error, sseType))
        .concatWith(Flux.interval(TIME_INTERVAL).flatMap(hr -> Flux.empty()));
  }

  private ServerSentEvent<BetResponse> handle(Throwable error, SSEType inputSseType) {
    Code errorCode = Code.fromException(error);
    SSEType sseType = inputSseType;
    if (error instanceof OpenBetCashoutServiceConnectionException) {
      sseType = SSEType.CASHOUT_UPDATE;
    } else if (error instanceof OpenBetCashoutServiceFailedRequestException) {
      sseType = SSEType.CASHOUT_UPDATE;
    } else if (error instanceof OpenBetCashoutServiceFailedResponseException) {
      sseType = SSEType.CASHOUT_UPDATE;
    }
    if (errorCode == Code.UNKNOWN_SERVICE_ERROR) {
      ASYNC_LOGGER.error(UNKNOWN_SERVICE_ERROR_MESSAGE, error);
      NewRelic.noticeError(error);
    }
    return SSEFactory.error(errorCode, sseType);
  }
}
