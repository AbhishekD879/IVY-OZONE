package com.ladbrokescoral.oxygen.cms.api.service.onboarding;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.CouponAndMarketSwitcherCFDto;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.CouponAndMarketSwitcher;
import com.ladbrokescoral.oxygen.cms.api.exception.CouponAndMarketSwitcherCreateException;
import com.ladbrokescoral.oxygen.cms.api.repository.CouponAndMarketSwitcherRepository;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import java.util.Optional;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Service
public class CouponAndMarketSwitcherWidgetService
    extends OnboardingService<CouponAndMarketSwitcher> {
  private ModelMapper modelMapper;

  public CouponAndMarketSwitcherWidgetService(
      CouponAndMarketSwitcherRepository couponAndMarketSwitcherRepository,
      ModelMapper modelMapper,
      ImageService imageService,
      @Value("${images.CouponAndMarketSwitcher.medium}") String mediumPath,
      @Value("${images.CouponAndMarketSwitcher.size}") String mediumImageSize) {
    super(couponAndMarketSwitcherRepository, imageService, mediumPath, mediumImageSize);
    this.modelMapper = modelMapper;
  }

  @Override
  public CouponAndMarketSwitcher save(CouponAndMarketSwitcher couponAndMarketSwitcher) {
    if (isEntityValidToCreate(couponAndMarketSwitcher)) return super.save(couponAndMarketSwitcher);
    throw new CouponAndMarketSwitcherCreateException();
  }

  public Optional<CouponAndMarketSwitcherCFDto> convertToCFDto(CouponAndMarketSwitcher entity) {
    return Optional.ofNullable(modelMapper.map(entity, CouponAndMarketSwitcherCFDto.class));
  }

  @Override
  public Optional<CouponAndMarketSwitcher> attachImage(
      CouponAndMarketSwitcher onboarding, MultipartFile image) {
    onboarding.setFileName(image.getOriginalFilename());
    return getUploadImageFunctionExcludeHW().apply(onboarding, image);
  }
}
