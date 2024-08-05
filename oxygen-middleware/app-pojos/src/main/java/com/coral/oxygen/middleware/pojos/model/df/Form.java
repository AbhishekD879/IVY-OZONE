package com.coral.oxygen.middleware.pojos.model.df;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;
import lombok.Data;

@Data
public class Form implements Serializable {
  private static final long serialVersionUID = -1642750249440778093L;

  private String rpr;
  private String weight;
  private Integer raceid;
  private Integer weightLbs;
  private String officialRating;
  private String course;
  private String jockey;
  private String date;
  private String topspeed;
  private String outcome;
  private String condition;
  private String position;
  private String allowance;
  private Map<String, Object> additionalProperties = new HashMap<>();
}
