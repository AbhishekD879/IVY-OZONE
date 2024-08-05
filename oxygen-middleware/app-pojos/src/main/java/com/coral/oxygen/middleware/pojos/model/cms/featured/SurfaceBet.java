package com.coral.oxygen.middleware.pojos.model.cms.featured;

import com.coral.oxygen.middleware.pojos.model.output.OutputPrice;
import java.math.BigInteger;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class SurfaceBet extends SportPageModuleDataItem {
  private String id;
  private String title;
  private String displayFrom;
  private String displayTo;

  private String svgId;
  private String svgBgImgPath;
  private String content;
  private String contentHeader;

  private Boolean disabled;
  private Boolean edpOn;
  private Boolean highlightsTabOn;
  private BigInteger selectionId;
  private OutputPrice price;
  private Integer displayOrder;
  private SurfaceBetRelation reference;
  private Boolean displayOnDesktop;
  private String svgBgId;
}
