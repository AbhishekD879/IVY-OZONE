package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.BetReceiptBanner;
import com.ladbrokescoral.oxygen.cms.api.repository.BetReceiptBannerExtendedRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.BetReceiptBannerRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class BetReceiptBannerService extends BetReceiptService<BetReceiptBanner> {

  @Autowired
  public BetReceiptBannerService(
      BetReceiptBannerRepository repository,
      @Qualifier("betReceipt") BetReceiptBannerExtendedRepository extendedRepository,
      ImageService imageService,
      @Value("${images.betReceiptBanners.original}") String originalPath,
      @Value("${images.betReceiptBanners.medium.path}") String mediumPath,
      @Value("${images.betReceiptBanners.medium.size}") String mediumSize) {
    super(repository, extendedRepository, imageService, originalPath, mediumPath, mediumSize);
  }
}
