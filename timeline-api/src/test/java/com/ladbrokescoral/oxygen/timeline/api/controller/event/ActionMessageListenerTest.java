package com.ladbrokescoral.oxygen.timeline.api.controller.event;

import com.ladbrokescoral.oxygen.timeline.api.channel.ChannelHandlersContext;
import com.ladbrokescoral.oxygen.timeline.api.controller.Room;
import com.ladbrokescoral.oxygen.timeline.api.model.message.*;
import java.time.Instant;
import java.util.Arrays;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.web.server.LocalServerPort;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.context.junit4.SpringRunner;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@DirtiesContext
public class ActionMessageListenerTest {
  @LocalServerPort private String port;
  @Autowired ModelMapper modelMapper;
  @Autowired ActionMessageListener listener;

  @Test
  public void testOnChangePostMessage() {
    Arrays.stream(Room.values())
        .forEach(room -> ChannelHandlersContext.createIfAbsentAndReturnChannel(room.name()));
    ChangePostMessage changePostMessage = new ChangePostMessage();
    changePostMessage.setId("12345");
    Instant instant = Instant.now();
    changePostMessage.setCreatedDate(instant);
    changePostMessage.setBrand("coral");
    changePostMessage.setAffectedMessageId("12345");
    changePostMessage.setCreatedDate(instant);
    changePostMessage.setAffectedMessageCreatedDate(instant);
    PostMessage postMessage = PostMessage.builder().build();
    postMessage.setCreatedDate(instant);
    changePostMessage.setData(postMessage);
    StepVerifier.create(Mono.fromRunnable(() -> listener.onChangePostMessage(changePostMessage)))
        .verifyComplete();
  }

  @Test
  public void testOnRemovePostMessage() {
    Arrays.stream(Room.values())
        .forEach(room -> ChannelHandlersContext.createIfAbsentAndReturnChannel(room.name()));
    RemovePostMessage removePostMessage = new RemovePostMessage();
    removePostMessage.setBrand("coral");
    removePostMessage.setAffectedMessageId("12345");
    Instant instant = Instant.now();
    removePostMessage.setCreatedDate(instant);
    removePostMessage.setId("12345");
    removePostMessage.setAffectedMessageCreatedDate(instant);
    StepVerifier.create(Mono.fromRunnable(() -> listener.onRemovePostMessage(removePostMessage)))
        .verifyComplete();
  }

  @Test
  public void onChangeCampaignMessageMessage() {
    Arrays.stream(Room.values())
        .forEach(room -> ChannelHandlersContext.createIfAbsentAndReturnChannel(room.name()));
    ChangeCampaignMessage postMessage = new ChangeCampaignMessage();
    postMessage.setId("12345");
    Instant instant = Instant.now();
    postMessage.setCreatedDate(instant);
    postMessage.setBrand("coral");
    CampaignMessage campaignMessage = new CampaignMessage();
    campaignMessage.setBrand("coral");
    campaignMessage.setCreatedDate(instant);
    campaignMessage.setId("12345");
    postMessage.setData(campaignMessage);
    StepVerifier.create(
            Mono.fromRunnable(() -> listener.onChangeCampaignMessageMessage(postMessage)))
        .verifyComplete();
  }

  @Test
  public void onRemoveCampaignMessage() {
    Arrays.stream(Room.values())
        .forEach(room -> ChannelHandlersContext.createIfAbsentAndReturnChannel(room.name()));
    RemoveCampaignMessage removeCampaignMessage = new RemoveCampaignMessage();
    removeCampaignMessage.setBrand("coral");
    removeCampaignMessage.setAffectedMessageId("12345");
    Instant instant = Instant.now();
    removeCampaignMessage.setCreatedDate(instant);
    removeCampaignMessage.setId("12345");
    removeCampaignMessage.setAffectedMessageCreatedDate(instant);
    StepVerifier.create(
            Mono.fromRunnable(() -> listener.onRemoveCampaignMessage(removeCampaignMessage)))
        .verifyComplete();
  }
}
