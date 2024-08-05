package com.ladbrokescoral.oxygen.bigcompetition.mapper;

import com.ladbrokescoral.oxygen.betradar.client.entity.SeasonMatches;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.results.Team;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionParticipant;
import java.util.HashMap;
import java.util.Map;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.util.ReflectionTestUtils;

@RunWith(SpringRunner.class)
public class ResultsModuleMapperTest {
  ParticipantMapper participantMapper = new ParticipantMapper();
  ResultsModuleMapper resultsModuleMapper = new ResultsModuleMapper(participantMapper);

  @Test
  public void testGropingFormatParseException() {
    String kickOffTime = "2020 09 21";

    Object result =
        ReflectionTestUtils.invokeMethod(resultsModuleMapper, "gropingFormat", kickOffTime);

    Assert.assertEquals(kickOffTime, result);
  }

  @Test
  public void testObNames() {

    String teamName = "Liverpool";
    SeasonMatches seasonMatches = new SeasonMatches();
    String teamIndex = "1";
    CompetitionParticipant competitionParticipant = new CompetitionParticipant();
    competitionParticipant.setId("11");
    competitionParticipant.setObName("Liverpool");
    competitionParticipant.setFullName("Liverpool");
    Map<String, CompetitionParticipant> map = new HashMap<>();
    map.put(teamName, competitionParticipant);
    Team team =
        ReflectionTestUtils.invokeMethod(
            resultsModuleMapper, "fillTeamInfo", seasonMatches, teamName, teamIndex, map);
    Assert.assertNotNull(team);
  }
}
