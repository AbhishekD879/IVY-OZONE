package com.coral.oxygen.middleware.in_play.service.config;

import static com.coral.oxygen.middleware.common.service.notification.topic.TopicType.*;

import com.coral.oxygen.middleware.common.configuration.KafkaConfiguration;
import com.coral.oxygen.middleware.common.service.notification.MessagePublisherTopicSelector;
import com.coral.oxygen.middleware.common.service.notification.topic.TopicResolver;
import org.apache.kafka.clients.admin.NewTopic;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@ConditionalOnProperty(name = "inplay.scheduled.task.enabled")
public class InPlayKafkaConfiguration extends KafkaConfiguration {

  public InPlayKafkaConfiguration(
      @Value("${spring.kafka.bootstrap-servers}") String kafkaBrokers,
      @Value("${kafka.partition.default}") Integer defaultNumPartitions,
      @Value("${kafka.replica.factor}") short replicaFactor,
      TopicResolver topicResolver) {
    super(kafkaBrokers, defaultNumPartitions, replicaFactor, topicResolver);
  }

  @Bean
  public NewTopic inPlayStructureChangedTopic() {
    String topic = topicResolver.find(IN_PLAY_STRUCTURE_CHANGED);
    return new NewTopic(topic, MIN_NUM_PARTITIONS, replicaFactor);
  }

  @Bean
  public NewTopic inPlaySportSegmentChangedTopic() {
    String topic = topicResolver.find(IN_PLAY_SPORT_SEGMENT_CHANGED);
    return new NewTopic(topic, MIN_NUM_PARTITIONS, replicaFactor);
  }

  @Bean
  public NewTopic inPlaySportsRibbonChangedTopic() {
    String topic = topicResolver.find(IN_PLAY_SPORTS_RIBBON_CHANGED);
    return new NewTopic(topic, MIN_NUM_PARTITIONS, replicaFactor);
  }

  @Bean
  public NewTopic inPlaySportCompetitionChangedTopic() {
    String topic = topicResolver.find(IN_PLAY_SPORT_COMPETITION_CHANGED);
    return new NewTopic(topic, MIN_NUM_PARTITIONS, replicaFactor);
  }

  @Bean
  public NewTopic virtualSportsRibbonChangedTopic() {
    String topic = topicResolver.find(VIRTUAL_SPORTS_RIBBON_CHANGED);
    return new NewTopic(topic, MIN_NUM_PARTITIONS, replicaFactor);
  }

  @Bean
  public NewTopic inplayLiveServeTopic() {
    String topic = topicResolver.find(INPLAY_LIVE_SERVER_MODULES);
    return new NewTopic(topic, defaultNumPartitions, replicaFactor);
  }

  @Bean
  public MessagePublisherTopicSelector messagePublisherTopicSelector() {
    return () -> INPLAY_LIVE_SERVER_MODULES;
  }
}
