package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.BrandedImage;
import java.util.List;
import javax.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class MyBetDto {
  private String id;
  @NotBlank private String brand;
  private String type;
  private String noBetText;
  private String addDescText;
  private String defaultImgLink;
  private List<BrandedImage> brandedImageList;
}
