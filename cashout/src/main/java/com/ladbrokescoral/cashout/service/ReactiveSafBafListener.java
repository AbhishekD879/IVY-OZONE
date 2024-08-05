package com.ladbrokescoral.cashout.service;

import com.ladbrokescoral.cashout.model.safbaf.Entity;
import com.ladbrokescoral.cashout.model.safbaf.Meta;
import com.ladbrokescoral.cashout.model.safbaf.betslip.Betslip;
import com.newrelic.api.agent.NewRelic;
import java.util.Optional;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.CommandLineRunner;
import org.springframework.kafka.core.reactive.ReactiveKafkaConsumerTemplate;
import org.springframework.messaging.SubscribableChannel;
import org.springframework.messaging.support.GenericMessage;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;

@Service
public class ReactiveSafBafListener implements CommandLineRunner {

  private static final String CUSTOM_SAFDELAY_METRIC = "Custom/SAFDelay";

  @Qualifier("safUpdatesListenerTemplate")
  private final ReactiveKafkaConsumerTemplate<String, String> safUpdatesListenerTemplate;

  @Qualifier("bafUpdatesListenerTemplate")
  private final ReactiveKafkaConsumerTemplate<String, String> bafUpdatesListenerTemplate;

  private final SubscribableChannel messageChannel;
  private final TopicContentConverter converter;
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  @Autowired
  public ReactiveSafBafListener(
      ReactiveKafkaConsumerTemplate<String, String> safUpdatesListenerTemplate,
      ReactiveKafkaConsumerTemplate<String, String> bafUpdatesListenerTemplate,
      SubscribableChannel messageChannel,
      TopicContentConverter converter) {
    this.safUpdatesListenerTemplate = safUpdatesListenerTemplate;
    this.bafUpdatesListenerTemplate = bafUpdatesListenerTemplate;
    this.messageChannel = messageChannel;
    this.converter = converter;
  }

  @Override
  public void run(String... args) throws Exception {
    consumeSafUpdates().subscribe();
    consumeBafUpdates().subscribe();
  }

  public Flux<ConsumerRecord<String, String>> consumeSafUpdates() {
    return safUpdatesListenerTemplate
        .receiveAutoAck()
        .doOnNext(this::processSafUpdate)
        .doOnError(
            throwable ->
                ASYNC_LOGGER.error("issue while consuming SAF Update: {}", throwable.getMessage()));
  }

  public void processSafUpdate(ConsumerRecord<String, String> consumerRecord) {
    Long receivedTimestamp = consumerRecord.timestamp();
    String sportbookUpdate = consumerRecord.value();
    String topicName = consumerRecord.topic();
    if (sportbookUpdate == null) {
      ASYNC_LOGGER.warn("Received null from {}", topicName);
      return;
    }
    ASYNC_LOGGER.debug("received from {} = {}", topicName, sportbookUpdate);

    Optional<Entity> entity = converter.convertSafUpdateToPojo(sportbookUpdate);

    if (!entity.isPresent()) {
      ASYNC_LOGGER.warn("Ignored entity other than event/market/selection");
      return;
    } else if (!"update".equals(entity.get().getMeta().getOperation())) {
      ASYNC_LOGGER.trace("Ignoring SAF because it's not update");
      return;
    }
    processIfNotNull(entity.get(), topicName, receivedTimestamp);
  }

  public <T extends Entity> void processIfNotNull(
      T update, String topicName, Long receivedTimestamp) {
    if (update == null) {
      ASYNC_LOGGER.warn("Received null from {}", topicName);
    } else {
      recordDelay(receivedTimestamp, update);
      messageChannel.send(new GenericMessage<>(update), 0);
    }
  }

  private void recordDelay(Long ts, Entity entity) {
    Optional.ofNullable(entity.getMeta())
        .map(Meta::getMessageTimestamp)
        .map(Long::parseLong)
        .ifPresent(
            (Long msgTimestamp) -> {
              long delay = ts - msgTimestamp;
              NewRelic.recordMetric(CUSTOM_SAFDELAY_METRIC, delay);
            });
  }

  public Flux<ConsumerRecord<String, String>> consumeBafUpdates() {
    return bafUpdatesListenerTemplate
        .receiveAutoAck()
        .doOnNext(this::processBafUpdate)
        .doOnError(
            throwable ->
                ASYNC_LOGGER.error("issue while consuming BAF Update: {}", throwable.getMessage()));
  }

  public void processBafUpdate(ConsumerRecord<String, String> consumerRecord) {
    String betslipUpdate = consumerRecord.value();
    String topicName = consumerRecord.topic();
    Long receivedTimestamp = consumerRecord.timestamp();
    Optional<Betslip> betslip = converter.convertBetslipUpdateToPojo(betslipUpdate);
    betslip.ifPresent(b -> ASYNC_LOGGER.debug("received from {} = {}", topicName, betslipUpdate));
    processIfNotNull(betslip.orElse(null), topicName, receivedTimestamp);
  }
}
