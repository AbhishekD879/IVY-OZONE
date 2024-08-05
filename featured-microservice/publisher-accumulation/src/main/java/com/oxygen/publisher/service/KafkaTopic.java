package com.oxygen.publisher.service;

import java.util.stream.Stream;
import javax.annotation.PostConstruct;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class KafkaTopic {

  @Value("${kafka.topics.prefix}")
  private String prefix;

  // This should be an instance method with @PostConstruct annotation
  // After spring injects @Value("${kafka.topics.prefix}") we change prefix on Topic enum
  @PostConstruct
  public void init() {
    Stream.of(Topic.values()).forEach(kt -> kt.setPrefix(prefix));
  }

  // this is used in SpEL in @KafkaListener
  public String keyFor(String key) {
    return Topic.valueOf(key).getKey();
  }

  @RequiredArgsConstructor
  public enum Topic {
    FEATURED_STRUCTURE_CHANGED,
    FEATURED_MODULE_CONTENT_CHANGED,
    FEATURED_MODULE_CONTENT_CHANGED_MINOR,
    SPORTS_FEATURED_PAGE_DELETED,
    SPORTS_FEATURED_PAGE_ADDED,
    IN_PLAY_STRUCTURE_CHANGED,
    IN_PLAY_SPORT_SEGMENT_CHANGED,
    IN_PLAY_SPORTS_RIBBON_CHANGED,
    IN_PLAY_SPORT_COMPETITION_CHANGED,

    VIRTUAL_SPORTS_RIBBON_CHANGED;

    private final String key;
    @Setter private String prefix;

    Topic() {
      this.key = name();
    }

    public String getKey() {
      return String.format("%s__%s", prefix, key);
    }
  }
}
