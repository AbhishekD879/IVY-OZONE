package com.coral.oxygen.middleware.pojos.model.cms.featured;

import java.util.List;
import lombok.Data;

@Data
public class PopularAccaWidgetData {

  private String id;
  private String title;
  private String subTitle;
  private String svgId;

  private Integer sortOrder;

  private String numberOfTimeBackedLabel;
  private Integer numberOfTimeBackedThreshold;

  private String accaIdsType;
  private List<String> listOfIds;
  private List<String> marketTemplateIds;
  private Integer accaRangeMin;
  private Integer accaRangeMax;
}
