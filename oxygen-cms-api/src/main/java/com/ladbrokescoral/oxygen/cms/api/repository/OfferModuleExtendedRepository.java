package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.OfferModule;
import java.util.List;

public interface OfferModuleExtendedRepository {
  List<OfferModule> findAllByBrandAndDeviceType(String brand, String deviceType);
}
