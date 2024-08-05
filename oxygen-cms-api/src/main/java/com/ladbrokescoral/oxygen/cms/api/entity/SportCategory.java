package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.IconAbstractMenu;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.ImageAbstractMenu;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.SvgAbstractMenu;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.AbstractSegmentEntity;
import java.util.List;
import java.util.Map;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "sportcategories")
@Data
@EqualsAndHashCode(callSuper = true)
public class SportCategory extends AbstractSegmentEntity
    implements SvgAbstractMenu, ImageAbstractMenu, IconAbstractMenu {

  private String alt;
  @NotBlank private String brand;
  private Integer categoryId;
  private boolean disabled;
  private SportTier tier;
  private Filename filename;
  private Integer heightMedium;
  private Integer heightMediumIcon;
  private Integer heightSmall;
  private Integer heightSmallIcon;
  private Filename icon;
  private String imageTitle;
  private boolean inApp;
  private Boolean isTopSport;
  private String key;
  private String lang;
  private String link;
  private String path;

  private boolean outrightSport;
  private boolean multiTemplateSport;
  private OddsCardHeaderType oddsCardHeaderType;
  private String typeIds;
  private String dispSortNames;
  private String primaryMarkets;
  private String topMarkets;
  private List<Map<String, String>> aggrigatedMarkets;

  private boolean showInMenu;
  private String spriteClass;
  private String ssCategoryCode;
  /**
   * @deprecated use SvgImages api to upload images and use update the menu endpoint to set the
   *     svgId delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated private String svg;
  /**
   * @deprecated use SvgImages api to upload images and use update the menu endpoint to set the
   *     svgId delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated private SvgFilename svgFilename;

  private String svgId;
  private String targetUri;
  private String uriMedium;
  private String uriMediumIcon;
  private String uriSmall;
  private String uriSmallIcon;
  private Integer widthMedium;
  private Integer widthMediumIcon;
  private Integer widthSmall;
  private Integer widthSmallIcon;
  private String collectionType;
  private boolean showInAZ;
  private boolean showInHome;
  private boolean showInPlay;
  private boolean showScoreboard;
  private Integer heightLarge;
  private Integer heightLargeIcon;
  private String uriLarge;
  private String uriLargeIcon;
  private Integer widthLarge;
  private Integer widthLargeIcon;
  private String scoreBoardUri;
  private boolean inplayEnabled;
  private boolean hasEvents;
  private boolean showFreeRideBanner;
  // OZONE-3426 added this field for non runner horse message for extrasignplace posting
  private String messageLabel;

  private boolean isReactionsEnabled;

  private InplayStatsConfig inplayStatsConfig;

  @JsonProperty("isReactionsEnabled")
  public boolean isReactionsEnabled() {
    return isReactionsEnabled;
  }
}
