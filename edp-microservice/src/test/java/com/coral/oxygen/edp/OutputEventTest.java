package com.coral.oxygen.edp;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;

import com.coral.oxygen.edp.model.output.Clock;
import com.coral.oxygen.edp.model.output.OutputEvent;
import com.coral.oxygen.edp.model.output.OutputMarket;
import com.coral.oxygen.edp.model.output.OutputOutcome;
import com.coral.oxygen.edp.model.output.OutputPrice;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import org.junit.Test;

public class OutputEventTest {

  @Test
  public void shouldCopyEventWithSmallMarketLimit() {
    OutputEvent event = createOutputEvent();
    OutputEvent copy = event.getCopyWithMarketLimit(1);

    assertEquals("SomeName", copy.getName());
    assertNotNull(copy.getInitClock());
    assertEquals("last_update", copy.getInitClock().getLastUpdate());
    assertNotNull(copy.getMarkets());
    assertEquals(1, copy.getMarkets().size());
    OutputMarket copyMarket = copy.getMarkets().get(0);
    assertEquals("market_id_1", copyMarket.getId());
    assertEquals(1, copyMarket.getOutcomes().size());
    OutputOutcome copyOutcome = copyMarket.getOutcomes().get(0);
    assertEquals("outcome_id", copyOutcome.getId());
    assertEquals(1, copyOutcome.getPrices().size());
    assertEquals("outcome_price_id", copyOutcome.getPrices().get(0).getId());
  }

  @Test
  public void shouldCopyEventWithLargeMarketLimit() {
    OutputEvent event = createOutputEvent();

    OutputEvent copy = event.getCopyWithMarketLimit(5);
    assertNotNull(copy.getMarkets());
    assertEquals(3, copy.getMarkets().size());
  }

  @Test
  public void shouldCopyEventWithTemplateWithSmallMarketLimit() {
    OutputEvent event = createOutputEventWithTemplate();

    OutputEvent copy = event.getCopyWithMarketLimit(1);
    assertEquals(3, copy.getMarkets().size());
  }

  @Test
  public void shouldCopyEventWithTemplateWithLargeMarketLimit() {
    OutputEvent event = createOutputEventWithTemplate();

    OutputEvent copy = event.getCopyWithMarketLimit(2);
    assertEquals(4, copy.getMarkets().size());
  }

  private OutputEvent createOutputEvent() {
    OutputEvent event = new OutputEvent();
    List<OutputMarket> marketsList = new ArrayList<>();
    OutputMarket market1 = new OutputMarket();
    market1.setId("market_id_1");
    List<OutputOutcome> outcomes = new ArrayList<>();
    OutputOutcome outcome = new OutputOutcome();
    outcome.setId("outcome_id");
    List<OutputPrice> prices = new ArrayList<>();
    OutputPrice price = new OutputPrice();
    price.setId("outcome_price_id");
    prices.add(price);
    outcome.setPrices(prices);
    outcomes.add(outcome);
    market1.setOutcomes(outcomes);

    OutputMarket market2 = new OutputMarket();
    market2.setId("market_id_2");

    OutputMarket market3 = new OutputMarket();
    market3.setId("market_id_3");

    marketsList.add(market1);
    marketsList.add(market2);
    marketsList.add(market3);

    event.setMarketsByTemplateMarket(
        Arrays.asList(
            Collections.singletonList(market1),
            Collections.singletonList(market2),
            Collections.singletonList(market3)));
    event.setMarketsCount(marketsList.size());
    event.setName("SomeName");
    Clock clock = new Clock();
    clock.setLastUpdate("last_update");
    event.setInitClock(clock);

    return event;
  }

  private OutputEvent createOutputEventWithTemplate() {
    OutputEvent event = createOutputEvent();
    Collection<List<OutputMarket>> marketsByTemplate = new ArrayList<>();
    List<OutputMarket> outputMarkets1 = new ArrayList<>();
    OutputMarket market1 = new OutputMarket();
    OutputMarket market2 = new OutputMarket();
    OutputMarket market3 = new OutputMarket();
    outputMarkets1.add(market1);
    outputMarkets1.add(market2);
    outputMarkets1.add(market3);
    marketsByTemplate.add(outputMarkets1);

    List<OutputMarket> outputMarkets2 = new ArrayList<>();
    OutputMarket market4 = new OutputMarket();
    outputMarkets2.add(market4);
    marketsByTemplate.add(outputMarkets2);
    event.setMarketsByTemplateMarket(marketsByTemplate);

    return event;
  }
}
