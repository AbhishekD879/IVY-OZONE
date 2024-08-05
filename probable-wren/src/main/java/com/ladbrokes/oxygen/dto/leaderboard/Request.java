package com.ladbrokes.oxygen.dto.leaderboard;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Data;

@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
public class Request {
  private String contestId;
  private String userId;
  private String betId;
  private String eventId;
  private String type;
  private String key;
  private String contentType;
  private String sessionId;
  private String token;
}
