package com.ladbrokescoral.oxygen.timeline.api.obevent.updates;

import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;
import static org.mockito.Mockito.atLeastOnce;

import com.coral.oxygen.middleware.ms.liveserv.client.model.Message;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.timeline.api.model.Template;
import com.ladbrokescoral.oxygen.timeline.api.model.message.PostMessage;
import com.ladbrokescoral.oxygen.timeline.api.model.obevent.*;
import com.ladbrokescoral.oxygen.timeline.api.repository.PostRepository;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import org.jetbrains.annotations.NotNull;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class EventMessageApplierTest {
  public static final String CHANNEL = "1234567890";
  private EventMessageApplier eventMessageApplier;
  @Mock private PostRepository postRepository;

  @Mock private ObjectMapper objectMapper;

  @Mock private MessageEnvelope messageEnvelope;

  @Before
  public void init() throws JsonProcessingException {
    eventMessageApplier = new EventMessageApplier(objectMapper, postRepository);
    when(objectMapper.readValue(anyString(), eq(EventStatus.class))).thenReturn(new EventStatus());
    when(messageEnvelope.getMessage()).thenReturn(new Message("123", "{}"));
    when(messageEnvelope.getChannel()).thenReturn(CHANNEL);

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
    obEvent.setId("1234");
    ObOutcome obOutcome = new ObOutcome();
    obOutcome.setId("7890");
    ObMarket obMarket = new ObMarket();
    obMarket.setOutcomes(Arrays.asList(obOutcome));
    obMarket.setId("1234");
    obEvent.setMarkets(Arrays.asList(obMarket));
    timelineSelectionEvent.setObEvent(obEvent);
    postMessage.setSelectionEvent(timelineSelectionEvent);

    doReturn(postMessage).when(postRepository).save(any(PostMessage.class));
    doReturn(postMessages()).when(postRepository).findAll();
  }

  @Test
  public void testIfPostsWereSearchedWithProperId() {
    eventMessageApplier.applyUpdate(messageEnvelope);
    Mockito.verify(postRepository, atLeastOnce()).findAll();
    Mockito.verify(postRepository, atLeastOnce()).save(any(PostMessage.class));
  }

  @NotNull
  private EventStatus getEventStatus() {
    EventStatus eventStatus = new EventStatus();
    when(eventStatus.getActive()).thenReturn(true);
    when(eventStatus.getDisplayed()).thenReturn(true);
    when(eventStatus.getStarted()).thenReturn(true);
    when(eventStatus.getResulted()).thenReturn(true);
    return eventStatus;
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
    obEvent.setId("7890");
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
