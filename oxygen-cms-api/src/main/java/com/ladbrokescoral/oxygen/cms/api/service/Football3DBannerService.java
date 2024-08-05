package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Football3DBanner;
import com.ladbrokescoral.oxygen.cms.api.repository.Football3DBannerRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class Football3DBannerService extends BetReceiptService<Football3DBanner> {

  private final Football3DBannerRepository bannerRepository;

  @Autowired
  public Football3DBannerService(
      Football3DBannerRepository bannerRepository,
      ImageService imageService,
      @Value("${images.3dbanners.original}") String originalPath,
      @Value("${images.3dbanners.medium.path}") String mediumPath,
      @Value("${images.3dbanners.medium.size}") String mediumSize) {
    super(bannerRepository, null, imageService, originalPath, mediumPath, mediumSize);

    this.bannerRepository = bannerRepository;
  }

  public List<Football3DBanner> findAllByBrandAndDisabled(String brand) {
    return bannerRepository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand, Boolean.FALSE);
  }
}
