package com.coral.oxygen.middleware.common.service.notification.topic;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
public class TopicResolver {

  private final String prefix;

  public String find(TopicType topic) {
    return String.format("%s__%s", prefix, topic.getTopicName());
  }
}
