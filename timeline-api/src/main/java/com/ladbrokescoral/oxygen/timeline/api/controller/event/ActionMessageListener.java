package com.ladbrokescoral.oxygen.timeline.api.controller.event;

import com.ladbrokescoral.oxygen.timeline.api.channel.ChannelHandlersContext;
import com.ladbrokescoral.oxygen.timeline.api.controller.Room;
import com.ladbrokescoral.oxygen.timeline.api.model.dto.out.*;
import com.ladbrokescoral.oxygen.timeline.api.model.message.ChangeCampaignMessage;
import com.ladbrokescoral.oxygen.timeline.api.model.message.ChangePostMessage;
import com.ladbrokescoral.oxygen.timeline.api.model.message.RemoveCampaignMessage;
import com.ladbrokescoral.oxygen.timeline.api.model.message.RemovePostMessage;
import com.ladbrokescoral.oxygen.timeline.api.reactive.model.MessageContent;
import java.util.Optional;
import lombok.RequiredArgsConstructor;
import org.modelmapper.ModelMapper;
import org.springframework.context.event.EventListener;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class ActionMessageListener {
  private final ModelMapper modelMapper;

  @EventListener
  public void onChangePostMessage(ChangePostMessage changePostMessage) {
    Optional.ofNullable(ChannelHandlersContext.channels.get(Room.ACTION_ROOM.name()))
        .ifPresent(
            manies ->
                manies.stream()
                    .parallel()
                    .forEach(
                        pageChannel ->
                            pageChannel.tryEmitNext(
                                MessageContent.withPayload(
                                    SocketEvent.POST_CHANGED.name(),
                                    modelMapper.map(
                                        changePostMessage, ChangePostMessageDto.class)))));
  }

  @EventListener
  public void onRemovePostMessage(RemovePostMessage removePostMessage) {
    Optional.ofNullable(ChannelHandlersContext.channels.get(Room.ACTION_ROOM.name()))
        .ifPresent(
            manies ->
                manies.stream()
                    .parallel()
                    .forEach(
                        pageChannel ->
                            pageChannel.tryEmitNext(
                                MessageContent.withPayload(
                                    SocketEvent.POST_REMOVED.name(),
                                    modelMapper.map(
                                        removePostMessage, RemovePostMessageDto.class)))));
  }

  @EventListener
  public void onChangeCampaignMessageMessage(ChangeCampaignMessage changeCampaignMessage) {
    Optional.ofNullable(ChannelHandlersContext.channels.get(Room.ACTION_ROOM.name()))
        .ifPresent(
            manies ->
                manies.stream()
                    .parallel()
                    .forEach(
                        pageChannel ->
                            pageChannel.tryEmitNext(
                                MessageContent.withPayload(
                                    SocketEvent.CAMPAIGN_CHANGED.name(),
                                    modelMapper.map(
                                        changeCampaignMessage, ChangeCampaignMessageDto.class)))));
  }

  @EventListener
  public void onRemoveCampaignMessage(RemoveCampaignMessage removeCampaignMessage) {
    Optional.ofNullable(ChannelHandlersContext.channels.get(Room.ACTION_ROOM.name()))
        .ifPresent(
            manies ->
                manies.stream()
                    .parallel()
                    .forEach(
                        pageChannel ->
                            pageChannel.tryEmitNext(
                                MessageContent.withPayload(
                                    SocketEvent.CAMPAIGN_CLOSED.name(),
                                    modelMapper.map(
                                        removeCampaignMessage, RemoveCampaignMessageDto.class)))));
  }
}
