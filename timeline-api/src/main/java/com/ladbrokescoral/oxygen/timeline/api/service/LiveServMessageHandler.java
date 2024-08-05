package com.ladbrokescoral.oxygen.timeline.api.service;

import static com.coral.oxygen.middleware.ms.liveserv.model.messages.EnvelopeType.MESSAGE;

import com.coral.oxygen.middleware.ms.liveserv.MessageHandler;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.Envelope;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.ladbrokescoral.oxygen.timeline.api.channel.ChannelHandlersContext;
import com.ladbrokescoral.oxygen.timeline.api.controller.Room;
import com.ladbrokescoral.oxygen.timeline.api.controller.event.SocketEvent;
import com.ladbrokescoral.oxygen.timeline.api.model.message.PostMessage;
import com.ladbrokescoral.oxygen.timeline.api.obevent.updates.LiveserveMessageApplierFactory;
import com.ladbrokescoral.oxygen.timeline.api.reactive.model.MessageContent;
import java.util.List;
import java.util.Optional;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

@Slf4j
@Component
@AllArgsConstructor
public class LiveServMessageHandler implements MessageHandler {

  private final LiveserveMessageApplierFactory liveserveMessageApplierFactory;

  @Override
  public void handle(Envelope envelope) {
    if (envelope.getType() == MESSAGE) {
      MessageEnvelope messageEnvelope = (MessageEnvelope) envelope;
      List<PostMessage> updatedPosts =
          liveserveMessageApplierFactory
              .get(messageEnvelope.getChannel())
              .applyUpdate(messageEnvelope);
      if (!updatedPosts.isEmpty()) {
        Optional.ofNullable(ChannelHandlersContext.channels.get(Room.ACTION_ROOM.name()))
            .ifPresent(
                manies ->
                    manies.stream()
                        .parallel()
                        .forEach(
                            pageChannel ->
                                pageChannel.tryEmitNext(
                                    MessageContent.withPayload(
                                        SocketEvent.POST_CHANGED.name(), updatedPosts))));
      }
    }
  }
}
