package com.ladbrokescoral.oxygen.trendingbets.liveserv.updates;

import com.coral.oxygen.middleware.ms.liveserv.client.model.Message;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.Unsubscribed;
import com.ladbrokescoral.oxygen.trendingbets.context.TrendingBetsContext;
import org.junit.Assert;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.mockito.Mockito;

class EventMessageHandlerTest extends AbstractLiveServMessageHandlerTest {

  public EventMessageApplier applier;

  private String EVENT_STATUS =
      "{\"status\": \"%s\", \"displayed\": \"Y\",  \"start_time\": \"2023-09-08 22:46:00\", \"started\": \"%s\", \"result_conf\": \"Y\"}\n";

  private String EVENT_STATUS_GMT =
      "{\"status\": \"%s\", \"displayed\": \"Y\",  \"start_time\": \"2023-09-08T22:46:00Z\", \"started\": \"%s\", \"result_conf\": \"Y\"}\n";

  @ParameterizedTest
  @CsvSource({"true, true", "true, false", "false, true"})
  void testApplyUpdateActiveAndNotStarted(boolean isTrendingBets, boolean isPersonalized) {

    createContext(
        isTrendingBets, isPersonalized, "sSELCN0235366998", MARKET_CHANNEL, EVENT_CHANNEL);
    handler.handle(prepareMessageEnvolpe(EVENT_CHANNEL, String.format(EVENT_STATUS, "A", "N")));
    Assert.assertFalse(
        isSuspended(MARKET_CHANNEL)
            && isSuspended(EVENT_CHANNEL)
            && isSuspended("sSELCN0235366998"));
    Assert.assertFalse(
        isEventLive("sSELCN0235366998")
            && isEventLive(MARKET_CHANNEL)
            && isEventLive(EVENT_CHANNEL));
  }

  @ParameterizedTest
  @CsvSource({"true, true", "true, false", "false, true"})
  void testApplyUpdateInactive(boolean isTrendingBets, boolean isPersonalized) {

    createContext(
        isTrendingBets, isPersonalized, "sSELCN0235366998", MARKET_CHANNEL, EVENT_CHANNEL);
    handler.handle(prepareMessageEnvolpe(EVENT_CHANNEL, String.format(EVENT_STATUS, "S", "N")));
    Assert.assertTrue(
        isSuspended("sSELCN0235366998")
            && isSuspended(MARKET_CHANNEL)
            && isSuspended(EVENT_CHANNEL));
  }

  @ParameterizedTest
  @CsvSource({"true, true", "true, false", "false, true"})
  void testApplyUpdateEventStartedActive(boolean isTrendingBets, boolean isPersonalized) {

    createContext(
        isTrendingBets, isPersonalized, "sSELCN0235366998", MARKET_CHANNEL, EVENT_CHANNEL);
    handler.handle(prepareMessageEnvolpe(EVENT_CHANNEL, String.format(EVENT_STATUS_GMT, "A", "Y")));
    Assert.assertEquals(0, TrendingBetsContext.getPopularSelections().size());
    Assert.assertEquals(0, TrendingBetsContext.getPersonalizedSelections().size());
  }

  @Test
  void testApplyUpdateWithEmptyTrendingSelection() {
    handler.handle(prepareMessageEnvolpe(EVENT_CHANNEL, String.format(EVENT_STATUS, "S", "Y")));
    Mockito.verify(liveServService, Mockito.times(1)).unsubscribe(EVENT_CHANNEL);
  }

  @Test
  void testApplySelectionUpdateInvalidSelectonStatus() {
    handler.handle(new MessageEnvelope(EVENT_CHANNEL, 123456782, new Message("", "{")));
    Mockito.verifyNoInteractions(liveServService);
  }

  @Test
  void testApplySelectionUpdateInvalidEventType() {
    handler.handle(new Unsubscribed(EVENT_CHANNEL, 123456782));
    Mockito.verifyNoInteractions(liveServService);
  }

  @Test
  void testApplySelectionUpdateInvalidApplier() {

    MessageEnvelope messageEnvelope =
        new MessageEnvelope(EVENT_CHANNEL_INVALID, 123456782, new Message("", "{"));
    Assert.assertThrows(IllegalArgumentException.class, () -> handler.handle(messageEnvelope));
  }
}
