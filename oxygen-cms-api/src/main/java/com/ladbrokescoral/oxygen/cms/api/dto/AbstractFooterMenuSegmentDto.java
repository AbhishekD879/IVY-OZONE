package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.SvgFilename;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.annotation.Id;

@Data
@EqualsAndHashCode(callSuper = false)
public class AbstractFooterMenuSegmentDto extends AbstractSegmentDto {
  @Id private String id;
  private Double sortOrder;
  private String brand;
  private String targetUri;
  private Integer heightMedium;
  private Integer heightSmall;
  private String imageTitle;
  private String imageTitleBrand;
  private String spriteClass;
  private String svg;
  private SvgFilename svgFilename;
  private String uriMedium;
  private String uriSmall;
  private Integer widthMedium;
  private Integer widthSmall;
}
