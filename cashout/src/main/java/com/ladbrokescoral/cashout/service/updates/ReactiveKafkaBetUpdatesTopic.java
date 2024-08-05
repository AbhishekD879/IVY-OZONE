package com.ladbrokescoral.cashout.service.updates;

import com.ladbrokescoral.cashout.config.InternalKafkaTopics;
import com.ladbrokescoral.cashout.model.response.UpdateDto;
import java.util.Objects;
import lombok.RequiredArgsConstructor;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.kafka.core.reactive.ReactiveKafkaProducerTemplate;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class ReactiveKafkaBetUpdatesTopic implements BetUpdatesTopic {
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");
  private final ReactiveKafkaProducerTemplate<String, UpdateDto>
      betUpdateReactiveKafkaProducerTemplate;
  private final ReactiveKafkaProducerTemplate<String, Throwable>
      betUpdatesErrorReactiveKafkaProducerTemplate;

  @Override
  public void sendBetUpdate(UpdateDto betUpdate) {
    Objects.requireNonNull(betUpdate);
    Objects.requireNonNull(betUpdate.getBet());
    Objects.requireNonNull(betUpdate.getBet().getBetId());

    betUpdateReactiveKafkaProducerTemplate
        .send(
            InternalKafkaTopics.BET_UDPATES.getTopicName(),
            betUpdate.getBet().getBetId(),
            betUpdate)
        .subscribe();
  }

  @Override
  public void sendBetUpdate(String key, UpdateDto betUpdate) {
    betUpdateReactiveKafkaProducerTemplate
        .send(InternalKafkaTopics.BET_UDPATES.getTopicName(), key, betUpdate)
        .subscribe();
  }

  @Override
  public void sendBetUpdateError(String key, Throwable ex) {
    betUpdatesErrorReactiveKafkaProducerTemplate
        .send(InternalKafkaTopics.BET_UPDATES_ERRORS.getTopicName(), key, ex)
        .subscribe();

    ASYNC_LOGGER.info("Sent betUpdateError - {}", ex.getClass().getSimpleName());
  }
}
