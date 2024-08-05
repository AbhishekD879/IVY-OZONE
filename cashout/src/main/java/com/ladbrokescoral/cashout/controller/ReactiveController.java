package com.ladbrokescoral.cashout.controller;

import static org.springframework.http.MediaType.TEXT_EVENT_STREAM_VALUE;

import com.coral.bpp.api.exception.BppUnauthorizedException;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.ladbrokescoral.cashout.bpptoken.BppToken;
import com.ladbrokescoral.cashout.bpptoken.BppTokenOperations;
import com.ladbrokescoral.cashout.model.SSEType;
import com.ladbrokescoral.cashout.model.response.BetResponse;
import com.ladbrokescoral.cashout.service.AccountHistoryService;
import com.ladbrokescoral.cashout.service.BetUpdateService;
import com.ladbrokescoral.cashout.service.ErrorHandler;
import com.ladbrokescoral.cashout.util.SSEFactory;
import com.newrelic.api.agent.NewRelic;
import com.newrelic.api.agent.Token;
import com.newrelic.api.agent.Trace;
import java.util.List;
import org.springframework.http.codec.ServerSentEvent;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@RestController
public class ReactiveController {

  private BetUpdateService betUpdateService;
  private AccountHistoryService accountHistoryService;
  private ErrorHandler errorHandler;
  private BppTokenOperations bppTokenOps;

  public ReactiveController(
      BetUpdateService betUpdateService,
      AccountHistoryService accountHistoryService,
      ErrorHandler errorHandler,
      BppTokenOperations bppTokenOperations) {
    this.betUpdateService = betUpdateService;
    this.accountHistoryService = accountHistoryService;
    this.errorHandler = errorHandler;
    this.bppTokenOps = bppTokenOperations;
  }

  @GetMapping(value = "/bet-details", produces = TEXT_EVENT_STREAM_VALUE)
  @Trace(dispatcher = true, metricName = "/controller/bet-details")
  public Flux<ServerSentEvent<BetResponse>> getBetDetails(@RequestParam String token) {
    final Token newRelicToken = NewRelic.getAgent().getTransaction().getToken();

    return getBets(token, newRelicToken);
  }

  private Flux<ServerSentEvent<BetResponse>> getBets(String token, Token newRelicToken) {

    try {
      BppToken bppToken = bppTokenOps.parseToken(token);
      Mono<List<BetSummaryModel>> accountHistoryInitBets =
          accountHistoryService
              .getDetailedAccountHistoryWithOpenBetsOnly(bppToken.getToken())
              .cache();

      Mono<ServerSentEvent<BetResponse>> accountHistoryInitialData =
          accountHistoryInitBets
              .map(SSEFactory::initialAccHistory)
              .onErrorResume(ex -> errorHandler.handleMono(ex, SSEType.INITIAL));

      Flux<ServerSentEvent<BetResponse>> accountHistoryUpdateData =
          betUpdateService
              .getAccHistoryUpdatedBets(bppToken, accountHistoryInitBets, newRelicToken)
              .map(SSEFactory::update)
              .onErrorResume(ex -> errorHandler.handleFlux(ex, SSEType.BET_UPDATE));

      return accountHistoryInitialData.concatWith(accountHistoryUpdateData);
    } catch (BppUnauthorizedException e) {
      return errorHandler.handleMono(e, SSEType.INITIAL).flux();
    }
  }
}
