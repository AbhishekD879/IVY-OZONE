package com.ladbrokescoral.oxygen.timeline.api.handlers;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

import com.coral.oxygen.middleware.ms.liveserv.client.model.Message;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.Envelope;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.ladbrokescoral.oxygen.timeline.api.channel.ChannelHandlersContext;
import com.ladbrokescoral.oxygen.timeline.api.controller.Room;
import com.ladbrokescoral.oxygen.timeline.api.model.Template;
import com.ladbrokescoral.oxygen.timeline.api.model.message.PostMessage;
import com.ladbrokescoral.oxygen.timeline.api.model.obevent.*;
import com.ladbrokescoral.oxygen.timeline.api.obevent.updates.ChannelMessageApplier;
import com.ladbrokescoral.oxygen.timeline.api.obevent.updates.LiveserveMessageApplierFactory;
import com.ladbrokescoral.oxygen.timeline.api.repository.PostRepository;
import com.ladbrokescoral.oxygen.timeline.api.service.LiveServMessageHandler;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.web.server.LocalServerPort;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.context.junit4.SpringRunner;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@DirtiesContext
public class LiveServMessageHandlerTest {
  @LocalServerPort private String port;
  @MockBean PostRepository postRepository;
  @Autowired List<ChannelMessageApplier> channelMessageApplierTypes;
  @Autowired LiveserveMessageApplierFactory liveserveMessageApplierFactory;
  @Autowired LiveServMessageHandler liveServMessageHandler;

  @Test
  public void testHandle() throws IOException {
    Arrays.stream(Room.values())
        .forEach(room -> ChannelHandlersContext.createIfAbsentAndReturnChannel(room.name()));
    when(postRepository.findAll()).thenReturn(postMessages());
    when(postRepository.save(any())).thenReturn(postMessages().get(0));
    Message message = new Message();
    message.setMessageCode("code");
    message.setJsonData(
        new String(Files.readAllBytes(Paths.get("src/test/resources/messsage_1.json"))));
    Envelope envelope = new MessageEnvelope("sEVENT0000810351", 123, message);
    StepVerifier.create(Mono.fromRunnable(() -> liveServMessageHandler.handle(envelope)))
        .verifyComplete();
  }

  private List<PostMessage> postMessages() {
    List<PostMessage> postMessages = new ArrayList<>();
    PostMessage postMessage = PostMessage.builder().build();
    postMessage.setCampaignId("12345");
    postMessage.setCampaignName("abcd");
    postMessage.setPinned(true);
    postMessage.setHeaderText("abcd");
    postMessage.setSpotlight(true);
    postMessage.setId("12345");
    Template template = new Template();
    template.setSelectionId("7890");
    postMessage.setTemplate(template);
    postMessage.setText("hello");
    postMessage.setVerdict(true);
    Instant instant = Instant.now();
    postMessage.setCreatedDate(instant);
    postMessage.setBrand("coral");
    TimelineSelectionEvent timelineSelectionEvent = new TimelineSelectionEvent();
    ObEvent obEvent = new ObEvent();
    obEvent.setId("810351");
    obEvent.setIsActive(true);
    ObOutcome obOutcome = new ObOutcome();
    obOutcome.setId("7890");
    ObMarket obMarket = new ObMarket();
    obMarket.setOutcomes(Arrays.asList(obOutcome));
    obMarket.setId("7890");
    obMarket.setIsActive(true);
    obEvent.setMarkets(Arrays.asList(obMarket));
    timelineSelectionEvent.setObEvent(obEvent);
    postMessage.setSelectionEvent(timelineSelectionEvent);

    postMessages.add(postMessage);
    return postMessages;
  }
}
