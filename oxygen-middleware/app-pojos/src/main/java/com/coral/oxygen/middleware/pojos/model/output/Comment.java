package com.coral.oxygen.middleware.pojos.model.output;

import java.io.Serializable;
import java.util.List;
import java.util.Map;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class Comment implements Serializable {
  private Map<String, Object> teams;
  private transient List<Object> facts;
  private Map<String, Object> latestPeriod;
  private Map<String, Object> setsScores;
  private Integer runningSetIndex;
  private Map<String, Object> runningGameScores;
}
