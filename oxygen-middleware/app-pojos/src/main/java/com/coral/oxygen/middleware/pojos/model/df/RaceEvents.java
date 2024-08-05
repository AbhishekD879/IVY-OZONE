package com.coral.oxygen.middleware.pojos.model.df;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;
import lombok.Data;

@Data
public class RaceEvents implements Serializable {

  private static final long serialVersionUID = 8823479002066837623L;

  @JsonProperty("Error")
  private boolean error;

  private Document document;
  private Map<String, String> additionalProperties = new HashMap<>();

  public void setAdditionalProperty(String name, String value) {
    this.additionalProperties.put(name, value);
  }
}
