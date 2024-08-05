package com.coral.oxygen.middleware.pojos.model.df;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;
import lombok.Data;

@Data
public class Keystat implements Serializable {
  private static final long serialVersionUID = 6593392544550057203L;

  private String runner;
  private String comment;
  private String ksweight;
  private Map<String, Object> additionalProperties = new HashMap<>();
}
