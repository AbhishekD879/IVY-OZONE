package com.coral.oxygen.middleware.featured.configuration;

import static com.coral.oxygen.middleware.common.service.notification.topic.TopicType.FEATURED_LIVE_SERVER_MODULES;
import static com.coral.oxygen.middleware.common.service.notification.topic.TopicType.FEATURED_MODULE_CONTENT_CHANGED;
import static com.coral.oxygen.middleware.common.service.notification.topic.TopicType.FEATURED_MODULE_CONTENT_CHANGED_MINOR;
import static com.coral.oxygen.middleware.common.service.notification.topic.TopicType.FEATURED_STRUCTURE_CHANGED;
import static com.coral.oxygen.middleware.common.service.notification.topic.TopicType.SPORTS_FEATURED_PAGE_ADDED;
import static com.coral.oxygen.middleware.common.service.notification.topic.TopicType.SPORTS_FEATURED_PAGE_DELETED;

import com.coral.oxygen.middleware.common.configuration.KafkaConfiguration;
import com.coral.oxygen.middleware.common.service.notification.MessagePublisherTopicSelector;
import com.coral.oxygen.middleware.common.service.notification.topic.TopicResolver;
import org.apache.kafka.clients.admin.NewTopic;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@ConditionalOnProperty(name = "featured.scheduled.task.enabled")
public class FeaturedKafkaConfiguration extends KafkaConfiguration {

  public FeaturedKafkaConfiguration(
      @Value("${spring.kafka.bootstrap-servers}") String kafkaBrokers,
      @Value("${kafka.partition.default}") Integer defaultNumPartitions,
      @Value("${kafka.replica.factor}") short replicaFactor,
      TopicResolver topicResolver) {
    super(kafkaBrokers, defaultNumPartitions, replicaFactor, topicResolver);
  }

  @Bean
  public NewTopic featuredStructureChangedTopic() {
    String topic = topicResolver.find(FEATURED_STRUCTURE_CHANGED);
    return new NewTopic(topic, MIN_NUM_PARTITIONS, replicaFactor);
  }

  @Bean
  public NewTopic featuredModuleContentChangedTopic() {
    String topic = topicResolver.find(FEATURED_MODULE_CONTENT_CHANGED);
    return new NewTopic(topic, MIN_NUM_PARTITIONS, replicaFactor);
  }

  @Bean
  public NewTopic featuredModuleContentChangedMinorTopic() {
    String topic = topicResolver.find(FEATURED_MODULE_CONTENT_CHANGED_MINOR);
    return new NewTopic(topic, MIN_NUM_PARTITIONS, replicaFactor);
  }

  @Bean
  public NewTopic featuredLiveServeTopic() {
    String topic = topicResolver.find(FEATURED_LIVE_SERVER_MODULES);
    return new NewTopic(topic, defaultNumPartitions, replicaFactor);
  }

  @Bean
  public NewTopic sportFeaturedPageDeleted() {
    String topic = topicResolver.find(SPORTS_FEATURED_PAGE_DELETED);
    return new NewTopic(topic, MIN_NUM_PARTITIONS, replicaFactor);
  }

  @Bean
  public MessagePublisherTopicSelector messagePublisherTopicSelector() {
    return () -> FEATURED_LIVE_SERVER_MODULES;
  }

  @Bean
  public NewTopic sportFeaturedPagesChanged() {
    String topic = topicResolver.find(SPORTS_FEATURED_PAGE_ADDED);
    return new NewTopic(topic, MIN_NUM_PARTITIONS, replicaFactor);
  }
}
