package com.ladbrokescoral.oxygen.bigcompetition.mapper;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;
import org.junit.Before;
import org.junit.Test;
import org.springframework.util.Assert;

public class ParticipantMapperTest {
  ParticipantMapper participantMapper = new ParticipantMapper();
  Set<String> participantSet;
  String statsCenterTeamName = "Saudi";

  @Before
  public void setUp() throws Exception {
    participantSet =
        new HashSet<>(Arrays.asList("saudi", "Iran", "Saudi", "Russia", "Saudi Aravia"));
  }

  @Test
  public void testParticipantMapper() {
    String bestParticipantName =
        participantMapper.findBestParticipantName(participantSet, statsCenterTeamName);
    Assert.isTrue(bestParticipantName.equals("Saudi"), "Should find right participant");
  }
}
