package com.coral.siteserver.model;

import java.io.Serializable;
import lombok.Data;

@Data
public class HealthCheck implements Serializable {
  private static final long serialVersionUID = 547045945039340648L;
  private String status;
}
