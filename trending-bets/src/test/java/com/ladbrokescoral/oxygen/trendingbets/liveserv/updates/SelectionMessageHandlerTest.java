package com.ladbrokescoral.oxygen.trendingbets.liveserv.updates;

import com.coral.oxygen.middleware.ms.liveserv.client.model.Message;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.ladbrokescoral.oxygen.trendingbets.context.TrendingBetsContext;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingEvent;
import java.util.List;
import org.junit.Assert;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.mockito.Mockito;

class SelectionMessageHandlerTest extends AbstractLiveServMessageHandlerTest {

  public SelectionMessageApplier selectionApplier;

  private String SELECTION_MSG_PAYLOAD =
      "{ \"status\": \"%s\", \"settled\": \"N\", \"result\": \"-\", \"displayed\": \"Y\",  \"lp_num\": \"%s\", \"lp_den\": \"%s\"}\n";

  private String SELECTION_MSG_PAYLOAD_NO_NUM =
      "{ \"status\": \"%s\", \"settled\": \"N\", \"result\": \"-\", \"displayed\": \"Y\",  \"lp_den\": \"%s\"}\n";

  private String SELECTION_MSG_PAYLOAD_NO_DEN =
      "{ \"status\": \"%s\", \"settled\": \"N\", \"result\": \"-\", \"displayed\": \"Y\",  \"lp_num\": \"%s\"}\n";

  private String SELECTION_MSG_PAYLOAD_PB = "{\"stream_type\": \"PRICE_BOOST\"}";

  @ParameterizedTest
  @CsvSource({"true, true", "true, false", "false, true"})
  void testApplySelectionUpdateActiveforTrendingBets(boolean isTrendingBets, boolean isPersonalized)
      throws Exception {

    createContext(isTrendingBets, isPersonalized, SEL_CHANNEL);
    TrendingBetsContext.getPopularSelections().put(SEL_CHANNEL, List.of(getTrendingSelection()));
    handler.handle(
        prepareMessageEnvolpe(SEL_CHANNEL, String.format(SELECTION_MSG_PAYLOAD, "A", "5", "2")));
    Assert.assertFalse(isSuspended(SEL_CHANNEL));
  }

  @ParameterizedTest
  @CsvSource({"true, true", "true, false", "false, true"})
  void testApplySelectionUpdateInactive(boolean isTrendingBets, boolean isPersonalized)
      throws Exception {

    createContext(isTrendingBets, isPersonalized, SEL_CHANNEL);
    handler.handle(
        prepareMessageEnvolpe(SEL_CHANNEL, String.format(SELECTION_MSG_PAYLOAD, "S", "5", "2")));
    Assert.assertTrue(isSuspended(SEL_CHANNEL));
  }

  @ParameterizedTest
  @CsvSource({"true, true", "true, false", "false, true"})
  void testApplySelectionUpdatePriceUpdate(boolean isTrendingBets, boolean isPersonalized)
      throws Exception {

    createContext(isTrendingBets, isPersonalized, SEL_CHANNEL);
    handler.handle(
        prepareMessageEnvolpe(SEL_CHANNEL, String.format(SELECTION_MSG_PAYLOAD, "A", "5", "2")));
    TrendingEvent selection = null;
    if (isTrendingBets)
      selection = TrendingBetsContext.getPopularSelections().get(SEL_CHANNEL).get(0);
    else if (isPersonalized)
      selection = TrendingBetsContext.getPersonalizedSelections().get(SEL_CHANNEL).get(0);

    Assert.assertEquals(
        5,
        selection
            .getMarkets()
            .get(0)
            .getOutcomes()
            .get(0)
            .getPrices()
            .get(0)
            .getPriceNum()
            .intValue());
    Assert.assertEquals(
        2,
        selection
            .getMarkets()
            .get(0)
            .getOutcomes()
            .get(0)
            .getPrices()
            .get(0)
            .getPriceDen()
            .intValue());
  }

  @Test
  void testApplySelectionUpdateWithEmptyTrendingSelection() throws Exception {
    handler.handle(
        prepareMessageEnvolpe(SEL_CHANNEL, String.format(SELECTION_MSG_PAYLOAD, "S", "5", "2")));
    Mockito.verify(liveServService, Mockito.times(1)).unsubscribe(SEL_CHANNEL);
  }

  @Test
  void testApplySelectionUpdateWithPriceBoostTrendingSelection() throws Exception {
    TrendingBetsContext.getPopularSelections().put(SEL_CHANNEL, List.of(getTrendingSelection()));
    handler.handle(prepareMessageEnvolpe(SEL_CHANNEL, SELECTION_MSG_PAYLOAD_PB));
    Mockito.verifyNoInteractions(liveServService);
  }

  @Test
  void testApplySelectionUpdateWithPriceBoostPersonilzedSelection() throws Exception {
    TrendingBetsContext.getPopularSelections().put(SEL_CHANNEL, List.of(getTrendingSelection()));
    handler.handle(prepareMessageEnvolpe(SEL_CHANNEL, SELECTION_MSG_PAYLOAD_PB));
    Mockito.verifyNoInteractions(liveServService);
  }

  @Test
  void testApplySelectionUpdateInvalidSelectonStatus() throws Exception {
    handler.handle(new MessageEnvelope(SEL_CHANNEL, 123456782, new Message("", "{")));
    Mockito.verifyNoInteractions(liveServService);
  }

  @ParameterizedTest
  @CsvSource({"true, true", "true, false", "false, true"})
  void testApplySelectionUpdateNumNull(boolean isTrendingBets, boolean isPersonalized)
      throws Exception {

    createContext(isTrendingBets, isPersonalized, SEL_CHANNEL);
    handler.handle(
        prepareMessageEnvolpe(SEL_CHANNEL, String.format(SELECTION_MSG_PAYLOAD_NO_NUM, "A", "2")));
    Assert.assertFalse(isSuspended(SEL_CHANNEL));
  }
}
