package com.coral.oxygen.middleware.ms.liveserv.impl;

import com.coral.oxygen.middleware.ms.liveserv.exceptions.ServiceException;
import com.coral.oxygen.middleware.ms.liveserv.model.ChannelType;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import java.util.Collections;
import java.util.List;
import java.util.Optional;

/** Created by azayats on 08.05.17. */
public class SiteServEventIdResolver extends BaseEventIdResolver implements EventIdResolver {

  private final SiteServerApi ssApi;

  public SiteServEventIdResolver(SiteServerApi ssApi) {
    this.ssApi = ssApi;
  }

  @Override
  protected long resolve(ChannelType type, long id) throws ServiceException {
    switch (type) {
      case sEVMKT:
      case SEVMKT:
        return getEventIdByMarketId(id);
      case sSELCN:
      case SSELCN:
      case sPRICE:
        return getEventIdByOutcomeId(id);
      default:
        return super.resolve(type, id);
    }
  }

  private long getEventIdByOutcomeId(long outcomeId) throws ServiceException {
    Optional<List<Event>> eventsOptional =
        ssApi.getEventToOutcomeForOutcome(
            Collections.singletonList(String.valueOf(outcomeId)),
            (SimpleFilter) new SimpleFilter.SimpleFilterBuilder().build(),
            Collections.emptyList());
    if (!eventsOptional.isPresent()) {
      throw new ServiceException(String.format("Event for outcome %d not found.", outcomeId));
    }
    List<Event> events = eventsOptional.get();
    if (events.isEmpty()) {
      throw new ServiceException(String.format("Event for outcome %d not found.", outcomeId));
    }
    try {
      return Long.parseLong(events.get(0).getId());
    } catch (Exception e) {
      throw new ServiceException(
          String.format("Error parsing event id %s", events.get(0).getId()), e);
    }
  }

  private long getEventIdByMarketId(long marketId) throws ServiceException {
    Optional<List<Market>> eventToOutcomeForMarket =
        ssApi.getEventToOutcomeForMarket(String.valueOf(marketId), false, true);
    if (!eventToOutcomeForMarket.isPresent()) {
      throw new ServiceException(String.format("Event for market %d not found.", marketId));
    }
    List<Market> markets = eventToOutcomeForMarket.get();
    if (markets.isEmpty()) {
      throw new ServiceException(String.format("Event for market %d not found.", marketId));
    }
    try {
      return Long.parseLong(markets.get(0).getEventId());
    } catch (Exception e) {
      throw new ServiceException(
          String.format("Error parsing event id %s", markets.get(0).getEventId()), e);
    }
  }
}
