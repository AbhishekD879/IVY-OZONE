package com.oxygen.publisher.inplay.service;

import static com.oxygen.publisher.inplay.context.InplaySocketMessages.*;
import static com.oxygen.publisher.inplay.context.InplaySocketMessages.VIRTUAL_SPORTS_RIBBON_CHANGED;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.doReturn;
import static org.mockito.Mockito.spy;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;

import com.oxygen.publisher.configuration.JsonSupportConfig;
import com.oxygen.publisher.inplay.context.InplayMiddlewareContext;
import com.oxygen.publisher.model.InplayCachedData;
import com.oxygen.publisher.service.KafkaTopic;
import com.oxygen.publisher.translator.DiagnosticService;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class InplayKafkaRecordConsumerTest {

  private InplayChainFactory chainFactory;
  @Mock InplayMiddlewareContext middlewareContext;
  @Mock InplayDataService dataService;
  private InplayKafkaRecordConsumer consumer;
  private String generation = "5";
  @Mock private InplayCachedData thisCache;
  @Mock private DiagnosticService diagnosticService;

  @Before
  public void setup() {
    chainFactory =
        spy(
            new InplayChainFactory(
                middlewareContext, diagnosticService, new JsonSupportConfig().objectMapper()));
    doReturn(dataService).when(middlewareContext).inplayDataService();
    InplayChainFactory.setInplayChainFactory(chainFactory);

    KafkaTopic kafkaTopic = new KafkaTopic();
    // this init method should not be changed to constructor
    // this is @PostConstruct of Spring
    kafkaTopic.init();

    consumer = spy(new InplayKafkaRecordConsumer(kafkaTopic));
    given(middlewareContext.getInplayCachedData()).willReturn(thisCache);
    given(thisCache.getEntityGUID()).willReturn(generation);
  }

  @Test
  public void onInplayDataChangeTest() {
    consumer.onInplayDataChange(
        new ConsumerRecord<String, String>(
            IN_PLAY_STRUCTURE_CHANGED.messageId(),
            0,
            0,
            IN_PLAY_STRUCTURE_CHANGED.messageId(),
            generation));
    verify(dataService, times(1)).getInPlayModel(eq(generation), any());
  }

  @Test
  public void onSportsRibbonChangeTest() {
    consumer.onSportsRibbonChange(
        new ConsumerRecord<String, String>(
            IN_PLAY_SPORTS_RIBBON_CHANGED.messageId(),
            0,
            0,
            IN_PLAY_SPORTS_RIBBON_CHANGED.messageId(),
            generation));
    verify(dataService, times(1)).getSportsRibbon(eq(generation), any());
  }

  @Test
  public void onSportSegmentsChangeTest() {
    consumer.onSportSegmentsChange(
        new ConsumerRecord<String, String>(
            IN_PLAY_SPORT_SEGMENT_CHANGED.messageId(),
            0,
            0,
            IN_PLAY_SPORT_SEGMENT_CHANGED.messageId(),
            generation));
    verify(dataService, times(1)).getSportSegment(eq(generation), any());
  }

  @Test
  public void onVirtualSportsTest() {
    consumer.onVirtualSportsRibbonChange(
        new ConsumerRecord<>(
            VIRTUAL_SPORTS_RIBBON_CHANGED.messageId(),
            0,
            0,
            VIRTUAL_SPORTS_RIBBON_CHANGED.messageId(),
            generation));
    verify(dataService, times(1)).getVirtualSport(eq(generation), any());
  }
}
