package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.Feature;
import java.util.List;

public interface FeatureExtendedRepository {
  List<Feature> findFeatures(String brand);
}
