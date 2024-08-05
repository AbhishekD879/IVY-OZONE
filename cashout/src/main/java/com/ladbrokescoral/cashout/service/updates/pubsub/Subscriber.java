package com.ladbrokescoral.cashout.service.updates.pubsub;

import com.ladbrokescoral.cashout.model.safbaf.Entity;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import org.springframework.messaging.Message;
import org.springframework.messaging.MessageHandler;

@Data
@RequiredArgsConstructor
public class Subscriber {
  private final String subscriberId;
  private final String token;
  private final MessageHandler handler;

  public void notify(Message<Entity> entity) {
    handler.handleMessage(entity);
  }
}
