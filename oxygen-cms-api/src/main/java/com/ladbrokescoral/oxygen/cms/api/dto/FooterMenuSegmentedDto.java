package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.SvgFilename;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.annotation.Id;

@Data
@EqualsAndHashCode(callSuper = true)
public class FooterMenuSegmentedDto extends AbstractSegmentDto {
  @Id private String id;
  private boolean desktop;
  private boolean disabled;
  private Filename filename;
  private Integer heightMedium;
  private Integer heightSmall;
  private String imageTitle;
  private String imageTitleBrand;
  private boolean inApp;
  private String lang;
  private boolean mobile;
  private String path;
  private String showItemFor;
  private String spriteClass;
  private String svg;
  private SvgFilename svgFilename;
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
  private String brand;
  private String linkTitle;
  private String linkTitleBrand;
  private Double sortOrder;
}
