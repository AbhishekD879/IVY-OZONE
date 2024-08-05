package com.ladbrokescoral.oxygen.cms.api.controller.private_api.onboarding;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.onboarding.CouponStatsWidgetDto;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.AbstractCrudController;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.CouponStatsWidget;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.onboarding.CouponStatsWidgetService;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import org.modelmapper.ModelMapper;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@Validated
public class CouponStatsWidgets extends AbstractCrudController<CouponStatsWidget> {
  private final CouponStatsWidgetService service;
  private final ModelMapper mapper;

  protected CouponStatsWidgets(
      CouponStatsWidgetService couponStatsWidgetService, ModelMapper mapper) {
    super(couponStatsWidgetService);
    this.mapper = mapper;
    this.service = couponStatsWidgetService;
  }

  @PostMapping("/coupon-stats-widget")
  public ResponseEntity<CouponStatsWidget> create(
      @RequestBody CouponStatsWidgetDto couponStatsWidgetDto) {
    CouponStatsWidget couponStatsWidget = mapper.map(couponStatsWidgetDto, CouponStatsWidget.class);
    return super.create(couponStatsWidget);
  }

  @PutMapping("/coupon-stats-widget/{id}")
  public CouponStatsWidget update(
      @PathVariable String id, @RequestBody CouponStatsWidgetDto couponStatsWidgetDto) {
    CouponStatsWidget couponStatsWidget = mapper.map(couponStatsWidgetDto, CouponStatsWidget.class);
    return super.update(id, couponStatsWidget);
  }

  @GetMapping("/coupon-stats-widget/brand/{brand}")
  public CouponStatsWidget findAllByBrand(@PathVariable String brand) {
    return service.readByBrand(brand).orElseThrow(NotFoundException::new);
  }

  @GetMapping("/coupon-stats-widget/{id}")
  public CouponStatsWidget findById(@PathVariable String id) {
    return super.read(id);
  }

  @DeleteMapping("/coupon-stats-widget/{id}")
  public void deleteById(@PathVariable String id) {
    super.delete(id);
  }

  @PostMapping("/coupon-stats-widget/{id}/image")
  public ResponseEntity<CouponStatsWidget> addCSWImg(
      @PathVariable("id") String id,
      @ValidFileType({"png", "jpg", "jpeg", "svg"}) @RequestParam("file") MultipartFile file) {
    CouponStatsWidget couponStatsWidget = service.findOne(id).orElseThrow(NotFoundException::new);
    return service
        .attachImage(couponStatsWidget, file)
        .map(
            (CouponStatsWidget csw) -> {
              CouponStatsWidget saved = service.save(csw);
              return new ResponseEntity<>(saved, HttpStatus.OK);
            })
        .orElseGet(failedToUpdateImage());
  }

  @DeleteMapping("/coupon-stats-widget/{id}/image")
  public ResponseEntity<CouponStatsWidget> removeImage(@PathVariable("id") String id) {
    CouponStatsWidget couponStatsWidget = service.findOne(id).orElseThrow(NotFoundException::new);

    return service
        .removeImage(couponStatsWidget)
        .map(
            (CouponStatsWidget csw) -> {
              CouponStatsWidget saved = service.save(csw);
              return new ResponseEntity<>(saved, HttpStatus.OK);
            })
        .orElseGet(failedToUpdateImage());
  }
}
