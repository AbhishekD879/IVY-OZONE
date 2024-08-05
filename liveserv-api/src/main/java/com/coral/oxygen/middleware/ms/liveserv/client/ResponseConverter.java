package com.coral.oxygen.middleware.ms.liveserv.client;

import com.coral.oxygen.middleware.ms.liveserv.client.model.Message;
import java.util.ArrayList;
import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ResponseConverter {

  private static final Logger LOGGER = LoggerFactory.getLogger(ResponseConverter.class);
  private static final int JSON_BODY_START_INDEX = 56;
  private static final String MESSAGE_DELIMITER = "M";
  private static final int MESSAGE_END_INDEX = 56;

  public List<Message> convert(String responseString) {
    LOGGER.debug("Data to convert : '{}' ", responseString);
    List<Message> messages = new ArrayList<>();
    List<Integer> items = new ArrayList<>();
    if (responseString == null || responseString.isEmpty()) {
      LOGGER.info("Empty response");
      return messages;
    }

    int lastIndex = 0;
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
    int next;
    for (int i = 0; i < items.size(); i++) {
      next = i + 1;
      int endPosition;
      int startPosition;
      if (next < items.size()) {
        startPosition = items.get(i);
        endPosition = items.get(next);
      } else {
        startPosition = items.get(i);
        endPosition = responseString.length();
      }
      String block = responseString.substring(startPosition, endPosition);
      String message = block.substring(0, MESSAGE_END_INDEX);
      String json = block.substring(JSON_BODY_START_INDEX);
      messages.add(new Message(message, json));
    }
    LOGGER.info("Converted {} message(s) ", messages.size());
    return messages;
  }
}
