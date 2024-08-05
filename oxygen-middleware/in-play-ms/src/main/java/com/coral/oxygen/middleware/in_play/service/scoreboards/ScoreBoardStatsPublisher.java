package com.coral.oxygen.middleware.in_play.service.scoreboards;

import com.coral.oxygen.middleware.common.service.notification.MessagePublisher;
import com.coral.oxygen.middleware.common.service.notification.MessagePublisherTopicSelector;
import com.coral.oxygen.middleware.common.service.notification.topic.TopicType;
import com.egalacoral.spark.liveserver.BaseObject;
import com.egalacoral.spark.liveserver.utils.JsonMapper;
import java.math.BigInteger;
import java.util.Date;
import java.util.Map;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
@Slf4j
public class ScoreBoardStatsPublisher {

  private final JsonMapper jsonMapper;

  private final MessagePublisherTopicSelector topicSelector;

  private final MessagePublisher messagePublisher;

  public void publishScoreBoardStats(String obEventId, String updatedMessage) {

    Map<String, Object> updatedStats;
    updatedStats = this.jsonMapper.read(updatedMessage, Map.class);
    BaseObject.ScoreBoardStats scoreBoardStats = new BaseObject.ScoreBoardStats();
    scoreBoardStats.setStats(updatedStats);
    BaseObject baseObject = new BaseObject();
    baseObject.setPublishedDate(new Date());
    baseObject.setType("ScoreBoardStats");
    baseObject.setEvent(
        new BaseObject.Event()
            .eventId(BigInteger.valueOf(Integer.parseInt(obEventId)))
            .scoreBoardStats(scoreBoardStats));
    String messageJson = this.jsonMapper.write(baseObject);
    log.info("ScoreBoardStats messageJson to publisher is::{}", messageJson);
    TopicType topic = this.topicSelector.getLiveServeMessageTopic();
    log.info("ScoreBoardStats topic is :: {}", topic.getTopicName());
    // publish to the inplay publisher
    this.messagePublisher.publish(topic, obEventId, messageJson);
  }
}
