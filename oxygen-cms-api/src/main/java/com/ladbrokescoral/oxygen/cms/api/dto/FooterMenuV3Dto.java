package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.Data;
import org.springframework.data.annotation.Id;

@Data
public class FooterMenuV3Dto {
  @Id private String id;
  private String target;
  private String title;
  private String image;
  private String imageLarge;
  private Boolean inApp;
  private String showItemFor;
  private String widget;
  private String svg;
  private String svgId;
  private Boolean authRequired;
  private Integer systemID;
  private List<String> device;
}
