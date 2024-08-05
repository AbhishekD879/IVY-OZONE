package com.ladbrokescoral.oxygen.cms.api.controller.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.SvgFilename;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Field;

@Data
public class BankingMenuDto {
  @Id private String id;
  @NotBlank @com.ladbrokescoral.oxygen.cms.api.service.validators.Brand protected String brand;
  @NotBlank private String linkTitle;

  @Field("linkTitle_brand")
  private String linkTitleBrand;

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
  private Boolean showOnlyOnIOS;
  private Boolean showOnlyOnAndroid;
  private Integer heightLarge;
  private Integer widthLarge;
  /**
   * @deprecated image should be extracted via svg sprite by svgId delete after release-103.0.0 goes
   *     live (check with ui)
   */
  @Deprecated private String svg;
  /**
   * @deprecated image should be extracted via svg sprite by svgId delete after release-103.0.0 goes
   *     live (check with ui)
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
  private Double sortOrder;
}
