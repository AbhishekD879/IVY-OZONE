package com.ladbrokescoral.oxygen.buildyourbetms.config;

import com.ladbrokescoral.oxygen.byb.banach.client.BanachClient;
import com.ladbrokescoral.oxygen.byb.banach.client.BanachClients;
import com.ladbrokescoral.oxygen.byb.banach.client.BanachOptions;
import com.ladbrokescoral.oxygen.byb.banach.client.PoolType;
import com.ladbrokescoral.oxygen.byb.banach.dto.internal.*;
import java.time.Clock;
import java.time.Duration;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.reactive.ReactorResourceFactory;
import reactor.core.publisher.Mono;

@Configuration
public class BanachWebClientConfig {
  @Value("${banach.url}")
  private String baseUrl;

  @Value("${banach.connectTimeout:1000}")
  private long connectTimeout;

  @Value("${banach.timeout:1000}")
  private long readTimeout;

  @Value("${banach.retries:-1}")
  private int retries;

  @Value("${banach.client.epoll:false}")
  private boolean useEpoll;

  @Value("${banach.client.log.level:SEVERE}")
  private String logLevel;

  private BanachClients banachClients(
      int poolSize,
      int noOfThreads,
      String poolName,
      String poolType,
      ReactorResourceFactory factory) {
    return BanachClients.builder()
        .baseUrl(baseUrl)
        .defaultOptions(
            BanachOptions.builder()
                .poolType(PoolType.valueOf(poolType))
                .factory(factory)
                .fixedPoolMaxConnections(poolSize)
                .fixedPoolAcquireTimeout(connectTimeout)
                .poolName(poolName)
                .threadPrefix(poolName)
                .timeoutDuration(Duration.ofMillis(readTimeout))
                .connectionTimeout(Duration.ofMillis(connectTimeout))
                .retriesAmount(retries)
                .useEpoll(useEpoll)
                .noOfThreads(noOfThreads)
                .logLevel(logLevel)
                .build())
        .build();
  }

  @Bean
  public ReactorResourceFactory resourceFactory() {
    ReactorResourceFactory factory = new ReactorResourceFactory();
    factory.setUseGlobalResources(false);
    return factory;
  }

  @Bean
  public BanachClient<Mono<LeaguesResponse>> leaguesClient(
      @Value("${banach.leagues.pool.size:100}") int poolSize,
      @Value("${banach.leagues.threads:20}") int noOfThreads,
      @Value("${banach.leagues.pool.type:FIXED}") String poolType,
      ReactorResourceFactory factory) {

    return banachClients(poolSize, noOfThreads, "banach-leagues", poolType, factory).leagues();
  }

  @Bean
  public BanachClient<Mono<MarketsResponse>> marketsClient(
      @Value("${banach.markets.pool.size:100}") int poolSize,
      @Value("${banach.markets.threads:20}") int noOfThreads,
      @Value("${banach.markets.pool.type:FIXED}") String poolType,
      ReactorResourceFactory factory) {
    return banachClients(poolSize, noOfThreads, "banach-markets", poolType, factory).markets();
  }

  @Bean
  public BanachClient<Mono<MarketsGroupedResponse>> marketsGroupedClient(
      @Value("${banach.markets-grouped.pool.size:100}") int poolSize,
      @Value("${banach.markets-grouped.threads:20}") int noOfThreads,
      @Value("${banach.markets-grouped.pool.type:FIXED}") String poolType,
      ReactorResourceFactory factory) {
    return banachClients(poolSize, noOfThreads, "banach-markets-grouped", poolType, factory)
        .marketsGrouped();
  }

  @Bean
  public BanachClient<Mono<EventResponse>> eventClient(
      @Value("${banach.event.pool.size:100}") int poolSize,
      @Value("${banach.event.threads:20}") int noOfThreads,
      @Value("${banach.event.pool.type:FIXED}") String poolType,
      ReactorResourceFactory factory) {
    return banachClients(poolSize, noOfThreads, "banach-event", poolType, factory).event();
  }

  @Bean
  public BanachClient<Mono<EventsResponse>> eventsClient(
      @Value("${banach.events.pool.size:100}") int poolSize,
      @Value("${banach.events.threads:20}") int noOfThreads,
      @Value("${banach.events.pool.type:FIXED}") String poolType,
      ReactorResourceFactory factory) {
    return banachClients(poolSize, noOfThreads, "banach-events", poolType, factory).events();
  }

  @Bean
  public BanachClient<Mono<SelectionsResponse>> selectionsClient(
      @Value("${banach.selection.pool.size:100}") int poolSize,
      @Value("${banach.selection.threads:40}") int noOfThreads,
      @Value("${banach.selection.pool.type:FIXED}") String poolType,
      ReactorResourceFactory factory) {
    return banachClients(poolSize, noOfThreads, "banach-selections", poolType, factory)
        .selections();
  }

  @Bean
  public BanachClient<Mono<PriceResponse>> priceClient(
      @Value("${banach.price.pool.size:500}") int poolSize,
      @Value("${banach.price.threads:100}") int noOfThreads,
      @Value("${banach.price.pool.type:FIXED}") String poolType,
      ReactorResourceFactory factory) {
    return banachClients(poolSize, noOfThreads, "banach-price", poolType, factory).price();
  }

  @Bean
  public BanachClient<Mono<PlayersResponse>> playersClient(
      @Value("${banach.players.pool.size:100}") int poolSize,
      @Value("${banach.players.threads:20}") int noOfThreads,
      @Value("${banach.players.pool.type:FIXED}") String poolType,
      ReactorResourceFactory factory) {
    return banachClients(poolSize, noOfThreads, "banach-players", poolType, factory).players();
  }

  @Bean
  public BanachClient<Mono<PlayerStatisticsResponse>> playerStatisticsClient(
      @Value("${banach.player-stats.pool.size:100}") int poolSize,
      @Value("${banach.player-stats.threads:20}") int noOfThreads,
      @Value("${banach.player-stats.pool.type:FIXED}") String poolType,
      ReactorResourceFactory factory) {
    return banachClients(poolSize, noOfThreads, "banach-player-stats", poolType, factory)
        .playerStatistics();
  }

  @Bean
  public BanachClient<Mono<StatisticValueRangeResponse>> statisticValueRangeClient(
      @Value("${banach.stats-value-range.pool.size:100}") int poolSize,
      @Value("${banach.stats-value-range.threads:20}") int noOfThreads,
      @Value("${banach.stats-value-range.pool.type:FIXED}") String poolType,
      ReactorResourceFactory factory) {
    return banachClients(poolSize, noOfThreads, "banach-stats-value-range", poolType, factory)
        .statisticValueRange();
  }

  @Bean
  public BanachClient<Mono<PlayerBanachStatsResponse>> playersStatsByOptaId(
      @Value("${banach.player-stats-opta.pool.size:100}") int poolSize,
      @Value("${banach.player-stats-opta.threads:20}") int noOfThreads,
      @Value("${banach.player-stats-opta.pool.type:FIXED}") String poolType,
      ReactorResourceFactory factory) {
    return banachClients(poolSize, noOfThreads, "banach-player-stats-opta", poolType, factory)
        .playerStatsByOptaId();
  }

  @Bean
  public Clock systemClock() {
    return Clock.systemUTC();
  }
}
