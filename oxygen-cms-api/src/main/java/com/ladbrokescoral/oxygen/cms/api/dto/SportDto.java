package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class SportDto extends BaseUIDto {
  private String svg;
  private String svgId;
  private String alt;
  private String imageTitle;
  private String categoryId;
  private List<String> typeIds;
  private String ssCategoryCode;
  private String targetUri;
  private List<String> dispSortName;
  private String primaryMarkets;
  private List<String> viewByFilters;
  private SportOddsCardHeaderTypeDto oddsCardHeaderType;
  private Boolean disabled;
  private Boolean showInPlay;
  private Boolean isOutrightSport;
  private Boolean isMultiTemplateSport;
  private SportTabsDto tabs;
  private String defaultTab;
  private String inApp;
}
