package com.ladbrokescoral.oxygen.bigcompetition.mapper;

import com.ladbrokescoral.oxygen.betradar.client.entity.Match;
import com.ladbrokescoral.oxygen.betradar.client.entity.Score;
import com.ladbrokescoral.oxygen.bigcompetition.dto.statsCenter.MatchResultDto;
import java.util.List;
import org.apache.commons.lang3.StringUtils;
import org.springframework.stereotype.Component;

@Component
public class MatchDetailsDtoMapper {

  enum MatchResultType {
    FT, // full time
    OT, // extra time
    AP // penalty
  }

  public MatchResultDto toDto(Match match) {
    List<Score> scores = match.getResult().getScores();
    if (scores != null) {
      MatchResultDto matchResultDto = new MatchResultDto();
      scores.forEach(score -> setResultedScore(matchResultDto, score));
      recalculatePenalties(matchResultDto);
      return matchResultDto;
    }
    return null;
  }

  private void recalculatePenalties(MatchResultDto matchResultDto) {
    if (matchResultDto.getPen() != null && matchResultDto.getPen().length == 2) {
      Integer home =
          Integer.valueOf(matchResultDto.getPen()[0]) - Integer.valueOf(matchResultDto.getAet()[0]);
      Integer away =
          Integer.valueOf(matchResultDto.getPen()[1]) - Integer.valueOf(matchResultDto.getAet()[1]);
      matchResultDto.setPen(new String[] {String.valueOf(home), String.valueOf(away)});
    }
  }

  private void setResultedScore(MatchResultDto matchResultDto, Score score) {
    String[] scores = StringUtils.isNotEmpty(score.getValue()) ? score.getValue().split(":") : null;

    if (MatchResultType.FT.name().equals(score.getType())) {
      matchResultDto.setScore(scores);
    } else if (MatchResultType.OT.name().equals(score.getType())) {
      matchResultDto.setAet(scores);
    } else if (MatchResultType.AP.name().equals(score.getType())) {
      matchResultDto.setPen(scores);
    }
  }
}
