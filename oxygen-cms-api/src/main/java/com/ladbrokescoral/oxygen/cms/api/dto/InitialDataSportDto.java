package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.Data;

@Data
public class InitialDataSportDto {
  private String id;
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
  private SportOddsCardHeaderTypeDto oddsCardHeaderType;
  private Boolean disabled;
  private Boolean showInPlay;
  private Boolean isOutrightSport;
  private Boolean isMultiTemplateSport;
  private SportTabsDto tabs;
  private String defaultTab;
  private String inApp;
  // OZONE-3426 added this field for non runner horse message for extrasignplace posting
  private String messageLabel;
}
