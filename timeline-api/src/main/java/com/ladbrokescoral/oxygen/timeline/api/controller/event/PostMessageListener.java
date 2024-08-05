package com.ladbrokescoral.oxygen.timeline.api.controller.event;

import com.ladbrokescoral.oxygen.timeline.api.channel.ChannelHandlersContext;
import com.ladbrokescoral.oxygen.timeline.api.controller.Room;
import com.ladbrokescoral.oxygen.timeline.api.model.dto.out.PostMessageDto;
import com.ladbrokescoral.oxygen.timeline.api.model.message.PostMessage;
import com.ladbrokescoral.oxygen.timeline.api.reactive.model.MessageContent;
import java.util.Optional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.context.event.EventListener;
import org.springframework.stereotype.Component;

@Component
@Slf4j
@RequiredArgsConstructor
public class PostMessageListener {
  private final ModelMapper modelMapper;

  @EventListener
  public void onPostMessage(PostMessage post) {
    Optional.ofNullable(ChannelHandlersContext.channels.get(Room.POST_ROOM.name()))
        .ifPresent(
            manies ->
                manies.stream()
                    .parallel()
                    .forEach(
                        pageChannel ->
                            pageChannel.tryEmitNext(
                                MessageContent.withPayload(
                                    SocketEvent.POST.name(),
                                    modelMapper.map(post, PostMessageDto.class)))));
  }
}
