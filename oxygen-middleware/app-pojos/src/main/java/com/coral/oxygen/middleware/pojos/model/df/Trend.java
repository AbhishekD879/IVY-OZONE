package com.coral.oxygen.middleware.pojos.model.df;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;
import lombok.Data;

@Data
public class Trend implements Serializable {
  private static final long serialVersionUID = -755093333366747580L;

  private String year;
  private String weightLbs;
  private String trainer;
  private String jockey;
  private String topspeed;
  private String rpr;
  private String draw;
  private String age;
  private String sp;
  private String winner;
  private Map<String, Object> additionalProperties = new HashMap<>();
}
