package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.segment.Segment;
import java.util.List;
import java.util.Optional;

public interface SegmentRepository extends CustomMongoRepository<Segment> {
  Optional<Object> findByBrandAndSegmentName(String brand, String segmentName);

  public void deleteByIdIn(List<String> ids);

  void deleteBysegmentNameInAndBrand(List<String> ids, String brand);

  List<Segment> findAllByIdIn(List<String> ids);
}
