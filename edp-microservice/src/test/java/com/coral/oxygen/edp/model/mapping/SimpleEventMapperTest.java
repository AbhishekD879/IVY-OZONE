package com.coral.oxygen.edp.model.mapping;

import com.coral.oxygen.edp.TestUtil;
import com.coral.oxygen.edp.model.mapping.converter.MarketGroupAndSortConverter;
import com.coral.oxygen.edp.model.output.OutputEvent;
import com.coral.oxygen.edp.model.output.OutputMarket;
import com.egalacoral.spark.siteserver.model.Event;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.util.stream.Collectors;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.test.context.TestPropertySource;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

@RunWith(SpringJUnit4ClassRunner.class)
@TestPropertySource(
    properties = {
      "markets.top=5",
    })
public class SimpleEventMapperTest {

  @Value("${markets.top}")
  private int topMarkets;

  @Test
  public void testWithFootballEvent() throws IOException {
    Event event = deserializeEventFromFile("SimpleEventMapperTest/event.json");

    MarketMapper marketMapper = new SimpleMarketMapper(new SimpleOutcomeMapper());
    MarketGroupAndSortConverter marketGroupAndSortConverter = new MarketGroupAndSortConverter();

    SimpleEventMapper mapper =
        new SimpleEventMapper(
            marketMapper, marketGroupAndSortConverter, TestUtil.virtualRacingIds());

    OutputEvent outputEvent = new OutputEvent();
    mapper.map(outputEvent, event);
    outputEvent = outputEvent.getCopyWithMarketLimit(1000);

    Assert.assertEquals(Long.valueOf(9378011), outputEvent.getId());
    Assert.assertEquals("Singida United v Zimamoto SC", outputEvent.getName());
    Assert.assertEquals("A", outputEvent.getEventStatusCode());
    Assert.assertEquals("MTCH", outputEvent.getEventSortCode());
    Assert.assertEquals("2018-01-02T11:30:00Z", outputEvent.getStartTime());
    Assert.assertEquals("sEVENT0009378011,", outputEvent.getLiveServChannels());
    Assert.assertEquals("SEVENT0009378011,", outputEvent.getLiveServChildrenChannels());
    Assert.assertEquals("16", outputEvent.getCategoryId());
    Assert.assertEquals("FOOTBALL", outputEvent.getCategoryCode());
    Assert.assertEquals("Football", outputEvent.getCategoryName());
    Assert.assertEquals("Mapinduzi Cup", outputEvent.getTypeName());
    Assert.assertEquals("Y", outputEvent.getCashoutAvail());
    Assert.assertEquals(Integer.valueOf(0), outputEvent.getDisplayOrder());
    Assert.assertNull(outputEvent.getIsFinished());
    Assert.assertEquals("EVFLAG_PDM,EVFLAG_BL,", outputEvent.getDrilldownTagNames());
    Assert.assertEquals("32934", outputEvent.getTypeId());
    Assert.assertEquals(2, outputEvent.getMarkets().size());
    Assert.assertEquals(13, outputEvent.getMarkets().get(0).getDisplayOrder().intValue());
    Assert.assertEquals(14, outputEvent.getMarkets().get(1).getDisplayOrder().intValue());
  }

  @Test
  public void testWithNonFootballEvent() throws IOException {
    Event event = deserializeEventFromFile("SimpleEventMapperTest/tennis_event.json");

    MarketMapper marketMapper = new SimpleMarketMapper(new SimpleOutcomeMapper());
    MarketGroupAndSortConverter marketGroupAndSortConverter = new MarketGroupAndSortConverter();
    SimpleEventMapper mapper =
        new SimpleEventMapper(
            marketMapper, marketGroupAndSortConverter, TestUtil.virtualRacingIds());

    OutputEvent outputEvent = new OutputEvent();
    mapper.map(outputEvent, event);

    Assert.assertEquals(Long.valueOf(8293333), outputEvent.getId());
    Assert.assertEquals(6, outputEvent.getMarkets().size());
    Assert.assertEquals(1, outputEvent.getMarkets().get(0).getDisplayOrder().intValue());
    Assert.assertEquals(3, outputEvent.getMarkets().get(1).getDisplayOrder().intValue());
    Assert.assertEquals(4, outputEvent.getMarkets().get(2).getDisplayOrder().intValue());
    Assert.assertEquals(100, outputEvent.getMarkets().get(3).getDisplayOrder().intValue());
    Assert.assertEquals(110, outputEvent.getMarkets().get(4).getDisplayOrder().intValue());
  }

  @Test
  public void testMarketsOrdering() throws IOException {
    List<Integer> sortedMarketsByDispOrderOrId = new ArrayList<>();
    Scanner scanner =
        new Scanner(
            this.getClass()
                .getClassLoader()
                .getResourceAsStream("SimpleEventMapperTest/eventIds.txt"));
    while (scanner.hasNextInt()) {
      sortedMarketsByDispOrderOrId.add(scanner.nextInt());
    }
    Event event = deserializeEventFromFile("SimpleEventMapperTest/event_groupedMarkets.json");

    OutcomeMapper outcomeMapper = new SimpleOutcomeMapper();
    SimpleMarketMapper marketMapper = new SimpleMarketMapper(outcomeMapper);
    event.getMarkets().stream().map(m -> marketMapper.map(event, m)).collect(Collectors.toList());
    MarketGroupAndSortConverter marketGroupAndSortConverter = new MarketGroupAndSortConverter();

    SimpleEventMapper mapper =
        new SimpleEventMapper(
            marketMapper, marketGroupAndSortConverter, TestUtil.virtualRacingIds());
    OutputEvent outputEvent = new OutputEvent();
    mapper.map(outputEvent, event);

    List<Integer> ids =
        outputEvent.getMarkets().stream()
            .map(OutputMarket::getId)
            .map(Integer::valueOf)
            .collect(Collectors.toList());

    Assert.assertEquals(155, outputEvent.getMarkets().size());
    Assert.assertEquals(sortedMarketsByDispOrderOrId, ids);
  }

  @Test
  public void testMarketsCount() throws IOException {
    Event event = deserializeEventFromFile("SimpleEventMapperTest/event_MarketsCount.json");

    MarketMapper marketMapper = new SimpleMarketMapper(new SimpleOutcomeMapper());
    MarketGroupAndSortConverter marketGroupAndSortConverter = new MarketGroupAndSortConverter();

    SimpleEventMapper mapper =
        new SimpleEventMapper(
            marketMapper, marketGroupAndSortConverter, TestUtil.virtualRacingIds());

    OutputEvent outputEvent = new OutputEvent();
    mapper.map(outputEvent, event);

    Assert.assertEquals(35, event.getMarkets().size());
    Assert.assertEquals(Integer.valueOf(31), outputEvent.getMarketsCount());
  }

  private Event deserializeEventFromFile(String resourcePath) throws IOException {
    return TestUtil.deserializeFromFile(resourcePath, Event.class);
  }
}
