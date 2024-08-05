package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.CouponSegment;
import com.ladbrokescoral.oxygen.cms.api.service.CouponSegmentService;
import java.util.List;
import javax.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CouponSegments extends AbstractSortableController<CouponSegment> {

  public CouponSegments(CouponSegmentService couponSegmentService) {
    super(couponSegmentService);
  }

  @Override
  @GetMapping("/coupon-segment")
  public List<CouponSegment> readAll() {
    return super.readAll();
  }

  @Override
  @GetMapping("coupon-segment/brand/{brand}")
  public List<CouponSegment> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @Override
  @PostMapping("coupon-segment/ordering")
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  @Override
  @PostMapping("/coupon-segment")
  public ResponseEntity create(@Valid @RequestBody CouponSegment entity) {
    return super.create(entity);
  }

  @Override
  @GetMapping("/coupon-segment/{id}")
  public CouponSegment read(@PathVariable("id") String id) {
    return super.read(id);
  }

  @Override
  @PutMapping("/coupon-segment/{id}")
  public CouponSegment update(
      @PathVariable("id") String id, @Valid @RequestBody CouponSegment updateEntity) {
    return super.update(id, updateEntity);
  }

  @Override
  @DeleteMapping("/coupon-segment/{id}")
  public ResponseEntity delete(@PathVariable("id") String id) {
    return super.delete(id);
  }
}
