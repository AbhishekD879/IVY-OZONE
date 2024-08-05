package com.ladbrokescoral.oxygen.timeline.api.controller;

import com.ladbrokescoral.oxygen.timeline.api.model.message.Message;
import com.ladbrokescoral.oxygen.timeline.api.service.MessageProcessor;

@FunctionalInterface
public interface MessageProcessorFactory {

  <T extends Message> MessageProcessor<T> getInstance(Class<?> type);
}
