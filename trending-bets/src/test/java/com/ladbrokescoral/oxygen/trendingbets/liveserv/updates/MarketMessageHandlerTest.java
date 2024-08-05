package com.ladbrokescoral.oxygen.trendingbets.liveserv.updates;

import com.coral.oxygen.middleware.ms.liveserv.client.model.Message;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import org.junit.Assert;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.mockito.Mockito;

class MarketMessageHandlerTest extends AbstractLiveServMessageHandlerTest {

  public MarketMessageApplier marketApplier;

  private String MARKET_STATUS = "{\"status\": \"%s\", \"displayed\": \"%s\"}";

  @ParameterizedTest
  @CsvSource({"true, true", "true, false", "false, true"})
  void testApplyUpdateActive(boolean isTrendingBets, boolean isPersonalized) throws Exception {

    createContext(isTrendingBets, isPersonalized, MARKET_CHANNEL, "sSELCN0235366998");
    handler.handle(prepareMessageEnvolpe(MARKET_CHANNEL, String.format(MARKET_STATUS, "A", "Y")));
    Assert.assertFalse(isSuspended("sSELCN0235366998") && isSuspended(MARKET_CHANNEL));
  }

  @ParameterizedTest
  @CsvSource({"true, true", "true, false", "false, true"})
  void testApplyUpdateInactive(boolean isTrendingBets, boolean isPersonalized) throws Exception {

    createContext(isTrendingBets, isPersonalized, MARKET_CHANNEL, "sSELCN0235366998");
    handler.handle(prepareMessageEnvolpe(MARKET_CHANNEL, String.format(MARKET_STATUS, "S", "Y")));
    Assert.assertTrue(isSuspended("sSELCN0235366998") && isSuspended(MARKET_CHANNEL));
  }

  @Test
  void testApplyUpdateWithEmptyTrendingSelection() throws Exception {
    handler.handle(prepareMessageEnvolpe(MARKET_CHANNEL, String.format(MARKET_STATUS, "S", "Y")));
    Mockito.verify(liveServService, Mockito.times(1)).unsubscribe(MARKET_CHANNEL);
  }

  @Test
  void testApplySelectionUpdateInvalidSelectonStatus() throws Exception {
    handler.handle(new MessageEnvelope(MARKET_CHANNEL, 123456782, new Message("", "{")));
    Mockito.verifyNoInteractions(liveServService);
  }
}
