package com.coral.oxygen.middleware.common.service.commentary

import com.coral.oxygen.middleware.pojos.model.output.Comment
import com.fasterxml.jackson.annotation.JsonInclude
import com.fasterxml.jackson.databind.ObjectMapper
import com.ladbrokescoral.scoreboards.parser.api.YesNo
import com.ladbrokescoral.scoreboards.parser.model.BipComment
import com.ladbrokescoral.scoreboards.parser.model.EventCategory
import spock.lang.Specification

class CommentaryServiceTest extends Specification {
  private CommentaryService commentaryService

  void setup() {
    ObjectMapper mapper = new ObjectMapper()
    mapper.setSerializationInclusion(JsonInclude.Include.NON_NULL)
    commentaryService = new CommentaryService(mapper)
  }

  def "Football and basketball comment"() {
    given:
    def bipComment =  BipComment.of(
        "Team A v Team B",
        comment("Team A", "5",YesNo.Y),
        comment("Team B", "3",YesNo.N),
        EventCategory.FOOTBALL)

    when:
    def middlewareComment = commentaryService.populateCommentaryFromEventName(123, bipComment)

    then:
    middlewareComment.teams == [
      "home": [
        "eventId" : 123,
        "name"    : "Team A",
        "score"   : "5",
        "id"      : "1",
        "role"    : "Home Team",
        "roleCode": "HOME",
        "type"    : "T",
        "code"    : "SCORE"
      ],
      "away": [
        "eventId" : 123,
        "name"    : "Team B",
        "score"   : "3",
        "id"      : "2",
        "role"    : "Away Team",
        "roleCode": "AWAY",
        "type"    : "T",
        "code"    : "SCORE"
      ]
    ]
  }

  def "Tennis comment"() {
    given:
    def bipComment =  BipComment.of(
        "Player A v Player B",
        comment("Player A*", "7", "30", "4",YesNo.Y),
        comment("Player B", "0", "15", "3",YesNo.N),
        EventCategory.TENNIS)

    when:
    def middlewareComment = commentaryService.populateCommentaryFromEventName(123, bipComment)

    then:
    middlewareComment.teams == [
      "player_1": [
        "eventId" : 123,
        "name"    : "Player A",
        "score"   : "7",
        "id"      : "1",
        "role"    : "Generic first player listed",
        "roleCode": "PLAYER_1",
        "type"    : "T",
        "code"    : "SCORE",
        "active": "Y"
      ],
      "player_2": [
        "eventId" : 123,
        "name"    : "Player B",
        "score"   : "0",
        "id"      : "2",
        "role"    : "Generic second player listed",
        "roleCode": "PLAYER_2",
        "type"    : "T",
        "code"    : "SCORE",
        "active": "N"
      ]
    ]

    middlewareComment.runningGameScores == ["1": "30", "2": "15"]

    middlewareComment.setsScores == [
      "8": ["1": "4", "2": "3"]
    ]
    middlewareComment.runningSetIndex == 8
  }

  def "Tennis comment runningSetIndex null on invalid scores"() {
    given:
    def invalidScores = ["", "-1", "abc"]
    def validScore = "0"

    def bipComments = []
    for (def invalidScore : invalidScores) {
      def bipComment = BipComment.of(
          "Player A v Player B",
          comment("Player A", validScore, "1", "1",YesNo.Y),
          comment("Player B", invalidScore, "1", "1",YesNo.N),
          EventCategory.TENNIS)
      bipComments.add(bipComment)
    }
    def commentsNumber = bipComments.size()

    when:
    def middlewareComments = []
    for (BipComment bipComment  : bipComments) {
      middlewareComments.add(commentaryService.populateCommentaryFromEventName(1L, bipComment))
    }

    then:
    for (int i = 0; i < commentsNumber; i++) {
      Comment comment = (Comment) middlewareComments[i]
      comment.runningSetIndex == null
      comment.setsScores == [
        "1": ["1": "1", "2": "1"]
      ]
    }
  }

  def "Badminton comment"() {
    given:
    def bipComment =  BipComment.of(
        "Player A v Player B",
        comment("Player A", "7", "15",YesNo.N),
        comment("Player B*", "0", "10",YesNo.Y),
        EventCategory.BADMINTON)

    when:
    def middlewareComment = commentaryService.populateCommentaryFromEventName(123, bipComment)

    then:
    middlewareComment.teams == [
      "player_1": [
        "eventId" : 123,
        "name"    : "Player A",
        "score"   : "7",
        "id"      : "1",
        "role"    : "Generic first player listed",
        "roleCode": "PLAYER_1",
        "type"    : "P",
        "code"    : "SCORE",
        "active": "N"
      ],
      "player_2": [
        "eventId" : 123,
        "name"    : "Player B",
        "score"   : "0",
        "id"      : "2",
        "role"    : "Generic second player listed",
        "roleCode": "PLAYER_2",
        "type"    : "P",
        "code"    : "SCORE",
        "active": "Y"
      ]
    ]

    middlewareComment.setsScores == [
      "8": ["1": "15", "2": "10"]
    ]
    middlewareComment.runningSetIndex == 8
  }

  private com.ladbrokescoral.scoreboards.parser.model.Comment comment(String name,
      String score,
      String currentPoints = null,
      String periodScore = null,
      YesNo serving) {
    return new com.ladbrokescoral.scoreboards.parser.model.Comment(
        name,
        score,
        currentPoints,
        periodScore,
        serving)
  }
}
