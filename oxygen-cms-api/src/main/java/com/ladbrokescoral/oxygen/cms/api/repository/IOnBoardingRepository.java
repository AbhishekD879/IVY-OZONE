package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.OnBoarding;

public interface IOnBoardingRepository<T extends OnBoarding> extends CustomMongoRepository<T> {

  public T findByBrandAndIsEnable(String brand, boolean b);

  boolean existsByBrand(String brand);
}
