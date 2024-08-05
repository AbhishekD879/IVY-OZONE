package com.coral.oxygen.edp.configuration;

import lombok.Getter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

@Getter
@Configuration
public class SportsDataConsumerConfiguration {
  @Value("${edp.firstmarkets.consumer.queue.size}")
  private int maxQueueSize;

  @Value("${edp.firstmarkets.consumer.thraeds.count}")
  private int threadsCount;

  @Value("${sports.update.min-seconds-before-event-start}")
  private int minimumSecondsUntilStart;

  @Value("${sports.virtuals.category.id}")
  private int virtualCategoryId;
}
