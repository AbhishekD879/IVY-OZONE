package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.CouponSegment;
import com.ladbrokescoral.oxygen.cms.api.repository.CouponSegmentRepository;
import org.springframework.stereotype.Service;

@Service
public class CouponSegmentService extends SortableService<CouponSegment> {
  public CouponSegmentService(CouponSegmentRepository repository) {
    super(repository);
  }

  @Override
  public CouponSegment save(CouponSegment couponSegment) {
    if (couponSegment.getDayOfWeek() != null) {
      if (couponSegment.getFrom() != null || couponSegment.getTo() != null) {
        throw new IllegalArgumentException(
            "Properties 'to', 'from' must be nulls when 'dayOfWeek' is specified");
      }
    } else if (couponSegment.getFrom() == null || couponSegment.getTo() == null) {
      throw new IllegalArgumentException("Properties 'to', 'from' must not be nulls");
    }

    return super.save(couponSegment);
  }
}
