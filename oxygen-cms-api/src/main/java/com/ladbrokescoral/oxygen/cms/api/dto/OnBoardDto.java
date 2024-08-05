package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.ladbrokescoral.oxygen.cms.api.controller.dto.onboarding.CrcOnBoardingDto;
import lombok.Data;

@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
public class OnBoardDto {

  private CrcOnBoardingDto crcOnBoardingDto;
}
