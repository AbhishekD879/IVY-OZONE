package com.ladbrokescoral.oxygen.cms.api.controller.dto.onboarding;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.web.multipart.MultipartFile;

@Data
@EqualsAndHashCode(callSuper = true)
@JsonInclude(JsonInclude.Include.NON_NULL)
public class MyStableOnboardingDto extends OnboardingDto {
  private String buttonText;

  private Boolean isActive;

  @ValidFileType({"png", "jpg", "jpeg", "svg"})
  private MultipartFile onboardImg;

  private Filename onboardImageDetails;
}
