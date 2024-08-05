package com.coral.oxygen.edp.model.mapping;

import static org.mockito.ArgumentMatchers.any;

import com.coral.oxygen.edp.model.mapping.config.SportsConfig;
import com.coral.oxygen.edp.model.output.OutputOutcome;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Outcome;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.core.io.ClassPathResource;

@RunWith(MockitoJUnitRunner.class)
public class OutcomeCorrectedMeaningMinorCodeMapperTest {

  private OutcomeCorrectedMeaningMinorCodeMapper mapper;

  @Mock private OutcomeMapper chain;

  @Before
  public void setUp() {
    Mockito.when(chain.map(any(), any(), any())).thenReturn(new OutputOutcome());
    ObjectMapper objectMapper = new ObjectMapper();
    objectMapper.enable(SerializationFeature.INDENT_OUTPUT);
    SportsConfig sportsConfig =
        new SportsConfig(new ClassPathResource("sportsConfig.json"), objectMapper);
    this.mapper = new OutcomeCorrectedMeaningMinorCodeMapper(chain, sportsConfig);
  }

  @Test
  public void testH() {
    // preparation
    Event event = new Event();

    Outcome outcome = new Outcome();
    outcome.setOutcomeMeaningMinorCode("H");

    // action
    OutputOutcome outputOutcome = mapper.map(event, null, outcome);

    // verification
    Assert.assertEquals(1, outputOutcome.getCorrectedOutcomeMeaningMinorCode().intValue());
  }

  @Test
  public void testHisUS() {
    // preparation
    Event event = new Event();
    event.setTypeFlagCodes("US");

    Outcome outcome = new Outcome();
    outcome.setOutcomeMeaningMinorCode("H");

    // action
    OutputOutcome outputOutcome = mapper.map(event, null, outcome);

    // verification
    Assert.assertEquals(3, outputOutcome.getCorrectedOutcomeMeaningMinorCode().intValue());
  }

  @Test
  public void testA() {
    // preparation
    Event event = new Event();

    Outcome outcome = new Outcome();
    outcome.setOutcomeMeaningMinorCode("A");

    // action
    OutputOutcome outputOutcome = mapper.map(event, null, outcome);

    // verification
    Assert.assertEquals(3, outputOutcome.getCorrectedOutcomeMeaningMinorCode().intValue());
  }

  @Test
  public void testAisUS() {
    // preparation
    Event event = new Event();
    event.setTypeFlagCodes("US");

    Outcome outcome = new Outcome();
    outcome.setOutcomeMeaningMinorCode("A");

    // action
    OutputOutcome outputOutcome = mapper.map(event, null, outcome);

    // verification
    Assert.assertEquals(1, outputOutcome.getCorrectedOutcomeMeaningMinorCode().intValue());
  }

  @Test
  public void testD() {
    // preparation
    Event event = new Event();

    Outcome outcome = new Outcome();
    outcome.setOutcomeMeaningMinorCode("D");

    // action
    OutputOutcome outputOutcome = mapper.map(event, null, outcome);

    // verification
    Assert.assertEquals(2, outputOutcome.getCorrectedOutcomeMeaningMinorCode().intValue());
  }

  @Test
  public void testN() {
    // preparation
    Event event = new Event();

    Outcome outcome = new Outcome();
    outcome.setOutcomeMeaningMinorCode("N");

    // action
    OutputOutcome outputOutcome = mapper.map(event, null, outcome);

    // verification
    Assert.assertEquals(2, outputOutcome.getCorrectedOutcomeMeaningMinorCode().intValue());
  }

  @Test
  public void testL() {
    // preparation
    Event event = new Event();

    Outcome outcome = new Outcome();
    outcome.setOutcomeMeaningMinorCode("L");

    // action
    OutputOutcome outputOutcome = mapper.map(event, null, outcome);

    // verification
    Assert.assertEquals(2, outputOutcome.getCorrectedOutcomeMeaningMinorCode().intValue());
  }

  @Test
  public void testYesOutcomeName() {
    // preparation
    Event event = new Event();
    event.setName("");

    Outcome outcome = new Outcome();
    outcome.setName("YES");

    // action
    OutputOutcome outputOutcome = mapper.map(event, null, outcome);

    // verification
    Assert.assertEquals(1, outputOutcome.getCorrectedOutcomeMeaningMinorCode().intValue());
  }

  @Test
  public void testNoOutcomeName() {
    // preparation
    Event event = new Event();
    event.setName("");

    Outcome outcome = new Outcome();
    outcome.setName("NO");

    // action
    OutputOutcome outputOutcome = mapper.map(event, null, outcome);

    // verification
    Assert.assertEquals(3, outputOutcome.getCorrectedOutcomeMeaningMinorCode().intValue());
  }

  @Test
  public void testHomeByName() {
    // preparation
    Event event = eventAvsB();

    Outcome outcome = new Outcome();
    outcome.setName("A");

    // action
    OutputOutcome outputOutcome = mapper.map(event, null, outcome);

    // verification
    Assert.assertEquals(1, outputOutcome.getCorrectedOutcomeMeaningMinorCode().intValue());
  }

  @Test
  public void testAwayByName() {
    // preparation
    Event event = eventAvsB();

    Outcome outcome = new Outcome();
    outcome.setName("B");

    // action
    OutputOutcome outputOutcome = mapper.map(event, null, outcome);

    // verification
    Assert.assertEquals(3, outputOutcome.getCorrectedOutcomeMeaningMinorCode().intValue());
  }

  @Test
  public void testNulRacing() {
    // preparation
    Event event = eventAvsB();
    event.setCategoryId("19");

    Outcome outcome = new Outcome();
    outcome.setName("B");

    // action
    OutputOutcome outputOutcome = mapper.map(event, null, outcome);

    // verification
    Assert.assertNull(outputOutcome.getCorrectedOutcomeMeaningMinorCode());
  }

  @Test
  public void testHLandL() {
    // preparation
    Outcome outcome = new Outcome();
    outcome.setOutcomeMeaningMinorCode("L");
    outcome.setOutcomeMeaningMajorCode("HL");

    // action
    OutputOutcome outputOutcome = mapper.map(eventAvsB(), null, outcome);

    // verification
    Assert.assertEquals(3, outputOutcome.getCorrectedOutcomeMeaningMinorCode().intValue());
  }

  @Test
  public void testHLAndNoL() {
    // preparation
    Outcome outcome = new Outcome();
    outcome.setOutcomeMeaningMajorCode("HL");

    // action
    OutputOutcome outputOutcome = mapper.map(eventAvsB(), null, outcome);

    // verification
    Assert.assertEquals(3, outputOutcome.getCorrectedOutcomeMeaningMinorCode().intValue());
  }

  @Test
  public void testYesOutcomeNameAndHyphenMajorCode() {
    // preparation
    Outcome outcome = new Outcome();
    outcome.setName("Yes");
    outcome.setOutcomeMeaningMinorCode("D");
    outcome.setOutcomeMeaningMajorCode("--");

    // action
    OutputOutcome outputOutcome = mapper.map(eventAvsB(), null, outcome);

    // verification
    Assert.assertEquals(1, outputOutcome.getCorrectedOutcomeMeaningMinorCode().intValue());
  }

  @Test
  public void testNoOutcomeNameAndHyphenMajorCode() {
    // preparation
    Outcome outcome = new Outcome();
    outcome.setName("No");
    outcome.setOutcomeMeaningMinorCode("D");
    outcome.setOutcomeMeaningMajorCode("--");

    // action
    OutputOutcome outputOutcome = mapper.map(eventAvsB(), null, outcome);

    // verification
    Assert.assertEquals(3, outputOutcome.getCorrectedOutcomeMeaningMinorCode().intValue());
  }

  @Test
  public void testIntegerMinorCode() {
    Outcome outcome = new Outcome();
    outcome.setOutcomeMeaningMinorCode("1");

    // action
    OutputOutcome outputOutcome = mapper.map(eventAvsB(), null, outcome);

    // verification
    Assert.assertEquals(1, outputOutcome.getCorrectedOutcomeMeaningMinorCode().intValue());
  }

  private Event eventAvsB() {
    Event event = new Event();
    event.setName("A vs B");
    return event;
  }
}
