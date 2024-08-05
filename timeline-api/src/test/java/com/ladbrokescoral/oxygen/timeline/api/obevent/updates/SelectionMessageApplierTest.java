package com.ladbrokescoral.oxygen.timeline.api.obevent.updates;

import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
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
import java.util.*;
import org.jetbrains.annotations.NotNull;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class SelectionMessageApplierTest {
  public static final String CHANNEL = "1234567890";
  private SelectionMessageApplier selectionMessageApplier;

  @Mock private PostRepository postRepository;

  @Mock private ObjectMapper objectMapper;

  @Mock private MessageEnvelope messageEnvelope;

  @Before
  public void init() throws JsonProcessingException {
    when(objectMapper.readValue(anyString(), eq(SelectionStatus.class)))
        .thenReturn(new SelectionStatus());
    when(messageEnvelope.getMessage()).thenReturn(new Message("123", "{}"));
    when(messageEnvelope.getChannel()).thenReturn(CHANNEL);

    PostMessage postMessage = PostMessage.builder().build();
    postMessage.setCampaignId("12345");
    postMessage.setCampaignName("abcd");
    postMessage.setPinned(true);
    postMessage.setHeaderText("abcd");
    postMessage.setSpotlight(true);
    postMessage.setId("12345");
    postMessage.setText("hello");
    postMessage.setVerdict(true);
    Instant instant = Instant.now();
    postMessage.setCreatedDate(instant);
    postMessage.setBrand("coral");
    TimelineSelectionEvent timelineSelectionEvent = new TimelineSelectionEvent();
    ObEvent obEvent = new ObEvent();
    obEvent.setId("1234");
    ObOutcome obOutcome = new ObOutcome();
    obOutcome.setId("1234");
    ObMarket obMarket = new ObMarket();
    obMarket.setOutcomes(Arrays.asList(obOutcome));
    obEvent.setMarkets(Arrays.asList(obMarket));
    timelineSelectionEvent.setObEvent(obEvent);
    postMessage.setSelectionEvent(timelineSelectionEvent);

    doReturn(postMessage).when(postRepository).save(any(PostMessage.class));
    doReturn(postMessages()).when(postRepository).findAll();

    selectionMessageApplier = new SelectionMessageApplier(objectMapper, postRepository);
  }

  @Test
  public void testIfPostsWereSearchedWithProperId() {
    selectionMessageApplier.applyUpdate(messageEnvelope);
    Mockito.verify(postRepository, atLeastOnce()).findAll();
    Mockito.verify(postRepository, atLeastOnce()).save(any(PostMessage.class));
  }

  @Test
  public void testChannelMessageApplierType() {
    String type = selectionMessageApplier.type();
    Assert.assertEquals("sSELCN", type);
  }

  @NotNull
  private SelectionStatus getSelectionStatus() {
    SelectionStatus selectionStatus = mock(SelectionStatus.class);
    when(selectionStatus.getActive()).thenReturn(true);
    when(selectionStatus.getDisplayed()).thenReturn(true);
    when(selectionStatus.getSettled()).thenReturn(true);
    when(selectionStatus.getPriceDen()).thenReturn(1);
    when(selectionStatus.getPriceNum()).thenReturn(3);
    return selectionStatus;
  }

  private List<PostMessage> postMessages() {
    List<PostMessage> postMessages = new ArrayList<>();
    TimelineSelectionEvent selectionEvent = new TimelineSelectionEvent();
    ObEvent obEvent = new ObEvent();
    obEvent.setMarkets(
        Arrays.asList(
            new ObMarket() {
              {
                setOutcomes(
                    Arrays.asList(
                        new ObOutcome() {
                          {
                            setId(CHANNEL.substring(6));
                          }
                        }));
              }
            }));

    selectionEvent.setObEvent(obEvent);

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
    obEvent.setId("1234");
    ObOutcome obOutcome = new ObOutcome();
    obOutcome.setId("7890");
    ObMarket obMarket = new ObMarket();
    obMarket.setOutcomes(Arrays.asList(obOutcome));
    obEvent.setMarkets(Arrays.asList(obMarket));
    timelineSelectionEvent.setObEvent(obEvent);
    postMessage.setSelectionEvent(selectionEvent);
    postMessages.add(postMessage);
    return postMessages;
  }
}
