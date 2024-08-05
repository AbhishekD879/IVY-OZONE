package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.ImageAbstractMenu;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.SvgAbstractMenu;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "rightmenus")
@Data
@EqualsAndHashCode(callSuper = true)
public class RightMenu extends AbstractMenuEntity implements SvgAbstractMenu, ImageAbstractMenu {

  private String collectionType;
  private Boolean disabled;
  private Filename filename;
  private Integer heightMedium;
  private Integer heightSmall;
  private String iconAligment;
  private Boolean inApp;
  private String lang;
  private String menuItemView;
  private String path;
  private String section;
  private String showItemFor;
  private String spriteClass;
  private String targetUri;
  private String type;
  private String uriMedium;
  private String uriSmall;
  private Integer widthMedium;
  private Integer widthSmall;
  private boolean showOnlyOnIOS;
  private boolean showOnlyOnAndroid;
  private Integer heightLarge;
  private Integer widthLarge;
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

  @Field(value = "QA")
  private String qa;

  private String uriLarge;
  private Boolean authRequired;
  private Integer systemID;
  private String startUrl;
  private String subHeader;
}
