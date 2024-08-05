package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.Offer;
import java.util.List;
import org.bson.types.ObjectId;

public interface OfferExtendedRepository {
  List<Offer> findOffers(String brand, String deviceType, List<ObjectId> moduleIds);
}
