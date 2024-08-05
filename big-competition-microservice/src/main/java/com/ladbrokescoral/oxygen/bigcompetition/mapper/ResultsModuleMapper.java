package com.ladbrokescoral.oxygen.bigcompetition.mapper;

import com.ladbrokescoral.oxygen.betradar.client.entity.Goals;
import com.ladbrokescoral.oxygen.betradar.client.entity.SeasonMatches;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.results.MatchesDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.results.ResultsModuleDataDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.results.Team;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionParticipant;
import java.time.*;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

@Slf4j
@Component
@RequiredArgsConstructor
public class ResultsModuleMapper {

  private static final String TEAM_A_INDEX = "1";
  private static final String TEAM_B_INDEX = "2";
  private static final int SCORES_COUNT = 2;
  private final ParticipantMapper participantMapper;

  public List<ResultsModuleDataDto> toDto(
      List<SeasonMatches> seasonMatches, List<CompetitionParticipant> participantList) {
    Map<String, CompetitionParticipant> participantMap =
        participantList.stream()
            .collect(Collectors.toMap(CompetitionParticipant::getObName, e -> e));
    return seasonMatches.stream()
        .collect(Collectors.groupingBy(m -> gropingFormat(m.getKickOffTime())))
        .entrySet()
        .stream()
        .map(
            entry ->
                new ResultsModuleDataDto()
                    .setDate(gropingFormat(entry.getKey()))
                    .setMatches(
                        entry.getValue().stream()
                            .map(
                                match ->
                                    new MatchesDto()
                                        .setKickOffTime(match.getKickOffTime())
                                        .setTeamA(getTeamA(match, participantMap))
                                        .setTeamB(getTeamB(match, participantMap)))
                            .sorted(
                                Comparator.comparing(MatchesDto::getKickOffTime)
                                    .reversed()
                                    .thenComparing(match -> match.getTeamA().getName()))
                            .collect(Collectors.toList())))
        .sorted(Comparator.comparing(ResultsModuleDataDto::getDate).reversed())
        .collect(Collectors.toList());
  }

  private String gropingFormat(String kickOffTime) {
    try {
      return DateTimeFormatter.ISO_LOCAL_DATE
          .withZone(ZoneOffset.UTC)
          .format(DateTimeFormatter.ISO_INSTANT.parse(kickOffTime));
    } catch (DateTimeException dateTimeException) {
      return kickOffTime;
    }
  }

  private Team getTeamA(SeasonMatches match, Map<String, CompetitionParticipant> participantMap) {
    return fillTeamInfo(match, match.getTeamA().getName(), TEAM_A_INDEX, participantMap);
  }

  private Team getTeamB(SeasonMatches match, Map<String, CompetitionParticipant> participantMap) {
    return fillTeamInfo(match, match.getTeamB().getName(), TEAM_B_INDEX, participantMap);
  }

  private Team fillTeamInfo(
      SeasonMatches match,
      String name,
      String teamIndex,
      Map<String, CompetitionParticipant> participants) {
    Team team = new Team();
    Set<String> obNames = participants.keySet();
    String bestTeamName = this.participantMapper.findBestParticipantName(obNames, name);
    team.setName(name);
    team.setScore(determineScore(match, teamIndex));
    team.setGoalScorers(getGoalScores(match, teamIndex));
    if (bestTeamName.equalsIgnoreCase(name)) {
      CompetitionParticipant participant = participants.get(bestTeamName);
      team.setSvgId(participant.getSvgId());
    }
    return team;
  }

  /**
   * Transformate field "score":"3:0" to "3" for teamA and "0" for teamB
   *
   * @param match
   * @param teamIndex
   * @return
   */
  private String determineScore(SeasonMatches match, String teamIndex) {
    return Optional.ofNullable(match.getResult())
        .map(res -> res.getFullTime().getValue())
        .filter(value -> !value.isEmpty())
        .map(value -> Arrays.asList(value.split(":")))
        .filter(scores -> scores.size() == SCORES_COUNT)
        .map(scores -> TEAM_A_INDEX.equals(teamIndex) ? scores.get(0) : scores.get(1))
        .orElse("");
  }

  /**
   * Build player goals string in format: Thiago 68', 10', Jesus Navas 37'
   *
   * @param match
   * @param teamIndex
   * @return goal scores string value
   */
  private String getGoalScores(SeasonMatches match, String teamIndex) {
    String joinDelimeter = "', ";
    String spaceDelimeter = " ";
    StringBuilder goalsString = new StringBuilder();
    Map<String, List<Goals>> playerGoals = getPlayerGoals(match, teamIndex);
    playerGoals.entrySet().stream()
        .sorted(
            (e1, e2) -> {
              Integer goal1 = Integer.parseInt(e1.getValue().get(0).getTime());
              Integer goal2 = Integer.parseInt(e2.getValue().get(0).getTime());
              return goal1.compareTo(goal2);
            })
        .forEach(
            entry ->
                goalsString
                    .append(entry.getKey()) //
                    .append(spaceDelimeter) //
                    .append(
                        entry.getValue().stream() //
                            .map(Goals::getTime) //
                            .collect(Collectors.joining(joinDelimeter, "", joinDelimeter))));
    return removeLastCharOptional(goalsString.toString());
  }

  private String removeLastCharOptional(String s) {
    return Optional.ofNullable(s)
        .filter(str -> !str.isEmpty())
        .map(String::trim)
        .map(str -> str.substring(0, str.length() - 1))
        .orElse(s);
  }

  private Map<String, List<Goals>> getPlayerGoals(SeasonMatches match, String index) {
    return match.getGoals() != null && !match.getGoals().isEmpty()
        ? match.getGoals().stream()
            .collect(
                Collectors.groupingBy(
                    Goals::getTeam,
                    Collectors.groupingBy(g -> Optional.ofNullable(g.getPlayerName()).orElse(""))))
            .getOrDefault(index, Collections.emptyMap())
        : Collections.emptyMap();
  }
}
