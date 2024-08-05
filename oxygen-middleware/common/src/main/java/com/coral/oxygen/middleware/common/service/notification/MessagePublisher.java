package com.coral.oxygen.middleware.common.service.notification;

import com.coral.oxygen.middleware.common.service.notification.topic.TopicType;

public interface MessagePublisher {

  void publish(TopicType topic, String key, String message);

  default void publish(TopicType topic, String message) {
    publish(topic, null, message);
  }
}
