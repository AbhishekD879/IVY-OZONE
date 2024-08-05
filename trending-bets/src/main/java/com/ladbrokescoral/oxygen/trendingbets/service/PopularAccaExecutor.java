package com.ladbrokescoral.oxygen.trendingbets.service;

import com.ladbrokescoral.oxygen.trendingbets.context.PopularAccaContext;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingPosition;
import com.ladbrokescoral.oxygen.trendingbets.util.TrendingBetsUtil;
import java.util.Optional;
import java.util.Set;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.stream.IntStream;
import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.concurrent.CustomizableThreadFactory;
import org.springframework.stereotype.Component;
import org.springframework.util.CollectionUtils;

@Slf4j
@Component
public class PopularAccaExecutor {

  private final ExecutorService executor;

  private String[] toBeFilteredMarkets;

  private String[] toBeFilteredEvents;

  private String[] toBeFilteredTemplateMarkets;

  private static final Integer MAX_THREADS = 1;

  @Autowired
  public PopularAccaExecutor(
      @Value("${popularacca.filter.market.drilldownTagNames}") String[] toBeFilteredMarkets,
      @Value("${popularacca.filter.event.drilldownTagNames}") String[] toBeFilteredEvents,
      @Value("${popularacca.filter.market.templateMarketNames}")
          String[] toBeFilteredTemplateMarkets) {
    executor =
        Executors.newFixedThreadPool(
            MAX_THREADS, new CustomizableThreadFactory("Acca-Events-Executor-"));
    this.toBeFilteredMarkets = toBeFilteredMarkets;
    this.toBeFilteredEvents = toBeFilteredEvents;
    this.toBeFilteredTemplateMarkets = toBeFilteredTemplateMarkets;
  }

  @PostConstruct
  public void runUploadWorkers() {
    if (!executor.isShutdown()) {
      IntStream.range(0, 1).forEach(w -> executor.execute(this::deliverIndefinitely));
    }
  }

  @PreDestroy
  public void shutdown() {
    executor.shutdownNow();
  }

  private void deliverIndefinitely() {
    while (!Thread.currentThread().isInterrupted()) {
      try {
        process(PopularAccaContext.getItemToExecute());
      } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
        runUploadWorkers();
      }
    }
  }

  public void process(Set<TrendingPosition> event) {
    if (CollectionUtils.isEmpty(event)) return;
    event.stream()
        .filter(
            position ->
                !TrendingBetsUtil.checkDrillDownTagsMatch(
                        position.getEvent(), toBeFilteredEvents, toBeFilteredMarkets)
                    && TrendingBetsUtil.checkWhetherMarketCanFormAnAccaOrNot(position.getEvent())
                    && !TrendingBetsUtil.checkTemplateMarketNames(
                        position.getEvent(), toBeFilteredTemplateMarkets))
        .forEach(this::processPopularAcca);
  }

  private void processPopularAcca(TrendingPosition trendingPosition) {

    Optional.ofNullable(
            PopularAccaContext.getSelectionAccas()
                .get(trendingPosition.getEvent().getSelectionId()))
        .ifPresentOrElse(
            (TrendingPosition exTrendingPosition) -> {
              if (exTrendingPosition.getNBets() < trendingPosition.getNBets()) {
                updatePopularAccaCache(trendingPosition);
              }
            },
            () -> updatePopularAccaCache(trendingPosition));
  }

  private void updatePopularAccaCache(TrendingPosition trendingPosition) {
    PopularAccaContext.updateSelectionAcca(trendingPosition);
    PopularAccaContext.updateLeagueAcca(trendingPosition);
    PopularAccaContext.updateEventAcca(trendingPosition);
  }
}
