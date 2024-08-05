package com.ladbrokescoral.oxygen.trendingbets.siteserv;

import com.egalacoral.spark.siteserver.api.BinaryOperation;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApiAsync;
import com.egalacoral.spark.siteserver.api.UnaryOperation;
import com.ladbrokescoral.oxygen.trendingbets.context.TrendingBetsContext;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingEvent;
import com.ladbrokescoral.oxygen.trendingbets.siteserv.converter.EventToTrendingEventConverter;
import com.ladbrokescoral.oxygen.trendingbets.siteserv.converter.MarketToOutputMarketConverter;
import com.ladbrokescoral.oxygen.trendingbets.siteserv.converter.OutcomeToOutputOutcomeConverter;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

@Service
@Slf4j
public class TrendingBetsSiteServImpl extends SiteServeServiceImpl {

  private String marketDrillDownTagNames;

  private String eventDrillDownTagNames;

  public TrendingBetsSiteServImpl(
      SiteServerApiAsync siteServerApiAsync,
      EventToTrendingEventConverter eventToTrendingEventConverter,
      MarketToOutputMarketConverter marketToOutputMarketConverter,
      OutcomeToOutputOutcomeConverter outcomeToOutputOutcomeConverter,
      @Value("${popularbets.filter.market.drilldownTagNames}") String marketDrillDownTagNames,
      @Value("${popularbets.filter.event.drilldownTagNames}") String eventDrillDownTagNames) {
    super(
        siteServerApiAsync,
        eventToTrendingEventConverter,
        marketToOutputMarketConverter,
        outcomeToOutputOutcomeConverter);
    this.eventDrillDownTagNames = eventDrillDownTagNames;
    this.marketDrillDownTagNames = marketDrillDownTagNames;
  }

  /**
   * Checks if TrendingEvent is exist in TrendingBetsContext with given selectionId and returns
   * TrendingEvent.
   *
   * @param selectionId
   * @return
   */
  public List<TrendingEvent> getTrendingSelection(String selectionId) {
    return TrendingBetsContext.getSubscribedChannels().keySet().stream()
        .filter(channel -> channel.contains(selectionId))
        .findFirst()
        .map(
            channel ->
                Optional.ofNullable(TrendingBetsContext.getPopularSelections().get(channel))
                    .orElse(
                        Optional.ofNullable(
                                TrendingBetsContext.getPersonalizedSelections().get(channel))
                            .map(
                                (List<TrendingEvent> events) -> {
                                  TrendingBetsContext.getPopularSelections().put(channel, events);
                                  return events;
                                })
                            .orElse(Collections.emptyList())))
        .orElse(Collections.emptyList());
  }

  @Override
  protected SimpleFilter getSimpleFilter() {
    SimpleFilter.SimpleFilterBuilder simpleFilterBuilder = new SimpleFilter.SimpleFilterBuilder();
    if (StringUtils.hasText(marketDrillDownTagNames)) {
      simpleFilterBuilder.addField(
          "market.drilldownTagNames:"
              + BinaryOperation.notIntersects
              + ":"
              + marketDrillDownTagNames);
    }
    if (StringUtils.hasText(eventDrillDownTagNames)) {
      simpleFilterBuilder.addField(
          "event.drilldownTagNames:"
              + BinaryOperation.notIntersects
              + ":"
              + eventDrillDownTagNames);
    }
    simpleFilterBuilder.addUnaryOperation("event.liveServChannels", UnaryOperation.isNotEmpty);
    return (SimpleFilter) simpleFilterBuilder.build();
  }
}
