package com.ladbrokescoral.oxygen.timeline.api.controller;

import com.ladbrokescoral.oxygen.timeline.api.model.message.Message;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Profile;
import org.springframework.kafka.core.reactive.ReactiveKafkaConsumerTemplate;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;

@Profile("!test")
@Service
@Slf4j
@AllArgsConstructor
public class MessageListener implements CommandLineRunner {
  private final ReactiveKafkaConsumerTemplate<String, Message> reactiveKafkaConsumerTemplate;
  private final MessageProcessorFactory messageProcessorFactory;

  public Flux<Message> consume() {
    return reactiveKafkaConsumerTemplate
        .receiveAutoAck()
        .map(ConsumerRecord::value)
        .doOnNext(
            (Message message) -> {
              log.info("Message ={}", message);
              messageProcessorFactory.getInstance(message.getClass()).process(message);
            })
        .doOnError(
            throwable ->
                log.error("something bad happened while consuming : {}", throwable.getMessage()));
  }

  @Override
  public void run(String... args) throws Exception {
    consume().subscribe();
  }
}
