package com.ladbrokescoral.oxygen.bigcompetition.mapper;

import static com.ladbrokescoral.oxygen.bigcompetition.util.Utils.buildAbbreviation;

import com.ladbrokescoral.oxygen.betradar.client.entity.Entry;
import com.ladbrokescoral.oxygen.betradar.client.entity.PlayerResult;
import com.ladbrokescoral.oxygen.betradar.client.entity.ResultsTable;
import com.ladbrokescoral.oxygen.bigcompetition.dto.statsCenter.GroupModuleBrGroupDetailDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.statsCenter.TeamDto;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionParticipant;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.util.Assert;
import org.springframework.util.StringUtils;

@Component
public class GroupModuleBrGroupDetailMapper {

  private static final String POINTS_TOTAL = "pointsTotal";
  private static final String MATCHES_TOTAL = "matchesTotal";
  private static final String WIN_TOTAL = "winTotal";
  private static final String DRAW_TOTAL = "drawTotal";
  private static final String LOSS_TOTAL = "lossTotal";
  private static final String GOAL_DIFF_TOTAL = "goalDiffTotal";
  private static final Pattern GROUP_PATTERN = Pattern.compile("group\\s\\w");

  private ParticipantMapper participantMapper;

  @Autowired
  public GroupModuleBrGroupDetailMapper(ParticipantMapper participantMapper) {
    this.participantMapper = participantMapper;
  }

  public List<GroupModuleBrGroupDetailDto> toDto(
      List<ResultsTable> resultsTables, List<CompetitionParticipant> competitionParticipants) {
    Map<String, CompetitionParticipant> participantMap =
        competitionParticipants.stream()
            .collect(Collectors.toMap(CompetitionParticipant::getObName, p -> p));
    return resultsTables.stream()
        .map(
            resultsTable ->
                new GroupModuleBrGroupDetailDto()
                    .setCompetitionId(resultsTable.getCompetitionId())
                    .setSeasonId(resultsTable.getSeasonId())
                    .setTableId(resultsTable.getTableId())
                    .setTableName(resultsTable.getTableName())
                    .setTeams(buildTeamDtos(resultsTable, participantMap)))
        .sorted(createGroupNameComparator())
        .collect(Collectors.toList());
  }

  private Comparator<GroupModuleBrGroupDetailDto> createGroupNameComparator() {
    return (el1, el2) -> {
      String firstGroupName = el1.getTableName().replace("_", " ").replace("-", " ").toLowerCase();
      String secondGroupName = el2.getTableName().replace("_", " ").replace("-", " ").toLowerCase();
      Matcher firstGroupMatcher = GROUP_PATTERN.matcher(firstGroupName);
      Matcher secondGroupMatcher = GROUP_PATTERN.matcher(secondGroupName);
      String firstTeamSymbol = findAndValidate(el1, firstGroupMatcher);
      String secondTeamSymbol = findAndValidate(el2, secondGroupMatcher);
      return firstTeamSymbol.compareTo(secondTeamSymbol);
    };
  }

  private String findAndValidate(GroupModuleBrGroupDetailDto el1, Matcher matcher) {
    if (!matcher.find()) {
      throw new IllegalArgumentException(String.format("Error. Bad group name - %s", el1));
    }
    String groupName = matcher.group();
    return groupName.substring(groupName.length() - 1, groupName.length());
  }

  private List<TeamDto> buildTeamDtos(
      ResultsTable resultsTable, Map<String, CompetitionParticipant> participantMap) {
    return resultsTable.getRows().stream()
        .map(t -> buildTeamDto(participantMap, t))
        .collect(Collectors.toList());
  }

  private TeamDto buildTeamDto(
      Map<String, CompetitionParticipant> participantMap, PlayerResult playerResult) {
    String statsCenterTeamName = playerResult.getName();
    Map<String, String> statistic =
        playerResult.getValues().stream().collect(Collectors.toMap(Entry::getKey, Entry::getValue));
    String bestTeamName =
        participantMapper.findBestParticipantName(participantMap.keySet(), statsCenterTeamName);
    CompetitionParticipant competitionParticipant = participantMap.get(bestTeamName);
    Assert.isTrue(
        null != competitionParticipant,
        String.format("Can't find competition participant data '%s' at CMS", statsCenterTeamName));
    return new TeamDto()
        .setStatsCenterName(statsCenterTeamName)
        .setName(
            (StringUtils.isEmpty(competitionParticipant.getFullName()))
                ? competitionParticipant.getObName()
                : competitionParticipant.getFullName())
        .setObName(competitionParticipant.getObName())
        .setAbbreviation(
            StringUtils.isEmpty(competitionParticipant.getAbbreviation())
                ? buildAbbreviation(competitionParticipant.getObName())
                : competitionParticipant.getAbbreviation())
        .setSvgId(competitionParticipant.getSvgId())
        .setTotalPoints(Integer.parseInt(statistic.get(POINTS_TOTAL)))
        .setMatchesTotal(Integer.parseInt(statistic.get(MATCHES_TOTAL)))
        .setWinTotal(Integer.parseInt(statistic.get(WIN_TOTAL)))
        .setDrawTotal(Integer.parseInt(statistic.get(DRAW_TOTAL)))
        .setLossTotal(Integer.parseInt(statistic.get(LOSS_TOTAL)))
        .setGoalDiffTotal(Integer.parseInt(statistic.get(GOAL_DIFF_TOTAL)));
  }
}
