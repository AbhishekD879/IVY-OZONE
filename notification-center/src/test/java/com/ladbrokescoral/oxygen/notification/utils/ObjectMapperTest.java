package com.ladbrokescoral.oxygen.notification.utils;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.ladbrokescoral.oxyegn.test.utils.Utils;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.Event;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.EventScores;
import java.util.Arrays;
import java.util.List;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.util.StringUtils;

@RunWith(MockitoJUnitRunner.class)
public class ObjectMapperTest {

  private Gson gson;

  private com.egalacoral.spark.siteserver.model.Event internationalTote;
  private com.egalacoral.spark.siteserver.model.Event greyhounds;
  private com.egalacoral.spark.siteserver.model.Event horseRacing;
  private com.egalacoral.spark.siteserver.model.Event football;

  @Before
  public void setUp() {
    gson = new GsonBuilder().create();

    internationalTote =
        Utils.fromFile(
            gson,
            "ssEvents/international_tote.json",
            com.egalacoral.spark.siteserver.model.Event.class);
    horseRacing =
        Utils.fromFile(
            gson, "ssEvents/horse_racing.json", com.egalacoral.spark.siteserver.model.Event.class);
    greyhounds =
        Utils.fromFile(
            gson, "ssEvents/greyhounds.json", com.egalacoral.spark.siteserver.model.Event.class);
    football =
        Utils.fromFile(
            gson, "ssEvents/football.json", com.egalacoral.spark.siteserver.model.Event.class);
  }

  @Test
  public void testGreyhoundsSportUri() {
    Event event = ObjectMapper.toEvent(greyhounds);
    Assert.assertEquals(
        "greyhound-racing/greyhounds-live/henlow/09-02-henlow/", event.getSportUri());
  }

  @Test
  public void testHorseRacingSportUri() {
    Event event = ObjectMapper.toEvent(horseRacing);
    Assert.assertEquals(
        "horse-racing/horse-racing-tote-pools/exeter--de-/3m-6-1-2f-hcap-chase/",
        event.getSportUri());
  }

  @Test
  public void testInternationalToteSportUri() {
    Event event = ObjectMapper.toEvent(internationalTote);
    Assert.assertEquals("tote/event/", event.getSportUri());
  }

  @Test
  public void testEventMappingNPE() {
    Event event = ObjectMapper.toEvent(internationalTote);
    Assert.assertFalse(event.isLive());
    Assert.assertFalse(event.isEventStarted());
    Assert.assertFalse(event.isEventResulted());
    Assert.assertFalse(event.isLive());
  }

  @Test
  public void testEventNull() {
    Assert.assertNull(ObjectMapper.toEvent(null));
  }

  @Test
  public void toEventWithScores() {
    // given:
    EventScores.Team homeTeam = createTeam("Team 1", 1, 2);
    EventScores.Team awayTeam = createTeam("Team 2", 3, 4);
    EventScores scores = new EventScores("PENALTIES", Arrays.asList(homeTeam, awayTeam));
    // when:
    Event event = ObjectMapper.toEventWithScores(football, scores);

    // then:
    Assert.assertNotNull(event);
    Assert.assertEquals(Long.parseLong(football.getId()), event.getEventId().longValue());
    Assert.assertEquals(football.getName(), event.getName());

    Assert.assertEquals(homeTeam.getName(), event.getHomeTeamName());
    Assert.assertEquals(homeTeam.getScore(), event.getHomeTeamScore());
    Assert.assertEquals(homeTeam.getPenalties(), event.getHomeTeamPenalties());

    Assert.assertEquals(awayTeam.getName(), event.getAwayTeamName());
    Assert.assertEquals(awayTeam.getScore(), event.getAwayTeamScore());
    Assert.assertEquals(awayTeam.getPenalties(), event.getAwayTeamPenalties());
  }

  @Mock List<String> codes;

  @Test
  public void testIsHomeTeam() {
    codes = Arrays.asList("TEAM_1", "HOME");
    EventScores.Team homeTeam = createTeam("Team 1", 1, 2);
    homeTeam.setRoleCode("HOME");
    EventScores.Team awayTeam = createTeam("Team 2", 3, 4);
    awayTeam.setRoleCode("AWAY");
    EventScores.Team homeTeam1 = createTeam("Team 3", 1, 2);
    homeTeam1.setRoleCode("");
    Assert.assertTrue(codes.contains(homeTeam.getRoleCode()));
    Assert.assertTrue(StringUtils.hasText(homeTeam.getRoleCode()));
    Assert.assertFalse(codes.contains(homeTeam1.getRoleCode()));
    Assert.assertFalse(StringUtils.hasText(homeTeam1.getRoleCode()));
    Assert.assertFalse(codes.contains(awayTeam.getRoleCode()));
    Assert.assertTrue(StringUtils.hasText(awayTeam.getRoleCode()));
    Assert.assertEquals(true, ObjectMapper.isHomeTeam(homeTeam));
    Assert.assertEquals(false, ObjectMapper.isHomeTeam(awayTeam));
    Assert.assertEquals(false, ObjectMapper.isHomeTeam(homeTeam1));
    ObjectMapper.isHomeTeam(homeTeam);
    ObjectMapper.isHomeTeam(awayTeam);
  }

  private EventScores.Team createTeam(String teamName, int score, int penalties) {
    EventScores.Team team = new EventScores.Team(teamName);
    team.setScore(score);
    team.setPenalties(penalties);
    return team;
  }
}
