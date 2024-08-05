package com.ladbrokescoral.oxygen.trendingbets.siteserv;

import com.egalacoral.spark.siteserver.api.SiteServerApiAsync;
import com.ladbrokescoral.oxygen.trendingbets.context.TrendingBetsContext;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingEvent;
import com.ladbrokescoral.oxygen.trendingbets.siteserv.converter.EventToTrendingEventConverter;
import com.ladbrokescoral.oxygen.trendingbets.siteserv.converter.MarketToOutputMarketConverter;
import com.ladbrokescoral.oxygen.trendingbets.siteserv.converter.OutcomeToOutputOutcomeConverter;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class PersonalizedBetsSiteServImpl extends SiteServeServiceImpl {

  public PersonalizedBetsSiteServImpl(
      SiteServerApiAsync siteServerApiAsync,
      EventToTrendingEventConverter eventToTrendingEventConverter,
      MarketToOutputMarketConverter marketToOutputMarketConverter,
      OutcomeToOutputOutcomeConverter outcomeToOutputOutcomeConverter) {
    super(
        siteServerApiAsync,
        eventToTrendingEventConverter,
        marketToOutputMarketConverter,
        outcomeToOutputOutcomeConverter);
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
                Optional.ofNullable(TrendingBetsContext.getPersonalizedSelections().get(channel))
                    .orElse(
                        Optional.ofNullable(TrendingBetsContext.getPopularSelections().get(channel))
                            .map(
                                (List<TrendingEvent> events) -> {
                                  TrendingBetsContext.getPersonalizedSelections()
                                      .put(channel, events);
                                  return events;
                                })
                            .orElse(Collections.emptyList())))
        .orElse(Collections.emptyList());
  }
}
