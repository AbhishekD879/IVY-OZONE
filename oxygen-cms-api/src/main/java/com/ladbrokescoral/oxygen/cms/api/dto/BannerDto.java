package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;
import lombok.Data;
import org.springframework.data.annotation.Id;

@Data
public class BannerDto {

  @Id private String id;
  private String filename;

  @JsonProperty("desktop_filename")
  private String desktopFilename;

  private String uriMedium;
  private String uriSmall;

  @JsonProperty("desktop_uriMedium")
  private String desktopUriMedium;

  @JsonProperty("desktop_uriSmall")
  private String desktopUriSmall;

  private List<String> showToCustomer;
  private List<Integer> vipLevels;
  private String signpostingEventLevel;
  private String signpostingMarketLevel;
  private String alt;
  private String imageTitle;
  private String targetUri;
  private String validityPeriodStart;
  private String validityPeriodEnd;
  private Integer widthMedium;
  private Integer heightMedium;
  private Integer widthSmall;
  private Integer heightSmall;
  private Boolean disabled;
  private Boolean inApp;
  private Boolean enabled;

  @JsonProperty("desktop_heightMedium")
  private String desktopHeightMedium;

  @JsonProperty("desktop_widthMedium")
  private String desktopWidthMedium;

  @JsonProperty("desktop_heightSmall")
  private String desktopHeightSmall;

  @JsonProperty("desktop_widthSmall")
  private String desktopWidthSmall;

  @JsonProperty("desktop_enabled")
  private String desktopEnabled;

  @JsonProperty("desktop_targetUri")
  private String desktopTargetUri;

  @JsonProperty("desktop_inApp")
  private Boolean desktopInApp;
}
