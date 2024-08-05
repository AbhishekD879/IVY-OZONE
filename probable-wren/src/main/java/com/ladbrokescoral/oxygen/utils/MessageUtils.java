package com.ladbrokescoral.oxygen.utils;

import com.corundumstudio.socketio.SocketIOClient;
import com.google.gson.Gson;
import com.ladbrokescoral.oxygen.dto.messages.Envelope;
import com.ladbrokescoral.oxygen.dto.messages.EnvelopeType;
import com.ladbrokescoral.oxygen.dto.messages.ErrorAsk;
import com.ladbrokescoral.oxygen.dto.messages.MessageObjectEnvelope;
import com.ladbrokescoral.oxygen.dto.messages.SubscriptionAck;
import com.ladbrokescoral.oxygen.dto.messages.SubscriptionError;
import com.ladbrokescoral.oxygen.dto.messages.UnsubscribedAsk;
import com.newrelic.api.agent.NewRelic;
import com.newrelic.api.agent.Trace;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class MessageUtils {

  private static final String METRIC_CATEGORY = "Queue";

  private MessageUtils() {
    throw new IllegalStateException("Utility class");
  }

  public static Object convert(Envelope envelope, Gson gson) {
    switch (envelope.getType()) {
      case MESSAGE:
        final MessageObjectEnvelope messageObjectEnvelope =
            new MessageObjectEnvelope(envelope, gson);
        NewRelic.setTransactionName(
            METRIC_CATEGORY,
            envelope.getType().toString() + "/" + messageObjectEnvelope.getSubChannel().getType());
        return messageObjectEnvelope;
      case SUBSCRIBED:
        NewRelic.setTransactionName(METRIC_CATEGORY, envelope.getType().toString());
        return new SubscriptionAck(envelope.getChannel());
      case UNSUBSCRIBE:
        NewRelic.setTransactionName(METRIC_CATEGORY, envelope.getType().toString());
        return new UnsubscribedAsk(envelope.getChannel());
      case SUBSCRIPTION_ERROR:
        NewRelic.setTransactionName(METRIC_CATEGORY, envelope.getType().toString());
        return new SubscriptionError(envelope.getChannel());
      default:
        NewRelic.setTransactionName(METRIC_CATEGORY, "ERROR");
        return new ErrorAsk(envelope.getChannel());
    }
  }

  public static Optional<MessageObjectEnvelope> toMessage(Envelope envelope, Gson gson) {
    if (!EnvelopeType.MESSAGE.equals(envelope.getType())) {
      return Optional.empty();
    }
    final MessageObjectEnvelope messageObjectEnvelope = new MessageObjectEnvelope(envelope, gson);
    NewRelic.setTransactionName(
        METRIC_CATEGORY,
        envelope.getType().toString() + "/" + messageObjectEnvelope.getSubChannel().getType());
    return Optional.of(messageObjectEnvelope);
  }

  @Trace(dispatcher = true)
  public static void notify(
      String channel, Object payload, SocketIOClient client, String transactionName) {
    NewRelic.setTransactionName(null, transactionName);
    try {
      client.sendEvent(channel, payload);
    } catch (Exception e) {
      log.error("ERROR-ON-MESSAGE-SEND-TO-CLIENT:{}:{}", channel, client, e);
    }
  }
}
