package com.ladbrokescoral.oxygen.cms.api.service.onboarding;

import com.ladbrokescoral.oxygen.cms.api.dto.CouponStatsWidgetCFDto;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.CouponStatsWidget;
import com.ladbrokescoral.oxygen.cms.api.exception.CouponStatsWidgetCreateException;
import com.ladbrokescoral.oxygen.cms.api.repository.CouponStatsWidgetRepository;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import java.util.Optional;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.multipart.MultipartFile;

@Service
@Validated
public class CouponStatsWidgetService extends OnboardingService<CouponStatsWidget> {

  private ModelMapper modelMapper;

  public CouponStatsWidgetService(
      CouponStatsWidgetRepository repository,
      ImageService imageService,
      @Value("${images.couponStatsWidget.medium}") String mediumPath,
      @Value("${images.couponStatsWidget.size}") String mediumImageSize,
      ModelMapper modelMapper) {
    super(repository, imageService, mediumPath, mediumImageSize);
    this.modelMapper = modelMapper;
  }

  @Override
  public CouponStatsWidget save(CouponStatsWidget couponStatsWidget) {
    if (isEntityValidToCreate(couponStatsWidget)) return super.save(couponStatsWidget);
    throw new CouponStatsWidgetCreateException();
  }

  public Optional<CouponStatsWidgetCFDto> convertToCFDto(CouponStatsWidget entity) {
    return Optional.ofNullable(modelMapper.map(entity, CouponStatsWidgetCFDto.class));
  }

  @Override
  public Optional<CouponStatsWidget> attachImage(
      CouponStatsWidget onboarding, MultipartFile image) {
    onboarding.setFileName(image.getOriginalFilename());
    return getUploadImageFunctionExcludeHW().apply(onboarding, image);
  }
}
