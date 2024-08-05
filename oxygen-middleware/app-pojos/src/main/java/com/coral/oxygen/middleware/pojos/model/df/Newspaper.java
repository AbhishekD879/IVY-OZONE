package com.coral.oxygen.middleware.pojos.model.df;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;
import lombok.Data;

@Data
public class Newspaper implements Serializable {
  private static final long serialVersionUID = 6782990190801312909L;

  private String selection;
  private String rpTip;
  private String name;
  private String flag;
  private Integer rpSelectionUid;
  private String tipster;
  private Map<String, Object> additionalProperties = new HashMap<>();

  public void setAdditionalProperty(String name, Object value) {
    this.additionalProperties.put(name, value);
  }
}
