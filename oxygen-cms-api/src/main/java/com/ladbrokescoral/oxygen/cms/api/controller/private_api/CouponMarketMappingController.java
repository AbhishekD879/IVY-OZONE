package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.CouponMarketMappingEntity;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.CouponMarketMappingService;
import java.util.List;
import java.util.Optional;
import javax.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/** @author PBalarangakumar 08-02-2024 */
@RestController
@SuppressWarnings("java:S4684")
public class CouponMarketMappingController
    extends AbstractSortableController<CouponMarketMappingEntity> {

  private final CouponMarketMappingService service;

  public CouponMarketMappingController(final CouponMarketMappingService service) {
    super(service);

    this.service = service;
  }

  @Override
  @PostMapping("/coupon-market-mapping")
  public ResponseEntity<CouponMarketMappingEntity> create(
      @Valid @RequestBody CouponMarketMappingEntity coupon) {

    validateCouponId(coupon.getCouponId());
    return super.create(coupon);
  }

  @Override
  @PutMapping("/coupon-market-mapping/{id}")
  public CouponMarketMappingEntity update(
      @PathVariable("id") String id, @Valid @RequestBody CouponMarketMappingEntity coupon) {

    final CouponMarketMappingEntity dbEntity =
        service
            .findOne(id)
            .orElseThrow(
                () ->
                    new NotFoundException(
                        ("coupon market mapping record not found in db, the mongo id is: " + id)));

    if (!dbEntity.getCouponId().equals(coupon.getCouponId())) {
      validateCouponId(coupon.getCouponId());
    }
    return super.update(id, coupon);
  }

  @Override
  @GetMapping("/coupon-market-mapping/{id}")
  public CouponMarketMappingEntity read(@PathVariable("id") String id) {
    return super.read(id);
  }

  @Override
  @GetMapping("coupon-market-mapping/brand/{brand}")
  public List<CouponMarketMappingEntity> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @Override
  @DeleteMapping("/coupon-market-mapping/{id}")
  public ResponseEntity<CouponMarketMappingEntity> delete(@PathVariable("id") String id) {
    return super.delete(id);
  }

  private void validateCouponId(final String couponId) {

    final Optional<CouponMarketMappingEntity> dbEntity = service.findByCouponId(couponId);
    if (dbEntity.isPresent()) {
      throw new IllegalArgumentException(
          "The coupon already exists in DB. the couponId is: " + dbEntity.get().getCouponId());
    }
  }
}
