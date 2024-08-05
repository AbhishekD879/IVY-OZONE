package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.onboarding.CrcOnBoardingDto;
import com.ladbrokescoral.oxygen.cms.api.dto.OnBoardDto;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.CrcOnBoarding;
import com.ladbrokescoral.oxygen.cms.api.service.onboarding.CrcOnBoardingService;
import java.util.List;
import java.util.Optional;
import lombok.RequiredArgsConstructor;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class OnBoardPublicService {

  private final CrcOnBoardingService crcOnBoardingService;
  private final ModelMapper modelMapper;

  public OnBoardDto getOnBoard(String brand) {

    OnBoardDto onBoardDto = new OnBoardDto();
    onBoardDto.setCrcOnBoardingDto(getCrcOnBoardingDto(brand));
    return onBoardDto;
  }

  public CrcOnBoardingDto getCrcOnBoardingDto(String brand) {
    Optional<List<CrcOnBoarding>> crcOnBoardings =
        Optional.ofNullable(crcOnBoardingService.findByBrand(brand));
    return crcOnBoardings
        .filter(onboardings -> !onboardings.isEmpty())
        .map(entity -> modelMapper.map(entity.get(0), CrcOnBoardingDto.class))
        .orElse(new CrcOnBoardingDto());
  }
}
