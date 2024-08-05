package com.oxygen.publisher.model;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.util.List;
import java.util.Map;
import lombok.Data;

/** Represents the Comment model. */
@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
public class Comment {

  private Map<String, Object> teams;
  private List<Object> facts;
  private Map<String, Object> latestPeriod;
  private Map<String, Object> setsScores;
  private Integer runningSetIndex;
  private Map<String, Object> runningGameScores;
}
