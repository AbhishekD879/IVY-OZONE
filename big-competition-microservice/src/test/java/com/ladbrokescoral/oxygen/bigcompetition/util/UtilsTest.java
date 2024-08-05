package com.ladbrokescoral.oxygen.bigcompetition.util;

import static com.ladbrokescoral.oxygen.bigcompetition.util.Utils.buildAbbreviation;
import static com.ladbrokescoral.oxygen.bigcompetition.util.Utils.buildName;

import com.ladbrokescoral.oxygen.cms.client.model.CompetitionParticipant;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.test.context.junit4.SpringRunner;

@RunWith(SpringRunner.class)
public class UtilsTest {

  @Test
  public void testBuildNameWithFullName() {
    String fullName = "cp1";
    CompetitionParticipant competitionParticipant = new CompetitionParticipant();
    competitionParticipant.setFullName(fullName);

    String result = buildName(competitionParticipant);

    Assert.assertEquals(result, fullName);
  }

  @Test
  public void testBuildNameWithOutFullName() {
    String obName = "obcp1";
    CompetitionParticipant competitionParticipant = new CompetitionParticipant();
    competitionParticipant.setObName(obName);

    String result = buildName(competitionParticipant);

    Assert.assertEquals(result, obName);
  }

  @Test
  public void testBuildAbbreviationByCompetitionParticipant() {
    String abbreviation = "VS";
    CompetitionParticipant competitionParticipant = new CompetitionParticipant();
    competitionParticipant.setAbbreviation(abbreviation);

    String result = buildAbbreviation(competitionParticipant);

    Assert.assertEquals(result, abbreviation);
  }

  @Test
  public void testBuildAbbreviationByTeamName() {
    String teamName = "t1";

    String result = buildAbbreviation(teamName);

    Assert.assertEquals(result, teamName);
  }
}
