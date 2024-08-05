package com.ladbrokescoral.cashout.service;

import com.ladbrokescoral.cashout.model.safbaf.Entity;
import com.ladbrokescoral.cashout.model.safbaf.Event;
import com.ladbrokescoral.cashout.model.safbaf.Market;
import com.ladbrokescoral.cashout.model.safbaf.Selection;
import com.ladbrokescoral.cashout.repository.EntityStatus;
import com.ladbrokescoral.cashout.repository.SelectionHierarchyStatusRepository;
import com.ladbrokescoral.cashout.service.masterslave.ExecuteOnMaster;
import com.ladbrokescoral.cashout.service.updates.pubsub.UpdateMessageHandler;
import lombok.RequiredArgsConstructor;
import org.springframework.messaging.Message;
import org.springframework.stereotype.Service;

/**
 * Populates selection price repository and event/market/selection statuses repositories based on
 * sportsbook updates (event/market/selection) received from SAF Kafka
 */
@Service
@RequiredArgsConstructor
public class SelectionHierarchyStatusToRepositoryHandler
    implements UpdateMessageHandler<Message<?>> {
  private final SelectionHierarchyStatusRepository statusRepository;

  @Override
  @ExecuteOnMaster
  public void handleUpdateMessage(Message<?> message) {
    Entity msg = (Entity) message.getPayload();
    if (msg instanceof Selection) {
      Selection selection = (Selection) msg;
      if (selection.statusChanged()) {
        statusRepository.updateSelectionStatus(
            new EntityStatus(selection.getSelectionKey(), selection.isActivated()));
      }
    } else if (msg instanceof Event) {
      Event event = (Event) msg;
      if (event.statusChanged()) {
        statusRepository.updateEventStatus(
            new EntityStatus(event.getEventKey(), event.isActivated()));
      }
    } else if (msg instanceof Market) {
      Market market = (Market) msg;
      if (market.statusChanged()) {
        statusRepository.updateMarketStatus(
            new EntityStatus(market.getMarketKey(), market.isActivated()));
      }
    }
  }
}
