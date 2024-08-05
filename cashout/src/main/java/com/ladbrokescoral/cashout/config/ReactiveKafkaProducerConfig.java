package com.ladbrokescoral.cashout.config;

import com.ladbrokescoral.cashout.api.client.entity.request.CashoutRequest;
import com.ladbrokescoral.cashout.model.response.UpdateDto;
import com.ladbrokescoral.cashout.service.updates.BetDetailRequestCtx;
import java.util.Map;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.core.reactive.ReactiveKafkaProducerTemplate;
import reactor.kafka.sender.SenderOptions;

@Configuration
public class ReactiveKafkaProducerConfig {

  /**
   * Bean defining Bet-details-request Kafka Producer
   *
   * @param properties
   * @return
   */
  @Bean
  public ReactiveKafkaProducerTemplate<String, BetDetailRequestCtx>
      betDetailReactiveKafkaProducerTemplate(InternalKafkaProperties properties) {
    return new ReactiveKafkaProducerTemplate<>(SenderOptions.create(getProps(properties)));
  }

  /**
   * Bean defining Cashout-offer-request Kafka Producer
   *
   * @param properties
   * @return
   */
  @Bean
  public ReactiveKafkaProducerTemplate<String, CashoutRequest>
      cashoutReqReactiveKafkaProducerTemplate(InternalKafkaProperties properties) {
    return new ReactiveKafkaProducerTemplate<>(SenderOptions.create(getProps(properties)));
  }

  /**
   * Bean defining BetUpdate Kafka Producer
   *
   * @param properties
   * @return
   */
  @Bean
  public ReactiveKafkaProducerTemplate<String, UpdateDto> betUpdateReactiveKafkaProducerTemplate(
      InternalKafkaProperties properties) {
    return new ReactiveKafkaProducerTemplate<>(SenderOptions.create(getProps(properties)));
  }

  /**
   * Bean defining betUpdates-error Kafka Producer
   *
   * @param properties
   * @return
   */
  @Bean
  public ReactiveKafkaProducerTemplate<String, Throwable>
      betUpdatesErrorReactiveKafkaProducerTemplate(InternalKafkaProperties properties) {
    return new ReactiveKafkaProducerTemplate<>(SenderOptions.create(getProps(properties)));
  }

  private Map<String, Object> getProps(InternalKafkaProperties properties) {
    return properties.getKafka().buildProducerProperties();
  }
}
