package com.ladbrokescoral.cashout.service;

import com.coral.bpp.api.model.bet.api.request.AccountHistoryRequest;
import com.coral.bpp.api.model.bet.api.request.GetBetDetailRequest;
import com.coral.bpp.api.model.bet.api.response.StatusResponse;
import com.coral.bpp.api.model.bet.api.response.accountHistory.Paging;
import com.coral.bpp.api.model.bet.api.response.accountHistory.ResponseTransAccountHistory;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.LottoBetResponse;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.PoolBet;
import com.coral.bpp.api.model.bet.api.response.oxi.base.Bet;
import com.coral.bpp.api.service.BppApiAsync;
import com.ladbrokescoral.cashout.exception.BppFailedGetBetDetailsRequestException;
import com.ladbrokescoral.cashout.model.response.InitialAccountHistoryBetResponse;
import com.ladbrokescoral.cashout.util.JsonUtil;
import com.newrelic.api.agent.ExternalParameters;
import com.newrelic.api.agent.HttpParameters;
import com.newrelic.api.agent.NewRelic;
import com.newrelic.api.agent.Token;
import com.newrelic.api.agent.Trace;
import java.net.URI;
import java.net.URISyntaxException;
import java.text.MessageFormat;
import java.util.Collections;
import java.util.List;
import java.util.Objects;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Service
public class BppServiceImpl implements BppService {

  private final BppApiAsync bppApiAsyncHeavy;
  private final BppApiAsync bppApiAsyncLight;
  private final URI bppUrl;
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  public BppServiceImpl(
      BppApiAsync bppApiAsyncHeavy,
      BppApiAsync bppApiAsyncLight,
      @Value("${bpp.url}") String bppUrl)
      throws URISyntaxException {
    this.bppApiAsyncHeavy = bppApiAsyncHeavy;
    this.bppApiAsyncLight = bppApiAsyncLight;
    this.bppUrl = new URI(bppUrl);
  }

  @Override
  @Trace(dispatcher = true, metricName = "/bpp/getBetDetail")
  public Mono<List<Bet>> getBetDetail(GetBetDetailRequest getBetDetailRequest) {
    ASYNC_LOGGER.info("BppServiceImpl getBetDetail {} ", getBetDetailRequest);
    ExternalParameters params =
        HttpParameters.library("Bpp-Api HttpClient")
            .uri(bppUrl)
            .procedure("get BPP betDetail")
            .noInboundHeaders()
            .build();
    NewRelic.getAgent().getTracedMethod().reportAsExternal(params);
    final Token newRelicToken = NewRelic.getAgent().getTransaction().getToken();
    newRelicToken.expire();

    return bppApiAsyncLight
        .getBetDetail(getBetDetailRequest)
        .map(
            response -> {
              newRelicToken.link();
              return response;
            })
        .filter(Objects::nonNull)
        .filter(response -> Objects.nonNull(response.getResponse()))
        .filter(
            response ->
                validateResponse(
                    response.getResponse().getReturnStatus(),
                    JsonUtil.toJson(getBetDetailRequest),
                    JsonUtil.toJson(response),
                    false))
        .map(
            response -> {
              List<Bet> bets = response.getResponse().getRespTransGetBetDetail().getBet();
              return bets == null ? Collections.emptyList() : bets;
            });
  }

  @Override
  public Mono<InitialAccountHistoryBetResponse> accountHistory(
      AccountHistoryRequest accountHistoryRequest) {
    return getResponse(accountHistoryRequest).map(this::initialAccountHistoryResp);
  }

  @Override
  public Mono<List<BetSummaryModel>> accountHistoryOpenBets(
      AccountHistoryRequest accountHistoryRequest) {
    return getResponse(accountHistoryRequest)
        .expand(
            response -> {
              Paging paging = response.getResponse().getModel().getPaging();
              String pagingToken = paging == null ? "" : paging.getToken();
              if (pagingToken.isEmpty()) {
                return Mono.empty();
              }
              accountHistoryRequest.setFromDate(null);
              accountHistoryRequest.setToDate(null);
              accountHistoryRequest.setSettled(null);
              accountHistoryRequest.setPagingBlockSize(null);
              accountHistoryRequest.setGroup(null);
              accountHistoryRequest.setBlockSize("20");
              accountHistoryRequest.setPagingToken(pagingToken);
              return getResponse(accountHistoryRequest);
            })
        .flatMap(
            response ->
                Flux.fromIterable(
                    response.getResponse().getModel().getBet() == null
                        ? Collections.emptyList()
                        : response.getResponse().getModel().getBet()))
        .collectList();
  }

  private Mono<ResponseTransAccountHistory> getResponse(
      AccountHistoryRequest accountHistoryRequest) {
    return bppApiAsyncHeavy
        .getAccountHistory(accountHistoryRequest)
        .filter(Objects::nonNull)
        .filter(response -> Objects.nonNull(response.getResponse()))
        .filter(
            response ->
                validateResponse(
                    response.getResponse().getReturnStatus(),
                    JsonUtil.toJson(accountHistoryRequest),
                    JsonUtil.toJson(response),
                    true));
  }

  private InitialAccountHistoryBetResponse initialAccountHistoryResp(
      ResponseTransAccountHistory response) {
    List<BetSummaryModel> bets =
        response.getResponse().getModel().getBet() == null
            ? Collections.emptyList()
            : response.getResponse().getModel().getBet();

    List<PoolBet> poolBets =
        response.getResponse().getModel().getPoolBet() == null
            ? Collections.emptyList()
            : response.getResponse().getModel().getPoolBet();

    List<LottoBetResponse> lootBets =
        response.getResponse().getModel().getLottoBetResponse() == null
            ? Collections.emptyList()
            : response.getResponse().getModel().getLottoBetResponse();

    Paging paging =
        response.getResponse().getModel().getPaging() == null
            ? new Paging()
            : response.getResponse().getModel().getPaging();
    String token = response.getResponse().getModel().getToken();
    String count = response.getResponse().getBetCount();

    return new InitialAccountHistoryBetResponse(bets, poolBets, lootBets, paging, token, count);
  }

  private boolean validateResponse(
      StatusResponse returnStatus, String request, String response, boolean throwException) {
    boolean isSuccessful = returnStatus.getMessage().equals(StatusResponse.SUCCESS);
    if (!isSuccessful) {
      String errorMessage =
          MessageFormat.format(
              "getBetDetails failed. Request: {0} Response: {1}", request, response);
      ASYNC_LOGGER.error(errorMessage);
      NewRelic.noticeError(errorMessage);
      if (throwException) {
        throw new BppFailedGetBetDetailsRequestException();
      }
    }
    return isSuccessful;
  }
}
