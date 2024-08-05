package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.TargetWindow;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = false)
public class GameMenuDto {
  private String title;
  private String url;
  private TargetWindow target;
  private Double sortOrder;
  private String externalImageId;
  private String svg;
  private String svgId;
  private Boolean isNative;
  private Filename pngFilename;
}
