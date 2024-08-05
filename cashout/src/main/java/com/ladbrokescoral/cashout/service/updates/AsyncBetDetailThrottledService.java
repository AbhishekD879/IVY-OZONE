package com.ladbrokescoral.cashout.service.updates;

import com.coral.bpp.api.model.bet.api.request.GetBetDetailRequest;
import com.coral.bpp.api.model.bet.api.response.oxi.base.Bet;
import com.ladbrokescoral.cashout.model.response.UpdateDto;
import com.ladbrokescoral.cashout.service.BppService;
import com.ladbrokescoral.cashout.util.Message;
import io.netty.util.NettyRuntime;
import java.io.IOException;
import java.time.Duration;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.concurrent.TimeoutException;
import java.util.function.Consumer;
import java.util.stream.Collectors;
import lombok.Builder;
import lombok.Getter;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Primary;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;
import reactor.core.Disposable;
import reactor.core.publisher.Flux;
import reactor.core.publisher.FluxSink;
import reactor.core.publisher.FluxSink.OverflowStrategy;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;
import reactor.util.function.Tuple2;

@Component
@Primary
public class AsyncBetDetailThrottledService
    implements AsyncBetDetailService, BufferedDisposable<BetDetailRequestCtx> {

  private static final int WINDOW_SIZE = 500;
  private final BetUpdatesTopic betUpdatesTopic;

  private final Disposable betDetailsDisposable;

  @Value("${betDetail.buffering.maxSize:5}")
  private int betDetailMaxSize;

  private Consumer<BetDetailRequestCtx> requestDemand;
  private FluxSink<BetDetailRequestCtx> sink;
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");
  private Message message;

  public AsyncBetDetailThrottledService(
      BppService bppService,
      BetUpdatesTopic betUpdatesTopic,
      @Value("${betDetail.buffering}") Duration bufferingTimespan,
      @Value("${cashout.scheduler.bet-detail.cpu.factor:1}") int cpuFactor,
      @Value("${bet-detail.buffer.overflow-strategy:BUFFER}") String overflowStrategy) {
    this.betUpdatesTopic = betUpdatesTopic;
    this.betDetailsDisposable =
        Flux.<BetDetailRequestCtx>create(
                sink -> {
                  this.requestDemand = sink::next;
                  this.sink = sink;
                },
                OverflowStrategy.valueOf(overflowStrategy))
            .publishOn(
                Schedulers.newParallel(
                    "Bet-Detail-Parallel", (NettyRuntime.availableProcessors() * cpuFactor)))
            .name("asyncGetBetDetailFlux")
            .groupBy(BetDetailRequestCtx::getUserId)
            .window(WINDOW_SIZE)
            .flatMap(
                w ->
                    w.flatMap(
                        g ->
                            g.bufferTimeout(betDetailMaxSize, bufferingTimespan)
                                .flatMap(
                                    reqs -> {
                                      MergeContext mergeCtx = mergeRequestsIntoOne(reqs);
                                      return Mono.zip(
                                              Mono.just(mergeCtx),
                                              bppService.getBetDetail(
                                                  mergeCtx.getMergedBetDetailRequest()))
                                          .onErrorMap(
                                              e ->
                                                  !(e instanceof IOException
                                                      || e instanceof TimeoutException),
                                              e -> {
                                                mergeCtx
                                                    .getTokensBeforeMerge()
                                                    .forEach(
                                                        token ->
                                                            betUpdatesTopic.sendBetUpdateError(
                                                                token, e));
                                                return e;
                                              })
                                          .onErrorResume(t -> Mono.empty());
                                    }),
                        WINDOW_SIZE),
                200)
            .doOnNext(this::sendBetDetails)
            .onErrorResume(
                t -> {
                  ASYNC_LOGGER.warn("error", t);
                  return Flux.empty();
                })
            .subscribe();
    message = new Message();
    message.setMessage(String.valueOf(bufferingTimespan));
    ASYNC_LOGGER.info("getBetDetail buffering time: {}", message);
  }

  private static MergeContext mergeRequestsIntoOne(List<BetDetailRequestCtx> requests) {
    Message message = new Message();
    String userName = requests.get(0).getUserId();
    Set<String> betIds =
        requests.stream()
            .map(BetDetailRequestCtx::getRequest)
            .flatMap(r -> r.getBetIds().stream())
            .collect(Collectors.toSet());
    message.setMessage(userName);
    ASYNC_LOGGER.info(
        "[{}] Merging {} requests. Collected betIds: {};", message, requests.size(), betIds.size());

    Comparator<BetDetailRequestCtx> requestCtxComparator =
        Comparator.comparing(BetDetailRequestCtx::getTimeToTokenExpirationLeft);

    Optional<String> newestToken =
        requests.stream()
            .sorted(requestCtxComparator.reversed())
            .map(BetDetailRequestCtx::getRequest)
            .map(GetBetDetailRequest::getToken)
            .findFirst();

    GetBetDetailRequest request =
        SelectionDataAwareUpdateProcessor.buildGetBetDetailRequest(
            newestToken.get(), new ArrayList<>(betIds));
    request.setTimestamp(requests.get(0).getRequest().getTimestamp());

    return MergeContext.builder()
        .userId(userName)
        .tokensBeforeMerge(
            requests.stream()
                .map(BetDetailRequestCtx::getRequest)
                .map(GetBetDetailRequest::getToken)
                .collect(Collectors.toSet()))
        .mergedBetDetailRequest(request)
        .timestamp(requests.get(0).getTimestamp())
        .build();
  }

  @Override
  @Async
  public void acceptBetDetailRequest(BetDetailRequestCtx requestCtx) {
    this.requestDemand.accept(requestCtx);
    ASYNC_LOGGER.info("Accepted request for betDetail: {}", requestCtx);
  }

  private List<String> sendBetDetails(Tuple2<MergeContext, List<Bet>> requestAndResponse) {
    MergeContext mergeCtx = requestAndResponse.getT1();
    List<Bet> bets = requestAndResponse.getT2();
    String userId = mergeCtx.getUserId();
    ASYNC_LOGGER.info("[{}] Going to send bet updates: {}", userId, bets);
    return bets.stream()
        .map(
            bet -> {
              UpdateDto betUpdate =
                  UpdateDto.builder()
                      .bet(bet)
                      .timestamp(
                          LocalDateTime.now(ZoneOffset.UTC).format(DateTimeFormatter.ISO_DATE_TIME))
                      .build();
              mergeCtx
                  .getTokensBeforeMerge()
                  .forEach(token -> betUpdatesTopic.sendBetUpdate(token, betUpdate));
              ASYNC_LOGGER.info(
                  "[{}] Sent betUpdate for betId={} in {} millis",
                  userId,
                  betUpdate.getBet().getBetId(),
                  mergeCtx.getTimestamp() != 0
                      ? calculateTimeElapsedSinceRequestCreated(mergeCtx)
                      : "?");
              return bet.getBetId();
            })
        .collect(Collectors.toList());
  }

  private long calculateTimeElapsedSinceRequestCreated(MergeContext mergeContext) {
    long requestTimestamp = mergeContext.getTimestamp();
    return System.currentTimeMillis() - requestTimestamp;
  }

  @Override
  public FluxSink<BetDetailRequestCtx> getSink() {
    return sink;
  }

  @Override
  public Disposable getDisposable() {
    return betDetailsDisposable;
  }

  @Builder
  @Getter
  private static class MergeContext {
    private final GetBetDetailRequest mergedBetDetailRequest;
    private final String userId;
    private final Set<String> tokensBeforeMerge;
    private final long timestamp;
  }
}
