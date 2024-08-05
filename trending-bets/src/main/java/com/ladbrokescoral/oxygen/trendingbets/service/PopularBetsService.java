package com.ladbrokescoral.oxygen.trendingbets.service;

import com.ladbrokescoral.oxygen.trendingbets.context.TrendingBetsContext;
import com.ladbrokescoral.oxygen.trendingbets.dto.PopularBets;
import com.ladbrokescoral.oxygen.trendingbets.dto.TrendingItem;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingEvent;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingPosition;
import com.ladbrokescoral.oxygen.trendingbets.siteserv.SiteServeService;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.locks.ReentrantLock;
import java.util.function.Predicate;
import java.util.stream.IntStream;
import lombok.Getter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.util.CollectionUtils;
import org.springframework.util.StringUtils;

public abstract class PopularBetsService {

  @Getter
  @Value("${trendingBets.frontend}")
  protected String frontend;

  protected final LiveUpdatesService liveUpdatesService;

  protected final SiteServeService siteServeService;

  private String[] filterMarketDrilldownTagNames;
  private String[] filterEventDrilldownTagNames;

  protected PopularBetsService(
      LiveUpdatesService liveUpdatesService,
      SiteServeService siteServeService,
      String[] filterMarketDrilldownTagNames,
      String[] filterEventDrilldownTagNames) {
    this.liveUpdatesService = liveUpdatesService;
    this.siteServeService = siteServeService;
    this.filterMarketDrilldownTagNames = filterMarketDrilldownTagNames;
    this.filterEventDrilldownTagNames = filterEventDrilldownTagNames;
  }

  public TrendingPosition populateTrendingPosition(TrendingItem item) {
    TrendingPosition trendingPosition = new TrendingPosition();
    trendingPosition.setRank(item.getRank());
    trendingPosition.setNBets(item.getNBets());
    trendingPosition.setEvent(getTrendingSelection(item));
    return trendingPosition;
  }

  private static final int CONCURRENCY_LEVEL = 10;

  private static ReentrantLock[] locks = new ReentrantLock[CONCURRENCY_LEVEL];

  static {
    IntStream.range(0, CONCURRENCY_LEVEL).forEach((int i) -> locks[i] = new ReentrantLock());
  }

  /**
   * Retrieves the TrendingSelection from TrendingBetsContext if an entry is already present for the
   * given combination of event/market/selection. Create new TrendingSelection if not present
   * already.
   *
   * @param item
   * @return
   */
  public TrendingEvent getTrendingSelection(TrendingItem item) {
    if (CollectionUtils.isEmpty(
        TrendingBetsContext.getSelectionByBetsType(getBetType())
            .get(item.getSelectionLivesChannel()))) {
      ReentrantLock lock =
          locks[
              Integer.parseInt(
                  item.getSelectionId().substring(item.getSelectionId().length() - 1))];
      lock.lock();
      if (CollectionUtils.isEmpty(
          TrendingBetsContext.getSelectionByBetsType(getBetType())
              .get(item.getSelectionLivesChannel()))) {
        TrendingBetsContext.updateOrSaveLivesChannels(item.getTrendingEvent(), getBetType());
      }
      lock.unlock();
    }
    return TrendingBetsContext.getSelectionByBetsType(getBetType())
        .get(item.getSelectionLivesChannel())
        .get(0);
  }

  protected abstract PopularBets getBetType();

  protected Predicate<TrendingItem> filterTrendingItem() {
    return (TrendingItem item) -> {
      String eventTagName = item.getTrendingEvent().getDrilldownTagNames();
      String marketTagName = item.getTrendingEvent().getMarkets().get(0).getDrilldownTagNames();
      return !(existsDrillDownTagName(eventTagName, filterEventDrilldownTagNames)
          || existsDrillDownTagName(marketTagName, filterMarketDrilldownTagNames));
    };
  }

  private boolean existsDrillDownTagName(String tagName, String[] restrictedTagNames) {
    if (StringUtils.hasText(tagName) && restrictedTagNames != null) {
      return Arrays.stream(restrictedTagNames).anyMatch(tagName::contains);
    }
    return false;
  }

  protected List<TrendingItem> enhanceTrendingBets(List<TrendingItem> trendingItems) {
    return trendingItems.stream().filter(filterTrendingItem()).toList();
  }
}
