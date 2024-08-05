package com.ladbrokescoral.oxygen.cms.api.controller.dto;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.SvgFilename;
import com.ladbrokescoral.oxygen.cms.api.entity.TargetWindow;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import javax.validation.constraints.NotNull;
import lombok.Data;
import org.hibernate.validator.constraints.URL;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Data
public class GameMenuDto {
  @Brand private String brand;
  private String title;
  @URL private String url;
  @NotNull private TargetWindow target = TargetWindow.CURRENT;
  private String externalImageId;
  private String svg;
  private SvgFilename svgFilename;
  private String svgId;
  private Double sortOrder;
  private Boolean isNative;
  private Filename pngFilename;
}
