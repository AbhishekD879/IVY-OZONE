package com.coral.oxygen.edp.model.output;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonInclude;
import java.util.List;
import java.util.Map;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@JsonInclude(JsonInclude.Include.NON_NULL)
@EqualsAndHashCode
public class Comment {

  private Map<String, Object> teams;

  @JsonIgnore private List<Object> facts;

  private Map<String, Object> latestPeriod;

  private Map<String, Object> setsScores;

  private Integer runningSetIndex;

  private Map<String, Object> runningGameScores;
}
