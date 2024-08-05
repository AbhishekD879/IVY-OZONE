package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import lombok.Data;
import org.springframework.web.multipart.MultipartFile;

@Data
public class OnboardingImageDto {

  private String id;

  @Size(max = 50, message = "ImageLabel should be max of 50 chars")
  private String imageLabel;

  @Size(max = 50, message = "nextCTAButtonLabel should be max of 50 chars")
  private String nextCTAButtonLabel;

  @ValidFileType({"png", "jpg", "jpeg"})
  private MultipartFile onboardImg;

  private Filename onboardImageDetails;
  @NotNull private String imageType;
}
