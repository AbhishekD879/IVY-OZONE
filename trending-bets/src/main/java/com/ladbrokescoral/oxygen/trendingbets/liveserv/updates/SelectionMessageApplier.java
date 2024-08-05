package com.ladbrokescoral.oxygen.trendingbets.liveserv.updates;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.trendingbets.liveserv.domain.SelectionStatus;
import com.ladbrokescoral.oxygen.trendingbets.service.PopularBetUpdateService;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class SelectionMessageApplier extends ChannelMessageApplier {

  public SelectionMessageApplier(
      ObjectMapper mapper,
      PopularBetUpdateService eventService,
      @Lazy LiveServService liveServService) {
    super(mapper, eventService, liveServService);
  }

  @Override
  public void applyUpdate(MessageEnvelope messageEnvelope) {
    Optional<SelectionStatus> selectionStatus =
        parseLiveUpdateData(messageEnvelope.getMessage().getJsonData(), SelectionStatus.class);

    if (selectionStatus.isPresent()
        && isValidChannel(messageEnvelope.getChannel())
        && !selectionStatus.get().isPriceBoost()) {
      log.info("selection update {}", selectionStatus.get());
      eventService.updateSelection(selectionStatus.get(), messageEnvelope.getChannel());
    }
    if (selectionStatus.isPresent() && selectionStatus.get().isPriceBoost()) {
      log.error("PRICE BOOST received :: {}", selectionStatus.get());
    }
  }

  @Override
  protected String type() {
    return "sSELCN";
  }
}
