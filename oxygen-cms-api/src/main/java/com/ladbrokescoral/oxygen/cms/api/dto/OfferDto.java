package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonIgnore;
import java.util.List;
import lombok.Data;

@Data
public class OfferDto {
  private String targetUri;
  private String displayFrom;
  private String displayTo;
  private Boolean useDirectImageUrl;
  private String directImageUrl;
  private List<Integer> vipLevels;
  private List<String> showToCustomer;
  private String image;
  @JsonIgnore private String module;
}
