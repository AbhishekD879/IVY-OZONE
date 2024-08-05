package com.ladbrokescoral.oxygen.trendingbets.liveserv.updates;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.trendingbets.liveserv.domain.MarketStatus;
import com.ladbrokescoral.oxygen.trendingbets.service.PopularBetUpdateService;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class MarketMessageApplier extends ChannelMessageApplier {

  public MarketMessageApplier(
      ObjectMapper mapper,
      PopularBetUpdateService eventService,
      @Lazy LiveServService liveServService) {
    super(mapper, eventService, liveServService);
  }

  @Override
  public void applyUpdate(MessageEnvelope messageEnvelope) {
    Optional<MarketStatus> marketStatus =
        parseLiveUpdateData(messageEnvelope.getMessage().getJsonData(), MarketStatus.class);

    if (marketStatus.isPresent() && isValidChannel(messageEnvelope.getChannel())) {
      log.info("Market update {}", marketStatus.get());
      eventService.updateMarket(marketStatus.get(), messageEnvelope.getChannel());
    }
  }

  @Override
  protected String type() {
    return "sEVMKT";
  }
}
