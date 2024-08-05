package com.ladbrokescoral.oxygen.betpackmp.kafka;

import com.coral.bpp.api.model.bet.api.response.freebetoffer.FreebetOffer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

/*
  This class is responsible to send messages to live updates topic
*/
@Component
public class KafkaBetPacksPublisher extends AbstractKafkaPublisher {

  public KafkaBetPacksPublisher(
      KafkaTemplate<String, FreebetOffer> kafkaTemplate,
      @Value("${topic.bet-pack-live-updates}") String topic) {
    super(kafkaTemplate, topic);
  }
}
