package com.ladbrokes.oxygen.dto.leaderboard;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Data;

@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
public class Response {
  private String key;
  private String data;
  private String type;
}
