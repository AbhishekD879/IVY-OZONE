package com.coral.oxygen.middleware.ms.liveserv.newclient.liveserve;

import com.newrelic.api.agent.NewRelic;
import java.util.ArrayList;
import java.util.List;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class ResponseConverter {

  private static final int JSON_BODY_START_INDEX = 56;
  private static final String MESSAGE_DELIMITER = "M";
  private static final int MESSAGE_END_INDEX = 56;
  private static final int MESSAGE_HASH_END_INDEX = 27;
  private static final int MESSAGE_HASH_START_INDEX = 17;
  private static final int MESSAGE_KEY_END_INDEX = 17;
  private static final String CUSTOM_LIVESERVER_MESSAGES_CONVERTED_COUNTER =
      "Custom/liveserverMessagesConverted";

  public List<Message> convert(String responseString) {
    log.debug("Data to convert : '{}' ", responseString);
    List<Message> messages = new ArrayList<>();
    List<Integer> items = new ArrayList<>();
    if (responseString == null || responseString.isEmpty()) {
      log.debug("Empty response");
      return messages;
    }

    int lastIndex = 0;
    items.clear();
    messages.clear();
    while (lastIndex < responseString.length()) {
      String prefix = responseString.substring(lastIndex, lastIndex + 1);
      if (MESSAGE_DELIMITER.equals(prefix)) {
        String hexJsonLength =
            responseString.substring(
                lastIndex + JSON_BODY_START_INDEX - 6, lastIndex + JSON_BODY_START_INDEX);
        int jsonLength = Integer.parseInt(hexJsonLength, 16);
        items.add(lastIndex);
        lastIndex += (JSON_BODY_START_INDEX + jsonLength);
      } else {
        lastIndex++;
      }
    }
    int next = 0;
    for (int i = 0; i < items.size(); i++) {
      next = i + 1;
      int endPosition;
      int startPosition;
      if (next != items.size() && items.size() > 1) {
        startPosition = items.get(i);
        endPosition = items.get(next);
      } else {
        startPosition = items.get(i);
        endPosition = responseString.length();
      }
      String block = responseString.substring(startPosition, endPosition);
      if (!block.isEmpty()) {
        String messageKey = block.substring(0, MESSAGE_KEY_END_INDEX);
        String message = block.substring(0, MESSAGE_END_INDEX);
        String json = block.substring(JSON_BODY_START_INDEX, block.length());
        String hash = message.substring(MESSAGE_HASH_START_INDEX, MESSAGE_HASH_END_INDEX);
        messages.add(new Message(message, hash, json, messageKey, block));
      }
    }
    log.trace("Converted {} message(s) ", messages.size());
    NewRelic.incrementCounter(CUSTOM_LIVESERVER_MESSAGES_CONVERTED_COUNTER, messages.size());
    return messages;
  }
}
