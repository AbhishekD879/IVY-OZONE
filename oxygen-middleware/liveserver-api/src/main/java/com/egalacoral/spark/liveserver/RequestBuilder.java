package com.egalacoral.spark.liveserver;

import com.egalacoral.spark.liveserver.utils.StringUtils;
import java.util.List;
import java.util.concurrent.ConcurrentMap;
import java.util.stream.Collectors;
import okhttp3.MediaType;
import okhttp3.Request;
import okhttp3.RequestBody;

public class RequestBuilder {
  private static final String UNCHANGED_SIZE_PREFIX = "S";
  private static final MediaType MEDIA_TYPE_MARKDOWN =
      MediaType.parse("text/x-markdown; charset=utf-8");
  private static final String PAYLOAD_COMMON_UPDATED_PREFIX = "CL0000";
  private static final String UNCGANGED_LAST_MESSAGE_ID = "!!!!!!!!!0";

  public Request build(String endPoint, Payload payload) {
    String body = buildPayload(payload);
    Request.Builder requestBuilder = new Request.Builder();
    requestBuilder.url(endPoint);
    requestBuilder.post(RequestBody.create(MEDIA_TYPE_MARKDOWN, body));
    return requestBuilder.build();
  }

  private void buildChangedItems(
      StringBuilder payloadBuilder, ConcurrentMap<String, SubscriptionSubject> eventsPayloads) {
    eventsPayloads
        .values()
        .forEach(
            subject -> {
              if (subject.getLastMessageID().length() > 0) {
                payloadBuilder.append(subject.getUpdatedKeyValue());
              }
            });
  }

  private String buildPayload(Payload payload) {
    StringBuilder payloadBuilder = new StringBuilder();
    payloadBuilder.append(PAYLOAD_COMMON_UPDATED_PREFIX);
    ConcurrentMap<String, SubscriptionSubject> eventsPayloads = payload.getPayloadItems();
    List<SubscriptionSubject> unchangedItems = collectUnchangedItems(eventsPayloads);
    buildUnchangedItems(payloadBuilder, unchangedItems);
    buildChangedItems(payloadBuilder, eventsPayloads);
    return payloadBuilder.toString();
  }

  private void buildUnchangedItems(StringBuilder payloadBuilder, List<SubscriptionSubject> items) {
    if (!items.isEmpty()) {
      payloadBuilder.append(UNCHANGED_SIZE_PREFIX);
      String count = StringUtils.addLeadingZeros(String.valueOf(items.size()), 4);
      payloadBuilder.append(count);
      for (SubscriptionSubject emptyMessage : items) {
        payloadBuilder.append(emptyMessage.getKeyValue());
      }
      payloadBuilder.append(UNCGANGED_LAST_MESSAGE_ID);
    }
  }

  private List<SubscriptionSubject> collectUnchangedItems(
      ConcurrentMap<String, SubscriptionSubject> eventsPayloads) {
    return eventsPayloads.values().stream()
        .filter(subject -> subject.getLastMessageID().isEmpty())
        .collect(Collectors.toList());
  }
}
