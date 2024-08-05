package com.ladbrokescoral.oxygen.timeline.api.obevent.updates;

import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

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
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class MarketMessageApplierTest {
  public static final String CHANNEL = "1234567890";
  private MarketMessageApplier marketMessageApplier;
  @Mock private PostRepository postRepository;

  @Mock private ObjectMapper objectMapper;

  @Mock private MessageEnvelope messageEnvelope;

  @Before
  public void init() throws JsonProcessingException {
    marketMessageApplier = new MarketMessageApplier(objectMapper, postRepository);
    when(objectMapper.readValue(anyString(), eq(MarketStatus.class)))
        .thenReturn(new MarketStatus());
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
    marketMessageApplier.applyUpdate(messageEnvelope);
    Mockito.verify(postRepository, atLeastOnce()).findAll();
    Mockito.verify(postRepository, atLeastOnce()).save(any(PostMessage.class));
  }

  @Test
  public void testChannelMessageApplierType() {
    String type = marketMessageApplier.type();
    Assert.assertEquals("sEVMKT", type);
  }

  @NotNull
  private MarketStatus getMarketStatus() {
    MarketStatus marketStatus = mock(MarketStatus.class);
    when(marketStatus.getActive()).thenReturn(true);
    when(marketStatus.getDisplayed()).thenReturn(true);
    when(marketStatus.getMarketBetInRun()).thenReturn(true);
    when(marketStatus.getLpAvailable()).thenReturn(true);
    when(marketStatus.getSpAvailable()).thenReturn(true);
    return marketStatus;
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
    obEvent.setId("1234");
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
