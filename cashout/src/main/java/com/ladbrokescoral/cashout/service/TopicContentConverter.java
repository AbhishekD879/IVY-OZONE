package com.ladbrokescoral.cashout.service;

import com.ladbrokescoral.cashout.model.safbaf.Entity;
import com.ladbrokescoral.cashout.model.safbaf.KafkaSafUpdate;
import com.ladbrokescoral.cashout.model.safbaf.betslip.Betslip;
import com.ladbrokescoral.cashout.util.JsonUtil;
import java.util.Optional;
import org.springframework.stereotype.Service;

@Service
class TopicContentConverter {

  public Optional<Entity> convertSafUpdateToPojo(String message) {
    KafkaSafUpdate kafkaSafUpdate = JsonUtil.fromJson(message, KafkaSafUpdate.class);
    Optional<Entity> event = Optional.ofNullable(kafkaSafUpdate.getEvent());
    Optional<Entity> market = Optional.ofNullable(kafkaSafUpdate.getMarket());
    Optional<Entity> selection = Optional.ofNullable(kafkaSafUpdate.getSelection());
    if (event.isPresent()) {
      return event;
    } else if (market.isPresent()) {
      return market;
    } else if (selection.isPresent()) {
      return selection;
    }
    return Optional.empty();
  }

  public Optional<Betslip> convertBetslipUpdateToPojo(String message) {
    return Optional.ofNullable(JsonUtil.fromJson(message, Betslip.class));
  }
}
