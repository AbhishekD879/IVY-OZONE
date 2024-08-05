package com.coral.oxygen.middleware.ms.quickbet.connector;

import static com.coral.oxygen.middleware.ms.quickbet.Messages.INTERNAL_PLACE_BET_PROCESSING;
import static com.coral.oxygen.middleware.ms.quickbet.Messages.PLACE_BET_ERROR_RESPONSE_CODE;
import static com.coral.oxygen.middleware.ms.quickbet.Messages.PLACE_BET_OVERASK_SPLITTED_RESPONSE_CODE;
import static com.coral.oxygen.middleware.ms.quickbet.Messages.PLACE_BET_RESPONSE_CODE;

import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.configuration.OveraskReadBetConfiguration;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.RegularPlaceBetResponse;
import com.coral.oxygen.middleware.ms.quickbet.converter.MultiReadBetResponseAdapter;
import com.coral.oxygen.middleware.ms.quickbet.converter.MultiReadBetResponseAdapterFactory;
import com.entain.oxygen.bettingapi.model.bet.api.request.BetRef;
import com.entain.oxygen.bettingapi.model.bet.api.response.Bet;
import com.entain.oxygen.bettingapi.model.bet.api.response.BetError;
import com.entain.oxygen.bettingapi.model.bet.api.response.BetsResponse;
import com.entain.oxygen.bettingapi.model.bet.api.response.ErrorBody;
import com.entain.oxygen.bettingapi.model.bet.api.response.GeneralResponse;
import io.vavr.collection.List;
import io.vavr.control.Option;
import java.util.Optional;
import java.util.UUID;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

public class OveraskReadBetTask implements Runnable {

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  private final UUID taskId = UUID.randomUUID();
  private Integer retryCounter = 0;

  private Session session;
  private List<BetRef> betsToRead;

  private final BetReader betReader;
  private final OveraskReadBetConfiguration overaskConfiguration;
  private final MultiReadBetResponseAdapterFactory multiReadBetResponseAdapterFactory;
  private final OveraskResponseFactory overaskResponseFactory;

  public OveraskReadBetTask(
      Session session,
      List<BetRef> betsToRead,
      BetReader betReader,
      OveraskReadBetConfiguration overaskConfiguration,
      MultiReadBetResponseAdapterFactory multiReadBetResponseAdapterFactory,
      OveraskResponseFactory overaskResponseFactory) {
    this.session = session;
    this.betReader = betReader;
    this.betsToRead = betsToRead;
    this.overaskConfiguration = overaskConfiguration;
    this.multiReadBetResponseAdapterFactory = multiReadBetResponseAdapterFactory;
    this.overaskResponseFactory = overaskResponseFactory;
  }

  @Override
  public void run() {
    if (retryCounter++ >= overaskConfiguration.getMaxNumberOfRetries()) {
      overaskResponseFactory.createTimeoutErrorResponse(PLACE_BET_ERROR_RESPONSE_CODE);
      finishTask();
    }

    readBet();
  }

  private void readBet() {
    Optional<GeneralResponse<BetsResponse>> responseOptional = betReader.read(betsToRead);

    if (responseOptional.isPresent()) {
      processReadBetResponse(responseOptional.get());
    } else {
      String error = "ReadBet response cannot be null";
      ASYNC_LOGGER.error(error);
      session.sendData(
          PLACE_BET_ERROR_RESPONSE_CODE.code(),
          RegularPlaceBetResponse.errorResponse(INTERNAL_PLACE_BET_PROCESSING.code(), error));

      finishTask();
    }
  }

  private void processReadBetResponse(GeneralResponse<BetsResponse> response) {
    ErrorBody errorBody = response.getErrorBody();
    if (errorBody != null) {
      overaskResponseFactory.createErrorResponse(PLACE_BET_ERROR_RESPONSE_CODE, errorBody);
      finishTask();
      return;
    }

    BetsResponse betResponse = response.getBody();
    List<BetError> betErrors =
        Option.of(betResponse.getBetError()).map(List::ofAll).getOrElse(List::empty);
    if (betErrors.nonEmpty()) {
      session.sendData(
          PLACE_BET_ERROR_RESPONSE_CODE.code(), RegularPlaceBetResponse.errorResponse(betResponse));
      finishTask();
    } else {
      List<Bet> bets = List.ofAll(betResponse.getBet());
      MultiReadBetResponseAdapter multiReadBetResponseAdapter =
          multiReadBetResponseAdapterFactory.from(betResponse);

      if (bets.size() > this.betsToRead.size()) {
        overaskResponseFactory.createSuccessOveraskResponse(
            PLACE_BET_OVERASK_SPLITTED_RESPONSE_CODE, betResponse);
        finishTask();
      } else if (multiReadBetResponseAdapter.allFinished()) {
        overaskResponseFactory.createSuccessOveraskResponse(PLACE_BET_RESPONSE_CODE, betResponse);
        finishTask();
      }
    }
  }

  private void finishTask() {
    ASYNC_LOGGER.info(
        "Finishing overask/bir processing for bets {} in session {}",
        betsToRead.map(BetRef::getId),
        session);
    session.finishTask(taskId);
  }

  UUID getTaskId() {
    return taskId;
  }
}
