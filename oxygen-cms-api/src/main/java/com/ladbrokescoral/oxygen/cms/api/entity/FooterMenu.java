package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.ImageAbstractMenu;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.SvgAbstractMenu;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.AbstractMenuSegmentEntity;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "footermenus")
@Data
@EqualsAndHashCode(callSuper = true)
public class FooterMenu extends AbstractMenuSegmentEntity
    implements ImageAbstractMenu, SvgAbstractMenu, HasBrand {
  private boolean desktop;
  private boolean disabled;
  private Filename filename;
  private Integer heightMedium;
  private Integer heightSmall;
  private String imageTitle;

  @Field("imageTitle_brand")
  private String imageTitleBrand;

  private boolean inApp;
  private String lang;
  private boolean mobile;
  private String path;
  private String showItemFor;
  private String spriteClass;
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
  private boolean tablet;
  private String targetUri;
  private String uriMedium;
  private String uriSmall;
  private Integer widthMedium;
  private Integer widthSmall;
  private String collectionType;
  private String itemType;
  private Integer heightLarge;
  private Integer widthLarge;
  private String uriLarge;
  private boolean authRequired;
  private Integer systemID;
  private String widgetName;
}
