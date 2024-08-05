package com.coral.oxygen.middleware.common.service.commentary;

import com.coral.oxygen.middleware.common.service.DefaultCommentaryFieldsType;
import com.coral.oxygen.middleware.common.service.DefaultCommentaryValuesType;
import com.coral.oxygen.middleware.pojos.model.output.Comment;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.scoreboards.parser.api.YesNo;
import com.ladbrokescoral.scoreboards.parser.model.BipComment;
import com.ladbrokescoral.scoreboards.parser.model.EventCategory;
import java.util.HashMap;
import java.util.Map;
import lombok.Builder;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import org.apache.commons.lang3.math.NumberUtils;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class CommentaryService {
  private final ObjectMapper objectMapper;

  /**
   * Converts comment parsed from event's names to comment used by middleware (based on SiteServer
   * comment structure)
   *
   * @param eventId - id of event
   * @param bipComment - {@link BipComment} - comment parsed from event's name
   * @return {@link Comment} - comment object with SiteServer structure that's used by UI
   */
  public Comment populateCommentaryFromEventName(Long eventId, BipComment bipComment) {
    Comment resultComment = new Comment();
    com.ladbrokescoral.scoreboards.parser.model.Comment homeComment =
        bipComment.getPlayerAComment();
    com.ladbrokescoral.scoreboards.parser.model.Comment awayComment =
        bipComment.getPlayerBComment();

    TeamCommentDto.TeamCommentDtoBuilder homeBuilder = commentBuilder(eventId, homeComment);
    TeamCommentDto.TeamCommentDtoBuilder awayBuilder = commentBuilder(eventId, awayComment);

    EventCategory eventCategory = bipComment.getEventCategory();
    if (eventCategory.equals(EventCategory.FOOTBALL)
        || eventCategory.equals(EventCategory.BASKETBALL)) {

      TeamCommentDto home = withDefaultHomeTeamBuilder(homeBuilder).build();
      TeamCommentDto away = withDefaultAwayTeamBuilder(awayBuilder).build();

      setTeams(resultComment, home, away);
    } else if (eventCategory.equals(EventCategory.TENNIS)) {

      TeamCommentDto player1 =
          buildPlayerComment(
              homeComment, withDefaultPlayerABuilder(homeBuilder), DefaultCommentaryValuesType.T);
      TeamCommentDto player2 =
          buildPlayerComment(
              awayComment, withDefaultPlayerBBuilder(awayBuilder), DefaultCommentaryValuesType.T);

      setPlayers(resultComment, player1, player2);
      setRunningSetIndex(resultComment, homeComment.getScore(), awayComment.getScore());
      setRunningGameScores(
          resultComment, homeComment.getCurrentPoints(), awayComment.getCurrentPoints());
      setSetsScore(resultComment, homeComment.getPeriodScore(), awayComment.getPeriodScore());
    } else if (eventCategory.equals(EventCategory.BADMINTON)) {

      TeamCommentDto player1 =
          buildPlayerComment(
              homeComment, withDefaultPlayerABuilder(homeBuilder), DefaultCommentaryValuesType.P);
      TeamCommentDto player2 =
          buildPlayerComment(
              awayComment, withDefaultPlayerBBuilder(awayBuilder), DefaultCommentaryValuesType.P);

      setPlayers(resultComment, player1, player2);
      setRunningSetIndex(resultComment, homeComment.getScore(), awayComment.getScore());
      setSetsScore(resultComment, homeComment.getCurrentPoints(), awayComment.getCurrentPoints());
    }
    return resultComment;
  }

  private void setRunningSetIndex(Comment comment, String homeScore, String awayScore) {
    if (NumberUtils.isDigits(homeScore) && NumberUtils.isDigits(awayScore)) {
      int indexShift = 1;
      comment.setRunningSetIndex(
          NumberUtils.toInt(homeScore) + NumberUtils.toInt(awayScore) + indexShift);
    }
  }

  private TeamCommentDto.TeamCommentDtoBuilder commentBuilder(
      Long eventId, com.ladbrokescoral.scoreboards.parser.model.Comment comment) {
    return TeamCommentDto.builder()
        .eventId(eventId)
        .name(comment.getName())
        .score(comment.getScore());
  }

  private TeamCommentDto buildPlayerComment(
      com.ladbrokescoral.scoreboards.parser.model.Comment homeComment,
      TeamCommentDto.TeamCommentDtoBuilder teamCommentDtoBuilder,
      DefaultCommentaryValuesType t) {
    return teamCommentDtoBuilder.active(homeComment.getServing()).type(t.getValue()).build();
  }

  private void setTeams(Comment comment, TeamCommentDto homeTeam, TeamCommentDto awayTeam) {
    Map<String, Object> teams = new HashMap<>();
    teams.put(DefaultCommentaryFieldsType.home.toString(), toMap(homeTeam));
    teams.put(DefaultCommentaryFieldsType.away.toString(), toMap(awayTeam));
    comment.setTeams(teams);
  }

  private void setPlayers(Comment comment, TeamCommentDto player1, TeamCommentDto player2) {
    Map<String, Object> teams = new HashMap<>();
    teams.put(DefaultCommentaryFieldsType.player_1.toString(), toMap(player1));
    teams.put(DefaultCommentaryFieldsType.player_2.toString(), toMap(player2));
    comment.setTeams(teams);
  }

  private void setRunningGameScores(
      Comment comment, String homeRunningScore, String awayRunningScore) {
    Map<String, Object> runningGameScores = new HashMap<>();
    runningGameScores.put(DefaultCommentaryValuesType.FIELD_1.getValue(), homeRunningScore);
    runningGameScores.put(DefaultCommentaryValuesType.FIELD_2.getValue(), awayRunningScore);
    comment.setRunningGameScores(runningGameScores);
  }

  private void setSetsScore(Comment comment, String homeSetsScore, String awaySetsScore) {
    Map<String, Object> setsScores = new HashMap<>();
    Map<String, Object> forPlayersScores = new HashMap<>();
    forPlayersScores.put(DefaultCommentaryValuesType.FIELD_1.getValue(), homeSetsScore);
    forPlayersScores.put(DefaultCommentaryValuesType.FIELD_2.getValue(), awaySetsScore);
    setsScores.put("" + comment.getRunningSetIndex(), forPlayersScores);
    comment.setSetsScores(setsScores);
  }

  private TeamCommentDto.TeamCommentDtoBuilder withDefaultHomeTeamBuilder(
      TeamCommentDto.TeamCommentDtoBuilder commentBuilder) {
    return commentBuilder
        .id(DefaultCommentaryValuesType.FIRST_PLAYER_ID.getValue())
        .role(DefaultCommentaryValuesType.HOME_TEAM_ROLE.getValue())
        .roleCode(DefaultCommentaryValuesType.HOME_TEAM_ROLE_CODE.getValue())
        .type(DefaultCommentaryValuesType.T.getValue())
        .code(DefaultCommentaryValuesType.SCORE.getValue());
  }

  private TeamCommentDto.TeamCommentDtoBuilder withDefaultAwayTeamBuilder(
      TeamCommentDto.TeamCommentDtoBuilder commentBuilder) {
    return commentBuilder
        .id(DefaultCommentaryValuesType.SECOND_PLAYER_ID.getValue())
        .role(DefaultCommentaryValuesType.AWAY_TEAM_ROLE.getValue())
        .roleCode(DefaultCommentaryValuesType.AWAY_TEAM_ROLE_CODE.getValue())
        .type(DefaultCommentaryValuesType.T.getValue())
        .code(DefaultCommentaryValuesType.SCORE.getValue());
  }

  private TeamCommentDto.TeamCommentDtoBuilder withDefaultPlayerABuilder(
      TeamCommentDto.TeamCommentDtoBuilder commentBuilder) {
    return commentBuilder
        .id(DefaultCommentaryValuesType.FIRST_PLAYER_ID.getValue())
        .role(DefaultCommentaryValuesType.GENERIC_HOME_TEAM_ROLE.getValue())
        .roleCode(DefaultCommentaryValuesType.PLAYER_1.getValue())
        .code(DefaultCommentaryValuesType.SCORE.getValue());
  }

  private TeamCommentDto.TeamCommentDtoBuilder withDefaultPlayerBBuilder(
      TeamCommentDto.TeamCommentDtoBuilder commentBuilder) {
    return commentBuilder
        .id(DefaultCommentaryValuesType.SECOND_PLAYER_ID.getValue())
        .role(DefaultCommentaryValuesType.GENERIC_AWAY_TEAM_ROLE.getValue())
        .roleCode(DefaultCommentaryValuesType.PLAYER_2.getValue())
        .code(DefaultCommentaryValuesType.SCORE.getValue());
  }

  @Data
  @Builder
  private static class TeamCommentDto {

    private Long eventId;
    private String id;
    private String name;
    private String role;
    private String roleCode;
    private YesNo active;
    private String type;
    private String score;
    private String code;
  }

  private Map<String, Object> toMap(TeamCommentDto commentDto) {
    return objectMapper.convertValue(commentDto, new TypeReference<Map<String, Object>>() {});
  }
}
