package com.gvc.oxygen.betreceipts.liveserv.updates;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Price;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.gvc.oxygen.betreceipts.entity.NextRace;
import com.gvc.oxygen.betreceipts.entity.NextRaceMap;
import com.gvc.oxygen.betreceipts.liveserv.domain.SelectionStatus;
import com.gvc.oxygen.betreceipts.service.EventService;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Component;

@Component
@Slf4j(topic = "testpostselection")
public class SelectionMessageApplier extends ChannelMessageApplier {

  private final ObjectMapper objectMapper;
  private final EventService eventService;

  private final LiveServService liveServService;

  public SelectionMessageApplier(
      ObjectMapper objectMapper, EventService eventService, @Lazy LiveServService liveServService) {
    super(objectMapper);
    this.objectMapper = objectMapper;
    this.eventService = eventService;
    this.liveServService = liveServService;
  }

  @Override
  public void applyUpdate(MessageEnvelope messageEnvelope) {
    Optional<SelectionStatus> selectionStatus =
        parseLiveUpdateData(messageEnvelope.getMessage().getJsonData(), SelectionStatus.class);

    if (selectionStatus.isPresent()) {
      log.info("selection update {}", selectionStatus.get());
      findAndUpdatePosts(selectionStatus.get(), messageEnvelope);
    }
  }

  private void findAndUpdatePosts(
      SelectionStatus selectionStatus, MessageEnvelope messageEnvelope) {
    try {
      Optional<NextRaceMap> metaEvent =
          eventService.getNextRaceMapById(String.valueOf(messageEnvelope.getEventId()));
      if (metaEvent.isPresent()) {
        NextRaceMap nextRaceMap = metaEvent.get();
        NextRace nextRace = objectMapper.readValue(nextRaceMap.getNextRace(), NextRace.class);
        updateOutcome(selectionStatus, messageEnvelope, nextRace);
        nextRaceMap.setNextRace(objectMapper.writeValueAsString(nextRace));
        eventService.saveNextRaceMap(nextRaceMap);
      } else {
        liveServService.unsubscribe(messageEnvelope.getChannel());
      }
    } catch (Exception ex) {
      log.error("error while applying outcome update", ex);
    }
  }

  private void updateOutcome(
      SelectionStatus selectionStatus, MessageEnvelope messageEnvelope, NextRace nextRace) {
    for (Children children : nextRace.getMarkets().get(0).getChildren()) {
      if (children.getOutcome().getLiveServChannels().contains(messageEnvelope.getChannel())) {
        Price price = children.getOutcome().getChildren().get(0).getPrice();
        price.setPriceNum(selectionStatus.getPriceNum());
        price.setPriceDen(selectionStatus.getPriceDen());
      }
    }
  }

  @Override
  protected String type() {
    return "sSELCN";
  }
}
