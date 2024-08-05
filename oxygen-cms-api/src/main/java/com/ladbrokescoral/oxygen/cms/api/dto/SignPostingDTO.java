package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.Price;
import lombok.Data;

@Data
public class SignPostingDTO {
  private String brand;
  private String freeBetType;
  private String fromOffer;
  private String betConditions;
  private String sport;
  private String event;
  private String market;
  private Price price;
  private String signPost;
  private Boolean disabled;
  private Boolean isActive;
  private String title;
}
