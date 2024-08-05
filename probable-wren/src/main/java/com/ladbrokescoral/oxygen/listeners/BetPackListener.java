package com.ladbrokescoral.oxygen.listeners;

import com.corundumstudio.socketio.SocketIOServer;
import com.ladbrokescoral.oxygen.model.FreebetOffer;
import java.util.Objects;
import lombok.extern.slf4j.Slf4j;
import lombok.val;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Configuration;

@ConditionalOnProperty(prefix = "bet-bundle", value = "enabled", havingValue = "true")
@Configuration
@Slf4j
public class BetPackListener {
  private final SocketIOServer socketIOServer;

  public BetPackListener(SocketIOServer socketIOServer) {
    this.socketIOServer = socketIOServer;
  }

  @org.springframework.kafka.annotation.KafkaListener(
      topics = "${topic.bet-pack-live-updates}",
      containerFactory = "kafkaBetPacksListenerContainerFactory",
      autoStartup = "${bet-bundle.enabled:false}")
  public void consumeBetPack(ConsumerRecord<String, FreebetOffer> freeBetOffer) {
    FreebetOffer messageObject = freeBetOffer.value();
    if (Objects.nonNull(messageObject)) {
      try {
        log.info("Bet Pack message received from Kafka: {}", messageObject);
        val betPackId = messageObject.getFreebetOfferId();
        socketIOServer.getRoomOperations(betPackId).sendEvent(betPackId, messageObject);
      } catch (Exception e) {
        log.error("Bet Pack message received from Kafka: {} {}", e.getMessage(), e);
      }
    }
  }
}
