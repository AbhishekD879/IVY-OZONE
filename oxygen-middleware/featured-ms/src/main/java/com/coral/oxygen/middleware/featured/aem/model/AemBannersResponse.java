package com.coral.oxygen.middleware.featured.aem.model;

import java.util.List;
import lombok.Data;

@Data
public class AemBannersResponse {

  private String statusCode;
  private String errorMsg;
  private String executionTime;
  private List<OfferObject> offers;
  private Object pinned;
}
