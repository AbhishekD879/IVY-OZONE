package com.coral.oxygen.edp.model.mapping;

import static junit.framework.TestCase.fail;
import static org.mockito.ArgumentMatchers.any;

import com.coral.oxygen.edp.model.mapping.converter.OrdinalToNumberConverter;
import com.coral.oxygen.edp.model.output.OutputMarket;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.core.io.ClassPathResource;

@RunWith(MockitoJUnitRunner.class)
public class MarketNextScoreMapperTest {

  private MarketNextScoreMapper mapper;
  private static final String ORDINAL_TO_NUMBER_RESOURCE = "ordinalToNumber.json";

  @Mock private MarketMapper chain;

  @Before
  public void setUp() {
    Mockito.when(chain.map(any(), any())).thenReturn(new OutputMarket());
    OrdinalToNumberConverter ordinalToNumberConverter =
        new OrdinalToNumberConverter(
            new ClassPathResource(ORDINAL_TO_NUMBER_RESOURCE), new ObjectMapper());
    mapper = new MarketNextScoreMapper(chain, ordinalToNumberConverter);
  }

  private Event footballEvent() {
    Event event = new Event();
    event.setCategoryCode("FOOTBALL");
    return event;
  }

  private Market marketNextTeamToScore() {
    Market market = new Market();
    market.setTemplateMarketName("Next Team to Score");
    return market;
  }

  @Test
  public void testMatchNotMatchFootballCategory() {
    // preparation
    Event event = new Event();
    Market market = marketNextTeamToScore();

    // action
    OutputMarket outputMarket = mapper.map(event, market);

    // verification
    Assert.assertNull(outputMarket.getNextScore());
  }

  @Test
  public void testNotMatchNextScoreMarketName() {
    // preparation
    Market market = new Market();
    Event event = footballEvent();

    // action
    OutputMarket outputMarket = mapper.map(event, market);

    // verification
    Assert.assertNull(outputMarket.getNextScore());
  }

  @Test
  public void testNumberAtTheEndOfMarketName() {
    // preparation
    Event event = footballEvent();
    Market market = marketNextTeamToScore();
    market.setName("Next Team To Score Goal 15");

    // action
    OutputMarket outputMarket = mapper.map(event, market);

    // verification
    Assert.assertEquals(15, outputMarket.getNextScore().intValue());
  }

  @Test
  public void testNumberAtTheEndOfMarketNameWithNoSpace() {
    // preparation
    Event event = footballEvent();
    Market market = marketNextTeamToScore();
    market.setName("Next Team To Score Goal15");

    // action
    OutputMarket outputMarket = mapper.map(event, market);

    // verification
    Assert.assertNull(outputMarket.getNextScore());
  }

  @Test
  public void testTextOnStartOfMarketName() {
    // preparation
    Event event = footballEvent();
    Market market = marketNextTeamToScore();
    market.setName("Thirtieth Team to Score");

    // action
    OutputMarket outputMarket = mapper.map(event, market);

    // verification
    Assert.assertEquals(30, outputMarket.getNextScore().intValue());
  }

  @Test
  public void testTextOnStartOfMarketNameWithInappropriateCase() {
    // preparation
    Event event = footballEvent();
    Market market = marketNextTeamToScore();
    market.setName("twEnty-ThiRD Team to Score");

    // action
    OutputMarket outputMarket = mapper.map(event, market);

    // verification
    Assert.assertEquals(23, outputMarket.getNextScore().intValue());
  }

  @Test
  public void testTextOnStartOfMarketNameIsGraterThen40OrInvalid() {
    // preparation
    Event event = footballEvent();
    Market market = marketNextTeamToScore();
    market.setName("InvalidOrdinalNumber Team to Score");

    // action
    OutputMarket outputMarket = mapper.map(event, market);

    // verification
    Assert.assertNull(outputMarket.getNextScore());
  }

  @Test
  public void testMarketNameIsEmpty() {
    // preparation
    Event event = footballEvent();
    Market market = marketNextTeamToScore();
    market.setName("");

    // action
    OutputMarket outputMarket = mapper.map(event, market);

    // verification
    Assert.assertNull(outputMarket.getNextScore());
  }

  @Test
  public void testNoTextOnStartAndNoNumberAtTheEnd() {
    // preparation
    Event event = footballEvent();
    Market market = marketNextTeamToScore();
    market.setName("Next Team to Score");

    // action
    OutputMarket outputMarket = mapper.map(event, market);

    // verification
    Assert.assertNull(outputMarket.getNextScore());
  }

  @Test
  public void testAllKnownOrdinalNumbersAreParsedCorrectly() {
    // preparation
    Event event = footballEvent();
    List<Market> markets = new ArrayList<>();
    try {
      InputStream inputStream =
          getClass().getClassLoader().getResourceAsStream(ORDINAL_TO_NUMBER_RESOURCE);
      Map<String, Integer> ordinalNumberMap =
          new ObjectMapper().readValue(inputStream, new TypeReference<Map<String, Integer>>() {});
      ordinalNumberMap.forEach(
          (ordinal, number) -> {
            Market market = marketNextTeamToScore();
            market.setName(ordinal + " Team to Score");
            markets.add(market);
          });
    } catch (IOException e) {
      fail();
    }

    markets.forEach(
        market -> {
          // action
          OutputMarket outputMarket = mapper.map(event, market);

          // verification
          Assert.assertNotNull(outputMarket.getNextScore());
        });
  }

  @Test
  public void testExceededIntegerRange() {
    Event event = footballEvent();
    Market market = marketNextTeamToScore();
    market.setName("market 3234567890");

    // action
    OutputMarket outputMarket = mapper.map(event, market);

    // verification
    Assert.assertNull(outputMarket.getNextScore());
  }
}
