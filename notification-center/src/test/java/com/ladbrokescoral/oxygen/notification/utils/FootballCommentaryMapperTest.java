package com.ladbrokescoral.oxygen.notification.utils;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertTrue;

import com.egalacoral.spark.siteserver.model.Event;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.ladbrokescoral.oxyegn.test.utils.Utils;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.EventScores;
import java.util.Objects;
import org.junit.Before;
import org.junit.Test;

public class FootballCommentaryMapperTest {

  private Gson gson;

  @Before
  public void setUp() {
    gson = new GsonBuilder().create();
  }

  @Test
  public void testConvertToEventScoresNoSubPeriodsNoFacts() {
    Event commentaryEvent =
        Utils.fromFile(
            gson,
            "ssEvents/commentary_no_subperiods_no_facts.json",
            com.egalacoral.spark.siteserver.model.Event.class);
    EventScores eventScores = FootballCommentaryMapper.toEventScores(commentaryEvent);

    assertNotNull(eventScores);
    assertEquals(2, eventScores.getTeams().size());
    assertTrue(eventScores.getTeams().stream().allMatch(t -> t.getScore() == 0));
    assertTrue(eventScores.getTeams().stream().allMatch(t -> Objects.nonNull(t.getName())));
  }

  @Test
  public void testConvertToEventScoresWithSubperiods() {
    Event commentaryEvent =
        Utils.fromFile(
            gson, "ssEvents/commentary.json", com.egalacoral.spark.siteserver.model.Event.class);
    EventScores eventScores = FootballCommentaryMapper.toEventScores(commentaryEvent);

    assertNotNull(eventScores);
    assertEquals(2, eventScores.getTeams().size());
    assertEquals("FIRSTHALF", eventScores.getPeriod());
    assertTrue(
        eventScores.getTeams().stream().allMatch(t -> t.getScore() == 0 || t.getScore() == 2));
    assertTrue(eventScores.getTeams().stream().allMatch(t -> Objects.nonNull(t.getName())));
  }

  @Test
  public void testConvertToEventScoresWithFacts() {
    Event commentaryEvent =
        Utils.fromFile(
            gson,
            "ssEvents/commentary_facts.json",
            com.egalacoral.spark.siteserver.model.Event.class);
    EventScores eventScores = FootballCommentaryMapper.toEventScores(commentaryEvent);

    assertNotNull(eventScores);
    assertEquals(2, eventScores.getTeams().size());
    assertNull(eventScores.getPeriod());
    assertTrue(
        eventScores.getTeams().stream().allMatch(t -> t.getScore() == 0 || t.getScore() == 2));
    assertTrue(eventScores.getTeams().stream().allMatch(t -> Objects.nonNull(t.getName())));
  }

  @Test
  public void testConvertToEventScoresWithPenalties() {
    Event commentaryEvent =
        Utils.fromFile(
            gson, "ssEvents/commentary.json", com.egalacoral.spark.siteserver.model.Event.class);
    EventScores eventScores = FootballCommentaryMapper.toEventScores(commentaryEvent);

    assertNotNull(eventScores);
    assertEquals(2, eventScores.getTeams().size());
    assertEquals("FIRSTHALF", eventScores.getPeriod());
    assertTrue(
        eventScores.getTeams().stream().allMatch(t -> t.getScore() == 0 || t.getScore() == 2));
    assertTrue(
        eventScores.getTeams().stream()
            .allMatch(t -> t.getPenalties() == 0 || t.getPenalties() == 2));
    assertTrue(eventScores.getTeams().stream().allMatch(t -> Objects.nonNull(t.getName())));
  }
}
