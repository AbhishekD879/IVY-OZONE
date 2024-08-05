package com.ladbrokescoral.cashout.service.updates;

import com.ladbrokescoral.cashout.api.client.RemoteCashoutApi;
import com.ladbrokescoral.cashout.api.client.entity.request.CashoutOfferRequest;
import com.ladbrokescoral.cashout.api.client.entity.request.CashoutRequest;
import com.ladbrokescoral.cashout.api.client.entity.response.CashoutOffer;
import com.ladbrokescoral.cashout.config.CashoutOfferBufferingProperties;
import com.ladbrokescoral.cashout.model.response.UpdateDto;
import com.ladbrokescoral.cashout.util.Message;
import com.newrelic.api.agent.NewRelic;
import io.netty.util.NettyRuntime;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.function.Function;
import java.util.stream.Collectors;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.reactivestreams.Publisher;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Primary;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import reactor.core.Disposable;
import reactor.core.publisher.Flux;
import reactor.core.publisher.FluxSink;
import reactor.core.publisher.FluxSink.OverflowStrategy;
import reactor.core.publisher.GroupedFlux;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;
import reactor.util.function.Tuple2;

@Service
@Primary
public class AsyncCashoutOfferServiceImpl
    implements AsyncCashoutOfferService, BufferedDisposable<CashoutRequest> {
  private Message message;
  private FluxSink<CashoutRequest> requestsSink;
  private Function<CashoutOffer, UpdateDto> cashoutOfferToBetUpdate;
  private BetUpdatesTopic betUpdatesTopic;
  private final Disposable cashoutOffersFlux;
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  public AsyncCashoutOfferServiceImpl(
      CashoutOfferBufferingProperties cashoutOfferProps,
      RemoteCashoutApi remoteCashoutApi,
      Function<CashoutOffer, UpdateDto> cashoutOfferToBetUpdate,
      BetUpdatesTopic betUpdatesTopic,
      @Value("${cashout.scheduler.cashout-offer.cpu.factor:1}") int cpuFactor,
      @Value("${cashout-offer.buffer.overflow-strategy:BUFFER}") String overflowStrategy) {
    this.cashoutOfferToBetUpdate = cashoutOfferToBetUpdate;
    this.betUpdatesTopic = betUpdatesTopic;
    cashoutOffersFlux =
        Flux.<CashoutRequest>create(
                sink -> this.requestsSink = sink, OverflowStrategy.valueOf(overflowStrategy))
            .publishOn(
                Schedulers.newParallel(
                    "Cashout-Offers-Parallel", (NettyRuntime.availableProcessors() * cpuFactor)))
            .name("asyncCashoutOffersFlux")
            .groupBy(this::defineGroup)
            .flatMap(
                g ->
                    g.window(cashoutOfferProps.getWindowTime())
                        .map(Flux::distinct)
                        .map(
                            f ->
                                f.groupBy(AsyncCashoutOfferServiceImpl::betId)
                                    .flatMap(
                                        AsyncCashoutOfferServiceImpl::takeLatestCashoutOffer,
                                        Integer.MAX_VALUE,
                                        Integer.MAX_VALUE))
                        .flatMap(
                            w ->
                                w.bufferTimeout(
                                    cashoutOfferProps.maxSizeForGroup(g.key()),
                                    cashoutOfferProps.getMaxTime()),
                            Integer.MAX_VALUE,
                            Integer.MAX_VALUE)
                        .doOnNext(
                            buffered ->
                                NewRelic.incrementCounter(
                                    String.format("Custom/CashoutOffers/%s", g.key()),
                                    buffered.size()))
                        .flatMap(this::mergeRequests, Integer.MAX_VALUE, Integer.MAX_VALUE),
                Integer.MAX_VALUE,
                Integer.MAX_VALUE)
            .flatMap(
                req ->
                    remoteCashoutApi
                        .getCashoutOffers(req)
                        .filter(offer -> offer.getCashoutOfferReqRef() != null)
                        .flatMap(
                            of -> this.zipOfferAndBetUpdate(of, req.getShouldActivate()),
                            Integer.MAX_VALUE,
                            Integer.MAX_VALUE)
                        .doOnNext(this::sendBetUpdate)
                        .onErrorResume(
                            t -> {
                              ASYNC_LOGGER.error("OB Cashout error", t);
                              return Mono.empty();
                            }),
                Integer.MAX_VALUE,
                Integer.MAX_VALUE)
            .onErrorResume(
                t -> {
                  ASYNC_LOGGER.warn("error", t);
                  return Flux.empty();
                })
            .subscribe();

    ASYNC_LOGGER.info("Cashout buffering properties: {}", cashoutOfferProps);
  }

  private static Publisher<CashoutRequest> takeLatestCashoutOffer(
      GroupedFlux<String, CashoutRequest> groupOfCashoutRequestForSameBet) {
    return Flux.from(
        groupOfCashoutRequestForSameBet
            .collectList()
            .map(AsyncCashoutOfferServiceImpl::takeLatestCashoutOffer));
  }

  private static CashoutRequest takeLatestCashoutOffer(
      List<CashoutRequest> cashoutOffersForSameBet) {
    CashoutRequest latestRequestInGroup =
        cashoutOffersForSameBet.get(cashoutOffersForSameBet.size() - 1);
    boolean shouldActivate =
        cashoutOffersForSameBet.stream().anyMatch(CashoutRequest::isActivationRequest);
    if (shouldActivate) {
      latestRequestInGroup.setShouldActivate(true);
    }
    return latestRequestInGroup;
  }

  private static String betId(CashoutRequest req) {
    return req.getCashoutOfferRequests().get(0).getCashoutOfferReqRef();
  }

  private String defineGroup(CashoutRequest request) {
    Iterator<CashoutOfferRequest> iterator = request.getCashoutOfferRequests().iterator();
    if (iterator.hasNext()) {
      return iterator.next().getBet().getBetType();
    }
    return "default_group";
  }

  private Flux<CashoutRequest> mergeRequests(List<CashoutRequest> bufferedCashoutRequests) {
    message = new Message();
    if (bufferedCashoutRequests.size() > 1) {
      Map<Boolean, List<CashoutRequest>> byActivation =
          bufferedCashoutRequests.stream()
              .collect(Collectors.groupingBy(CashoutRequest::isActivationRequest));

      List<CashoutRequest> result = byActivation.getOrDefault(true, new ArrayList<>());
      List<CashoutRequest> regularCashoutRequests =
          byActivation.getOrDefault(false, Collections.emptyList());
      if (!regularCashoutRequests.isEmpty()) {
        List<CashoutOfferRequest> flattenRequests =
            regularCashoutRequests.stream()
                .flatMap(r -> r.getCashoutOfferRequests().stream())
                .collect(Collectors.toList());

        CashoutRequest mergedRequest =
            CashoutRequest.builder().cashoutOfferRequests(flattenRequests).build();

        result.add(mergedRequest);
      }
      message.setMessage(result.toString());
      ASYNC_LOGGER.info(
          "Merged [{} -> {}]: {}", bufferedCashoutRequests.size(), result.size(), message);
      return Flux.fromIterable(result);
    } else {
      message.setMessage(bufferedCashoutRequests.toString());
      ASYNC_LOGGER.trace("Not merged single item: {}", message);
      return Flux.just(bufferedCashoutRequests.get(0));
    }
  }

  private void sendBetUpdate(Tuple2<CashoutOffer, UpdateDto> offerAndUpdateTuple) {
    this.betUpdatesTopic.sendBetUpdate(
        offerAndUpdateTuple.getT1().getCashoutOfferReqRef(), offerAndUpdateTuple.getT2());
  }

  private Publisher<Tuple2<CashoutOffer, UpdateDto>> zipOfferAndBetUpdate(
      CashoutOffer offer, Boolean shouldActivate) {
    return Mono.zip(
        Mono.just(offer),
        Mono.just(cashoutOfferToBetUpdate.apply(offer))
            .doOnNext(
                betUpdate ->
                    Optional.ofNullable(betUpdate)
                        .map(UpdateDto::getCashoutData)
                        .ifPresent(data -> data.setShouldActivate(shouldActivate))));
  }

  @Override
  @Async
  public void acceptCashoutOfferRequest(CashoutRequest cashoutRequest) {
    this.requestsSink.next(cashoutRequest);
  }

  @Override
  public Disposable getDisposable() {
    return cashoutOffersFlux;
  }

  @Override
  public FluxSink<CashoutRequest> getSink() {
    return requestsSink;
  }
}
