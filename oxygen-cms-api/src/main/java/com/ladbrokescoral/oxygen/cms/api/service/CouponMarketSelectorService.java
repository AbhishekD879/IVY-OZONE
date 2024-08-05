package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.CouponMarketSelector;
import com.ladbrokescoral.oxygen.cms.api.repository.CouponMarketSelectorRepository;
import org.springframework.stereotype.Service;

@Service
public class CouponMarketSelectorService extends SortableService<CouponMarketSelector> {
  private final CouponMarketSelectorRepository couponMarketSelectorRepository;

  public CouponMarketSelectorService(
      CouponMarketSelectorRepository couponMarketSelectorRepository) {
    super(couponMarketSelectorRepository);
    this.couponMarketSelectorRepository = couponMarketSelectorRepository;
  }

  @Override
  public <S extends CouponMarketSelector> S save(S entity) {
    if (couponMarketSelectorRepository.existsByTemplateMarketNameAndIdNotAndBrandIs(
        entity.getTemplateMarketName(), entity.getId(), entity.getBrand())) {
      throw new IllegalArgumentException(
          "CouponMarketSelector.templateMarketName must be unique within the same brand");
    }
    return super.save(entity);
  }
}
