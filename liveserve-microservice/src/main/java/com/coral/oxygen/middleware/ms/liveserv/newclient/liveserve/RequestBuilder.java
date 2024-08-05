package com.coral.oxygen.middleware.ms.liveserv.newclient.liveserve;

import com.coral.oxygen.middleware.ms.liveserv.newclient.LiveUpdatesChannel;
import com.coral.oxygen.middleware.ms.liveserv.utils.StringUtils;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentMap;
import java.util.stream.Collectors;
import okhttp3.MediaType;
import okhttp3.Request;
import okhttp3.RequestBody;

public class RequestBuilder {
  private static final String UNCHANGED_SIZE_PREFIX = "S";
  public static final MediaType MEDIA_TYPE_MARKDOWN =
      MediaType.parse("text/x-markdown; charset=utf-8");
  private static final String PAYLOAD_COMMON_UPDATED_PREFIX = "CL0000";
  private static final String UNCGANGED_LAST_MESSAGE_ID = "!!!!!!!!!0";

  public Request build(String endPoint, Payload payload) {
    String body = buildPayload(payload);
    Request.Builder builder = new Request.Builder();
    builder.url(endPoint);
    builder.post(RequestBody.create(MEDIA_TYPE_MARKDOWN, body));
    return builder.build();
  }

  private void buildChangedItems(
      StringBuilder payloadBuilder, ConcurrentMap<String, LiveUpdatesChannel> eventsPayloads) {
    for (Map.Entry<String, LiveUpdatesChannel> entry : eventsPayloads.entrySet()) {
      LiveUpdatesChannel subscriptionSubject = entry.getValue();
      if (subscriptionSubject.getLastMessageID().length() > 0) {
        payloadBuilder.append(subscriptionSubject.getUpdatedKeyValue());
      }
    }
  }

  private String buildPayload(Payload payload) {
    StringBuilder payloadBuilder = new StringBuilder();
    payloadBuilder.append(PAYLOAD_COMMON_UPDATED_PREFIX);
    ConcurrentMap<String, LiveUpdatesChannel> eventsPayloads = payload.getPayloadItems();
    List<LiveUpdatesChannel> unchangedItems = collectUnchangedItems(eventsPayloads);
    buildUnchangedItems(payloadBuilder, unchangedItems);
    buildChangedItems(payloadBuilder, eventsPayloads);
    return payloadBuilder.toString();
  }

  private void buildUnchangedItems(StringBuilder payloadBuilder, List<LiveUpdatesChannel> items) {
    if (items.size() > 0) {
      payloadBuilder.append(UNCHANGED_SIZE_PREFIX);
      String count = StringUtils.addLeadingZeros(String.valueOf(items.size()), 4);
      payloadBuilder.append(count);
      for (LiveUpdatesChannel emptyMessage : items) {
        payloadBuilder.append(emptyMessage.getKeyValue());
      }
      payloadBuilder.append(UNCGANGED_LAST_MESSAGE_ID);
    }
  }

  private List<LiveUpdatesChannel> collectUnchangedItems(
      ConcurrentMap<String, LiveUpdatesChannel> eventsPayloads) {
    return eventsPayloads.values().stream()
        .filter(channel -> channel.getLastMessageID().length() == 0)
        .collect(Collectors.toList());
  }
}
