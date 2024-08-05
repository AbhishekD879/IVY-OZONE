package com.ladbrokescoral.cashout.service.updates;

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.ladbrokescoral.cashout.api.client.RemoteCashoutApi;
import com.ladbrokescoral.cashout.api.client.entity.request.CashoutOfferRequest;
import com.ladbrokescoral.cashout.api.client.entity.request.CashoutRequest;
import com.ladbrokescoral.cashout.api.client.entity.response.CashoutOffer;
import com.ladbrokescoral.cashout.converter.BetToCashoutOfferRequestConverter;
import com.ladbrokescoral.cashout.model.response.UpdateDto;
import com.ladbrokescoral.cashout.service.BppService;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.util.stream.Stream;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class CashoutService {

  @Value("${cashout.offer.request-size:1}")
  private int cashoutOfferReqSize;

  @Value("${cashout.bet.details.bet-ids.size:1}")
  private int betIdSize;

  private BetToCashoutOfferRequestConverter converter;
  private RemoteCashoutApi remoteCashoutApi;
  private Function<CashoutOffer, UpdateDto> cashoutOfferToBetUpdate;
  private BetUpdatesTopic betUpdatesTopic;
  private BppService bppService;
  private AsyncCashoutOfferService asyncCashoutOfferService;
  private AsyncBetDetailService asyncBetDetailService;
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  @Autowired
  public CashoutService(
      BetToCashoutOfferRequestConverter converter,
      RemoteCashoutApi remoteCashoutApi,
      Function<CashoutOffer, UpdateDto> cashoutOfferToBetUpdate,
      BetUpdatesTopic betUpdatesTopic,
      BppService bppService,
      AsyncCashoutOfferService asyncCashoutOfferService,
      AsyncBetDetailService asyncBetDetailService) {
    this.converter = converter;
    this.remoteCashoutApi = remoteCashoutApi;
    this.cashoutOfferToBetUpdate = cashoutOfferToBetUpdate;
    this.betUpdatesTopic = betUpdatesTopic;
    this.bppService = bppService;
    this.asyncCashoutOfferService = asyncCashoutOfferService;
    this.asyncBetDetailService = asyncBetDetailService;
  }

  public void prepareCashoutReq(Set<BetSummaryModel> bets, boolean shouldActivate) {
    Map<String, BetSummaryModel> betWiseInitialPotentialValues =
        bets.parallelStream()
            .collect(Collectors.toConcurrentMap(BetSummaryModel::getId, Function.identity()));
    List<BetSummaryModel> betSummaryModels =
        new ArrayList<>(betWiseInitialPotentialValues.values());
    List<List<BetSummaryModel>> betSummaryModelSubLists =
        prepareSubLists(betSummaryModels, cashoutOfferReqSize).collect(Collectors.toList());
    if (!betSummaryModelSubLists.isEmpty()) {
      ASYNC_LOGGER.info(
          "BetSummary Model Sublists Size:{} shouldActivate:{}",
          betSummaryModelSubLists.size(),
          shouldActivate);
      betSummaryModelSubLists.forEach(
          (List<BetSummaryModel> eachlist) -> {
            List<CashoutOfferRequest> cashoutOfferRequests = new ArrayList<>();
            eachlist.forEach(
                (BetSummaryModel bet) -> {
                  CashoutRequest cashoutRequest = converter.convert(Collections.singletonList(bet));
                  cashoutOfferRequests.add(cashoutRequest.getCashoutOfferRequests().get(0));
                });
            CashoutRequest cashoutRequest =
                CashoutRequest.builder()
                    .cashoutOfferRequests(cashoutOfferRequests)
                    .shouldActivate(shouldActivate)
                    .build();
            asyncCashoutOfferService.acceptCashoutOfferRequest(cashoutRequest);
          });
    }
  }

  private <T> Stream<List<T>> prepareSubLists(List<T> source, int length) {
    if (length <= 0) throw new IllegalArgumentException("length = " + length);
    int size = source.size();
    if (size <= 0) return Stream.empty();
    int fullChunks = (size - 1) / length;
    return IntStream.range(0, fullChunks + 1)
        .mapToObj(
            n ->
                new ArrayList<>(
                    source.subList(n * length, n == fullChunks ? size : (n + 1) * length)));
  }

  public List<List<String>> betIdSubList(Set<String> betIds) {
    List<String> bets = new ArrayList<>(betIds);
    List<List<String>> betIdSubList = prepareSubLists(bets, betIdSize).collect(Collectors.toList());
    ASYNC_LOGGER.info("BetIdSubList Size :{}", betIdSubList.size());
    return betIdSubList;
  }

  public void getBetDetail(BetDetailRequestCtx betDetailrequestCtx) {
    asyncBetDetailService.acceptBetDetailRequest(betDetailrequestCtx);
  }
}
