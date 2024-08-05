package com.ladbrokescoral.cashout.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.when;

import com.coral.bpp.api.model.bet.api.request.AccountHistoryRequest;
import com.coral.bpp.api.model.bet.api.request.GetBetDetailRequest;
import com.coral.bpp.api.model.bet.api.response.StatusResponse;
import com.coral.bpp.api.model.bet.api.response.accountHistory.Paging;
import com.coral.bpp.api.model.bet.api.response.accountHistory.RespTransAccountHistory;
import com.coral.bpp.api.model.bet.api.response.accountHistory.Response;
import com.coral.bpp.api.model.bet.api.response.accountHistory.ResponseTransAccountHistory;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.LottoBetResponse;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.PoolBet;
import com.coral.bpp.api.model.bet.api.response.betDetail.RespTransGetBetDetail;
import com.coral.bpp.api.model.bet.api.response.betDetail.ResponseTransGetBetDetail;
import com.coral.bpp.api.model.bet.api.response.oxi.base.Bet;
import com.coral.bpp.api.service.BppApiAsync;
import com.ladbrokescoral.cashout.exception.BppFailedGetBetDetailsRequestException;
import com.ladbrokescoral.cashout.model.response.InitialAccountHistoryBetResponse;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

@ExtendWith(MockitoExtension.class)
class BppServiceTest {

  BppService bppService;

  @Mock private BppApiAsync bppApi;
  private AccountHistoryRequest accountHistoryRequest;

  @BeforeEach
  public void setUp() throws URISyntaxException {
    bppService = new BppServiceImpl(bppApi, bppApi, "http://bpp_url/");
    accountHistoryRequest = AccountHistoryRequest.builder().build();
  }

  @Test
  void testGetBetDetailsReturnsBets() {
    BetSummaryModel bet1 = new BetSummaryModel();
    bet1.setId("12");
    BetSummaryModel bet2 = new BetSummaryModel();
    bet2.setId("12");
    Paging paging = new Paging();
    paging.setToken("abcx");
    paging.setBlockSize("20");

    ResponseTransAccountHistory bppResponse =
        accHistoryBppResponse("success", Arrays.asList(bet1, bet2), paging, "xyza");

    when(bppApi.getAccountHistory(accountHistoryRequest)).thenReturn(Mono.just(bppResponse));

    Mono<InitialAccountHistoryBetResponse> result =
        bppService.accountHistory(accountHistoryRequest);
    StepVerifier.create(result)
        .assertNext(
            bets -> {
              assertEquals(2, bets.getBets().size());
              assertEquals("12", bets.getBets().get(0).getId());
              assertEquals("abcx", bets.getPaging().getToken());
            })
        .expectComplete()
        .verify();
  }

  @Test
  void testGetBetDetailsReturnsBetsPoolAndLottoBets() {
    BetSummaryModel bet = new BetSummaryModel();
    bet.setId("12");
    LottoBetResponse bet1 = new LottoBetResponse();
    bet1.setId("12");
    PoolBet bet2 = new PoolBet();
    bet2.setId("12");
    Paging paging = new Paging();
    paging.setToken("abcx");
    paging.setBlockSize("20");

    ResponseTransAccountHistory bppResponse =
        accHistoryBppResponseMyBets(
            "success",
            Arrays.asList(bet),
            Arrays.asList(bet1),
            Arrays.asList(bet2),
            paging,
            "xyza");

    when(bppApi.getAccountHistory(accountHistoryRequest)).thenReturn(Mono.just(bppResponse));

    Mono<InitialAccountHistoryBetResponse> result =
        bppService.accountHistory(accountHistoryRequest);
    StepVerifier.create(result)
        .assertNext(
            bets -> {
              assertEquals(1, bets.getBets().size());
              assertEquals("12", bets.getBets().get(0).getId());
              assertEquals("abcx", bets.getPaging().getToken());
            })
        .expectComplete()
        .verify();
  }

  @Test
  void testGetBetDetailsReturnsBetsWithoutPagingToken() {
    BetSummaryModel bet = new BetSummaryModel();
    bet.setId("102");
    Paging paging = new Paging();

    ResponseTransAccountHistory bppResponse =
        accHistoryBppResponse("success", Arrays.asList(bet), paging, "xyza");

    when(bppApi.getAccountHistory(accountHistoryRequest)).thenReturn(Mono.just(bppResponse));

    Mono<InitialAccountHistoryBetResponse> result =
        bppService.accountHistory(accountHistoryRequest);
    StepVerifier.create(result)
        .assertNext(
            bets -> {
              assertEquals(1, bets.getBets().size());
              assertEquals("102", bets.getBets().get(0).getId());
              assertEquals(null, bets.getPaging().getToken());
            })
        .expectComplete()
        .verify();
  }

  @Test
  void testGetBetDetailsWithPaging() {
    BetSummaryModel bet1 = new BetSummaryModel();
    bet1.setId("12");
    BetSummaryModel bet2 = new BetSummaryModel();
    bet2.setId("13");
    Paging paging = new Paging();
    paging.setToken("xyz");
    paging.setBlockSize("20");

    AccountHistoryRequest accountHistoryRequest =
        AccountHistoryRequest.builder()
            .blockSize("20")
            .detailLevel("DETAILED")
            .pagingToken("pagingToken")
            .build();

    ResponseTransAccountHistory bppResponse =
        accHistoryBppResponse("success", Arrays.asList(bet1, bet2), paging, "abcxyz");
    when(bppApi.getAccountHistory(accountHistoryRequest)).thenReturn(Mono.just(bppResponse));

    Mono<InitialAccountHistoryBetResponse> result =
        bppService.accountHistory(accountHistoryRequest);

    StepVerifier.create(result)
        .assertNext(
            bets -> {
              assertEquals(2, bets.getBets().size());
              assertEquals("12", bets.getBets().get(0).getId());
              assertEquals("13", bets.getBets().get(1).getId());
            })
        .expectComplete()
        .verify();
  }

  @Test
  void testGetBetDetailsReturnsEmptyBetsList() {

    ResponseTransAccountHistory bppResponse = accHistoryBppResponse("success", null, null, "");
    when(bppApi.getAccountHistory(accountHistoryRequest)).thenReturn(Mono.just(bppResponse));

    Mono<InitialAccountHistoryBetResponse> result =
        bppService.accountHistory(accountHistoryRequest);
    StepVerifier.create(result)
        .assertNext(
            bets -> {
              assertEquals(0, bets.getBets().size());
            })
        .expectComplete()
        .verify();
  }

  @Test
  @Disabled("")
  void testOpenBetDetailsWithPaging() {
    BetSummaryModel bet1 = new BetSummaryModel();
    bet1.setId("12");
    BetSummaryModel bet2 = new BetSummaryModel();
    bet2.setId("13");

    ResponseTransAccountHistory bppResponse =
        accHistoryOpenBetsBppResp("success", Collections.singletonList(bet1), "pagingToken");
    when(bppApi.getAccountHistory(accountHistoryRequest)).thenReturn(Mono.just(bppResponse));

    AccountHistoryRequest accountHistoryRequest1 =
        AccountHistoryRequest.builder().blockSize("20").pagingToken("pagingToken").build();
    ResponseTransAccountHistory bppResponse1 =
        accHistoryOpenBetsBppResp("success", Collections.singletonList(bet2), "");

    when(bppApi.getAccountHistory(accountHistoryRequest1)).thenReturn(Mono.just(bppResponse1));

    Mono<List<BetSummaryModel>> result = bppService.accountHistoryOpenBets(accountHistoryRequest);
    StepVerifier.create(result)
        .assertNext(
            bets -> {
              assertEquals(2, bets.size());
              assertEquals("12", bets.get(0).getId());
              assertEquals("13", bets.get(1).getId());
            })
        .expectComplete()
        .verify();
  }

  @Test
  void testaccountHistoryOpenBetsReturnsEmptyBetsList() {
    ResponseTransAccountHistory bppResponse = accHistoryOpenBetsBppResp("success", null, "");
    when(bppApi.getAccountHistory(accountHistoryRequest)).thenReturn(Mono.just(bppResponse));

    Mono<List<BetSummaryModel>> result = bppService.accountHistoryOpenBets(accountHistoryRequest);
    StepVerifier.create(result)
        .assertNext(
            bets -> {
              assertEquals(0, bets.size());
            })
        .expectComplete()
        .verify();
  }

  @Test
  void testGetBetDetailsReturnsExceptionInCaseOfFailure() {
    ResponseTransAccountHistory bppResponse = accHistoryBppResponse("failure", null, null, "");
    when(bppApi.getAccountHistory(accountHistoryRequest)).thenReturn(Mono.just(bppResponse));

    Mono<InitialAccountHistoryBetResponse> result =
        bppService.accountHistory(accountHistoryRequest);
    StepVerifier.create(result).expectError(BppFailedGetBetDetailsRequestException.class).verify();
  }

  @Test
  void testaccountHistoryOpenBetsReturnsExceptionInCaseOfFailure() {
    ResponseTransAccountHistory bppResponse = accHistoryBppResponse("failure", null, null, "");
    when(bppApi.getAccountHistory(accountHistoryRequest)).thenReturn(Mono.just(bppResponse));

    Mono<List<BetSummaryModel>> result = bppService.accountHistoryOpenBets(accountHistoryRequest);
    StepVerifier.create(result).expectError(BppFailedGetBetDetailsRequestException.class).verify();
  }

  @Test
  void testGetBetDetailReturnsEmptyBetsList() {
    List<Bet> bet = new ArrayList<>();
    GetBetDetailRequest getBetDetial =
        GetBetDetailRequest.builder().betIds(Arrays.asList("12121212".split(","))).build();
    ResponseTransGetBetDetail resp = new ResponseTransGetBetDetail();
    com.coral.bpp.api.model.bet.api.response.betDetail.Response response =
        new com.coral.bpp.api.model.bet.api.response.betDetail.Response();
    StatusResponse StatusResponse = new StatusResponse("success", "200", "su");
    response.setReturnStatus(StatusResponse);
    RespTransGetBetDetail details = new RespTransGetBetDetail();
    details.setBet(bet);
    response.setRespTransGetBetDetail(details);
    resp.setResponse(response);
    when(bppApi.getBetDetail(getBetDetial)).thenReturn(Mono.just(resp));
    Mono<List<Bet>> result = bppService.getBetDetail(getBetDetial);
    StepVerifier.create(result)
        .assertNext(
            bets -> {
              assertEquals(0, bets.size());
            })
        .expectComplete()
        .verify();
  }

  private ResponseTransAccountHistory accHistoryBppResponse(
      String statusMessage, List<BetSummaryModel> bets, Paging paging, String token) {

    ResponseTransAccountHistory responseTransAccountHistory = new ResponseTransAccountHistory();
    Response response = new Response();

    StatusResponse statusResponse = new StatusResponse();
    statusResponse.setMessage(statusMessage);
    response.setReturnStatus(statusResponse);

    RespTransAccountHistory respTransAccountHistory = new RespTransAccountHistory();
    respTransAccountHistory.setBet(bets);
    respTransAccountHistory.setPaging(paging);
    respTransAccountHistory.setToken(token);

    response.setModel(respTransAccountHistory);
    responseTransAccountHistory.setResponse(response);
    return responseTransAccountHistory;
  }

  private ResponseTransAccountHistory accHistoryBppResponseMyBets(
      String statusMessage,
      List<BetSummaryModel> bets,
      List<LottoBetResponse> lottoBetResponses,
      List<PoolBet> poolBets,
      Paging paging,
      String token) {

    ResponseTransAccountHistory responseTransAccountHistory = new ResponseTransAccountHistory();
    Response response = new Response();

    StatusResponse statusResponse = new StatusResponse();
    statusResponse.setMessage(statusMessage);
    response.setReturnStatus(statusResponse);

    RespTransAccountHistory respTransAccountHistory = new RespTransAccountHistory();
    respTransAccountHistory.setBet(bets);
    respTransAccountHistory.setLottoBetResponse(lottoBetResponses);
    respTransAccountHistory.setPoolBet(poolBets);
    respTransAccountHistory.setPaging(paging);
    respTransAccountHistory.setToken(token);

    response.setModel(respTransAccountHistory);
    responseTransAccountHistory.setResponse(response);
    return responseTransAccountHistory;
  }

  private ResponseTransAccountHistory accHistoryOpenBetsBppResponse(
      String statusMessage, List<BetSummaryModel> bets, Paging paging, String token) {

    ResponseTransAccountHistory responseTransAccountHistory = new ResponseTransAccountHistory();
    Response response = new Response();

    StatusResponse statusResponse = new StatusResponse();
    statusResponse.setMessage(statusMessage);
    response.setReturnStatus(statusResponse);

    RespTransAccountHistory respTransAccountHistory = new RespTransAccountHistory();
    respTransAccountHistory.setBet(bets == null ? Collections.emptyList() : bets);
    respTransAccountHistory.setPaging(paging == null ? new Paging() : paging);
    respTransAccountHistory.setToken(token);

    response.setModel(respTransAccountHistory);
    responseTransAccountHistory.setResponse(response);
    return responseTransAccountHistory;
  }

  private ResponseTransAccountHistory accHistoryReturnOpenBetsBppResponse(
      String statusMessage, List<BetSummaryModel> bets, Paging paging, String token) {

    ResponseTransAccountHistory responseTransAccountHistory = new ResponseTransAccountHistory();
    Response response = new Response();

    StatusResponse statusResponse = new StatusResponse();
    statusResponse.setMessage(statusMessage);
    response.setReturnStatus(statusResponse);

    RespTransAccountHistory respTransAccountHistory = new RespTransAccountHistory();
    respTransAccountHistory.setBet(bets);
    respTransAccountHistory.setPaging(paging);
    respTransAccountHistory.setToken(token);

    response.setModel(respTransAccountHistory);
    responseTransAccountHistory.setResponse(response);
    return responseTransAccountHistory;
  }

  private ResponseTransAccountHistory accHistoryOpenBetsBppResp(
      String statusMessage, List<BetSummaryModel> bets, String pagingToken) {

    ResponseTransAccountHistory responseTransAccountHistory = new ResponseTransAccountHistory();
    Response response = new Response();

    StatusResponse statusResponse = new StatusResponse();
    statusResponse.setMessage(statusMessage);
    response.setReturnStatus(statusResponse);

    RespTransAccountHistory respTransAccountHistory = new RespTransAccountHistory();
    respTransAccountHistory.setBet(bets);

    Paging paging = new Paging();
    paging.setToken(pagingToken);
    respTransAccountHistory.setPaging(paging);

    response.setModel(respTransAccountHistory);
    responseTransAccountHistory.setResponse(response);
    return responseTransAccountHistory;
  }
}
