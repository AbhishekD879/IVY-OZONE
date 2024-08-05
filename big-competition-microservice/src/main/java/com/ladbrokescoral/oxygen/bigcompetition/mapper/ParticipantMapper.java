package com.ladbrokescoral.oxygen.bigcompetition.mapper;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import org.apache.commons.text.similarity.LevenshteinDistance;
import org.springframework.stereotype.Component;

@Component
public class ParticipantMapper {
  public String findBestParticipantName(Set<String> teamNameSet, String statsCenterTeamName) {
    List<String> teamNames = new ArrayList<>(teamNameSet);
    LevenshteinDistance levenshteinDistance = LevenshteinDistance.getDefaultInstance();
    int min = 1000;
    String bestTeamName = "";
    for (int i = 0; i < teamNames.size(); i++) {
      int distance = levenshteinDistance.apply(teamNames.get(i), statsCenterTeamName);
      if (distance < min) {
        min = distance;
        bestTeamName = teamNames.get(i);
      }
    }
    return bestTeamName;
  }
}
