package com.coral.oxygen.middleware.in_play.service;

import com.coral.oxygen.middleware.in_play.service.scoreboards.ScoreboardEvent;
import org.junit.Test;
import org.junit.jupiter.api.Assertions;

public class ScoreBoardEventTest {

  @Test
  public void testScoreBoardEventStuctureNull() {
    ScoreboardEvent scoreboardEvent = new ScoreboardEvent("112233", "");
    Assertions.assertDoesNotThrow(scoreboardEvent::getRawStructure);
  }
}
