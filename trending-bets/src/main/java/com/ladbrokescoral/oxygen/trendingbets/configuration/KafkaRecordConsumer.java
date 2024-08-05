package com.ladbrokescoral.oxygen.trendingbets.configuration;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.trendingbets.dto.TrendingBets;
import com.ladbrokescoral.oxygen.trendingbets.service.TrendingBetsService;
import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import kafka.consumer.ConsumerIterator;
import kafka.consumer.KafkaStream;
import kafka.javaapi.consumer.ConsumerConnector;
import kafka.message.MessageAndMetadata;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.util.StringUtils;

@Configuration
@Slf4j
@RequiredArgsConstructor
@Profile("!TEST")
public class KafkaRecordConsumer implements CommandLineRunner {

  private final ConsumerConnector consumerConnector;

  private final TrendingBetsService trendingBetsService;

  private final ObjectMapper objectMapper;

  private ExecutorService executor;

  @Value("${trendingBets.kafka.topic.name}")
  private String kafkaTopicName;

  @Override
  public void run(String... args) {
    Map<String, Integer> topicCountMap = new HashMap<>();
    topicCountMap.put(kafkaTopicName, 1);
    Map<String, List<KafkaStream<byte[], byte[]>>> consumerMap =
        consumerConnector.createMessageStreams(topicCountMap);
    List<KafkaStream<byte[], byte[]>> streams = consumerMap.get(kafkaTopicName);
    executor = Executors.newFixedThreadPool(1);
    streams.forEach(stream -> executor.execute(() -> processTrendingBets(stream)));
  }

  private void processTrendingBets(KafkaStream<byte[], byte[]> stream) {
    ConsumerIterator<byte[], byte[]> it = stream.iterator();

    while (it.hasNext()) {
      processTrendingBets(it.next());
    }
  }

  private void processTrendingBets(MessageAndMetadata<byte[], byte[]> consumerRecord) {
    if (StringUtils.hasText(new String(consumerRecord.message()))) {
      try {
        long startTime = System.currentTimeMillis();
        TrendingBets trendingBets =
            objectMapper.readValue(consumerRecord.message(), TrendingBets.class);
        trendingBetsService
            .processTrendingBets(trendingBets)
            .subscribe(
                s ->
                    log.info(
                        "processing Trending bets {} took {} millis",
                        s.getChannelId(),
                        (System.currentTimeMillis() - startTime)));
      } catch (IOException | RuntimeException e) {
        log.error("Error processing trending bets ::", e);
      }
    }
  }
}
