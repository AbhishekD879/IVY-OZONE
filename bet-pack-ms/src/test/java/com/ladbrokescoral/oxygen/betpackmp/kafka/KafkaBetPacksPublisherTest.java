package com.ladbrokescoral.oxygen.betpackmp.kafka;

import com.coral.bpp.api.model.bet.api.response.freebetoffer.FreebetOffer;
import org.assertj.core.api.WithAssertions;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.kafka.core.KafkaTemplate;

@ExtendWith(MockitoExtension.class)
class KafkaBetPacksPublisherTest implements WithAssertions {

  @Mock private KafkaTemplate<String, FreebetOffer> kafkaTemplate;

  @InjectMocks private KafkaBetPacksPublisher kafkaBetPacksPublisher;

  @Test
  void kafkaBetPacksPublisherTest() {
    kafkaBetPacksPublisher = new KafkaBetPacksPublisher(kafkaTemplate, "kafka_topic");
    Assertions.assertNotNull(kafkaBetPacksPublisher);
  }
}
