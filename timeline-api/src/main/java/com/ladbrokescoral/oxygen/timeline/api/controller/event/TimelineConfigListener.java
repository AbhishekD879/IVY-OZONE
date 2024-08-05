package com.ladbrokescoral.oxygen.timeline.api.controller.event;

import com.ladbrokescoral.oxygen.timeline.api.channel.ChannelHandlersContext;
import com.ladbrokescoral.oxygen.timeline.api.controller.Room;
import com.ladbrokescoral.oxygen.timeline.api.model.dto.out.TimelineConfigDto;
import com.ladbrokescoral.oxygen.timeline.api.model.message.TimelineConfigMessage;
import com.ladbrokescoral.oxygen.timeline.api.reactive.model.MessageContent;
import java.util.Optional;
import lombok.RequiredArgsConstructor;
import org.modelmapper.ModelMapper;
import org.springframework.context.event.EventListener;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class TimelineConfigListener {
  private final ModelMapper modelMapper;

  @EventListener
  public void onPostMessage(TimelineConfigMessage timelineConfigMessage) {
    Optional.ofNullable(ChannelHandlersContext.channels.get(Room.TIMELINE_CONFIG.name()))
        .ifPresent(
            manies ->
                manies.stream()
                    .parallel()
                    .forEach(
                        pageChannel ->
                            pageChannel.tryEmitNext(
                                MessageContent.withPayload(
                                    SocketEvent.TIMELINE_CONFIG.name(),
                                    modelMapper.map(
                                        timelineConfigMessage, TimelineConfigDto.class)))));
  }
}
