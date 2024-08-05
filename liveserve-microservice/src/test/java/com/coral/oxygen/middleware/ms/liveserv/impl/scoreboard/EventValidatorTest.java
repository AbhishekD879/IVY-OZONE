package com.coral.oxygen.middleware.ms.liveserv.impl.scoreboard;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import com.coral.oxygen.middleware.ms.liveserv.model.scoreboard.ScoreboardEvent;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class EventValidatorTest {

  private EventValidator eventValidator;

  @Before
  public void setup() {
    eventValidator = new EventValidator(new FootballValidator());
  }

  @Test
  public void footballValidTest() {
    String data =
        "{\"football\" : {\"provider\" : \"opta\", \"sequenceId\" : 1, \"period\" : \"1h\"}}";

    ScoreboardEvent scoreboardEvent = new ScoreboardEvent("123123", data);
    boolean valid = eventValidator.validate(scoreboardEvent);

    assertTrue(valid);
  }

  @Test
  public void invalidFootballPeriodTest() {
    String data =
        "{\"football\" : {\"provider\" : \"opta\", \"sequenceId\" : 1, \"period\" : \"pre\"}}";

    ScoreboardEvent scoreboardEvent = new ScoreboardEvent("123123", data);
    boolean valid = eventValidator.validate(scoreboardEvent);

    assertFalse(valid);
  }

  @Test
  public void invalidFootballPeriodTestForETHT() {
    String data =
        "{\"football\" : {\"provider\" : \"opta\", \"sequenceId\" : 1, \"period\" : \"ETHT\"}}";

    ScoreboardEvent scoreboardEvent = new ScoreboardEvent("123123", data);
    boolean valid = eventValidator.validate(scoreboardEvent);

    assertFalse(valid);
  }

  @Test
  public void invalidFootballProviderTest() {
    String data = "{\"football\" : {\"provider\" : \"not-opta\", \"sequenceId\" : 1}}";

    ScoreboardEvent scoreboardEvent = new ScoreboardEvent("123123", data);
    boolean valid = eventValidator.validate(scoreboardEvent);

    assertFalse(valid);
  }

  @Test
  public void invalidSportTest() {
    String data = "{\"basketball\" : {\"provider\" : \"opta\", \"sequenceId\" : 1}}";

    ScoreboardEvent scoreboardEvent = new ScoreboardEvent("123123", data);
    boolean valid = eventValidator.validate(scoreboardEvent);

    assertFalse(valid);
  }
}
