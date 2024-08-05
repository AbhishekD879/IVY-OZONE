package com.ladbrokescoral.oxygen.betpackmp.kafka;

import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.betpackmp.configuration.JsonConfiguration;
import com.ladbrokescoral.oxygen.betpackmp.model.*;
import com.ladbrokescoral.oxygen.betpackmp.service.BetPackService;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.common.record.TimestampType;
import org.assertj.core.api.WithAssertions;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class DfKafkaConsumerTest implements WithAssertions {

  @Mock private BetPackService betPackService;

  @InjectMocks private DfKafkaConsumer dfKafkaConsumer;

  @BeforeEach
  public void init() {
    dfKafkaConsumer = new DfKafkaConsumer(betPackService);
  }

  @Test
  void consumePAFeedTest() {
    ConsumerRecord<String, PafExtractorPromotion> consumerRecord = getRecord();
    dfKafkaConsumer.consumePAFeed(consumerRecord);
    verify(betPackService, times(1))
        .processBetPacks(consumerRecord.value().getPayload().getCampaignRef());
    Assertions.assertDoesNotThrow(() -> dfKafkaConsumer.consumePAFeed(consumerRecord));
  }

  @Test
  void consumePAFeedTestFailure() {
    ConsumerRecord<String, PafExtractorPromotion> consumerRecord = getRecord();
    verify(betPackService, times(0))
        .processBetPacks(consumerRecord.value().getPayload().getCampaignRef());
    Assertions.assertDoesNotThrow(() -> dfKafkaConsumer.consumePAFeed(consumerRecord));
  }

  private ConsumerRecord<String, PafExtractorPromotion> getRecord() {
    String promotionStr =
        "{\n"
            + "  \"id\": \"8698698\",\n"
            + "  \"brand\": \"coral\",\n"
            + "  \"customerRef\": \"7687d74s68sdf8\",\n"
            + "  \"offerName\": \"football\",\n"
            + "  \"amount\": \"2000\",\n"
            + "  \"status\": \"active\",\n"
            + "  \"campaignRef\": \"campaign_ref\"\n"
            + "}";
    Promotion promotion =
        new JsonConfiguration().gsonInstance().fromJson(promotionStr, Promotion.class);
    PafExtractorPromotion extractorPromotion = new PafExtractorPromotion();
    extractorPromotion.setPayload(promotion);
    extractorPromotion.getPayload().setStatus("Issued");
    Metadata metadata = new Metadata(new EventSource(), new EventType());
    extractorPromotion.setMetadata(metadata);
    return new ConsumerRecord<>(
        "test.scoreboards.1",
        0,
        0,
        123,
        TimestampType.NO_TIMESTAMP_TYPE,
        123,
        1,
        1,
        "someKey",
        extractorPromotion);
  }
}
