package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.FreeRidePublicSplashPageDto;
import com.ladbrokescoral.oxygen.cms.api.entity.freeride.FreeRideSplashPage;
import com.ladbrokescoral.oxygen.cms.api.service.FreeRideSplashPageService;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.stream.Collectors;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;

@Service
public class FreeRideSplashPagePublicService {

  private final FreeRideSplashPageService freeRideSplashPageService;

  private ModelMapper modelMapper;

  public FreeRideSplashPagePublicService(
      FreeRideSplashPageService freeRideSplashPageService, ModelMapper modelMapper) {
    this.freeRideSplashPageService = freeRideSplashPageService;
    this.modelMapper = modelMapper;
  }

  public List<FreeRidePublicSplashPageDto> getFreeRideSplashPageByBrand(String brand) {
    List<FreeRideSplashPage> freeRideSplashPageList =
        freeRideSplashPageService.getFreeRideSplashPageByBrand(brand);
    List<FreeRidePublicSplashPageDto> freeRideSplashpage =
        freeRideSplashPageList.stream()
            .map(x -> modelMapper.map(x, FreeRidePublicSplashPageDto.class))
            .collect(Collectors.toList());
    Optional<FreeRideSplashPage> freeRideSplashpageObj =
        freeRideSplashPageList.stream().findFirst();
    freeRideSplashpage.forEach(
        (FreeRidePublicSplashPageDto splashPage) -> {
          splashPage.setBannerImageUrl(
              Objects.nonNull(freeRideSplashpageObj.get().getBannerImage())
                  ? freeRideSplashpageObj.get().getBannerImage().relativePath()
                  : null);
          splashPage.setFreeRideLogoUrl(
              Objects.nonNull(freeRideSplashpageObj.get().getFreeRideLogo())
                  ? freeRideSplashpageObj.get().getFreeRideLogo().relativePath()
                  : null);
          splashPage.setSplashImageUrl(
              Objects.nonNull(freeRideSplashpageObj.get().getSplashImage())
                  ? freeRideSplashpageObj.get().getSplashImage().relativePath()
                  : null);
        });
    return freeRideSplashpage;
  }
}
