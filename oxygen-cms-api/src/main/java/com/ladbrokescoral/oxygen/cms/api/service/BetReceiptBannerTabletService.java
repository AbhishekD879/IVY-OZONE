package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.BetReceiptBannerTablet;
import com.ladbrokescoral.oxygen.cms.api.repository.BetReceiptBannerExtendedRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.BetReceiptBannerTabletRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class BetReceiptBannerTabletService extends BetReceiptService<BetReceiptBannerTablet> {

  @Autowired
  public BetReceiptBannerTabletService(
      BetReceiptBannerTabletRepository repository,
      @Qualifier("betReceiptTablet") BetReceiptBannerExtendedRepository extendedRepository,
      ImageService imageService,
      @Value("${images.betReceiptBannersTablet.original}") String originalPath,
      @Value("${images.betReceiptBannersTablet.medium.path}") String mediumPath,
      @Value("${images.betReceiptBannersTablet.medium.size}") String mediumSize) {
    super(repository, extendedRepository, imageService, originalPath, mediumPath, mediumSize);
  }
}
