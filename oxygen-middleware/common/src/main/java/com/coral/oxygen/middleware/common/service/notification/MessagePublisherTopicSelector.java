package com.coral.oxygen.middleware.common.service.notification;

import com.coral.oxygen.middleware.common.service.notification.topic.TopicType;

public interface MessagePublisherTopicSelector {

  TopicType getLiveServeMessageTopic();
}
