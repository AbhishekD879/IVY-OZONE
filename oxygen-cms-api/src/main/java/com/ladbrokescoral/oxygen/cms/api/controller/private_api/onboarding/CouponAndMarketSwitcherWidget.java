package com.ladbrokescoral.oxygen.cms.api.controller.private_api.onboarding;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.onboarding.CouponAndMarketSwitcherDto;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.AbstractCrudController;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.CouponAndMarketSwitcher;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.onboarding.CouponAndMarketSwitcherWidgetService;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import org.modelmapper.ModelMapper;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class CouponAndMarketSwitcherWidget extends AbstractCrudController<CouponAndMarketSwitcher> {
  public final CouponAndMarketSwitcherWidgetService couponAndMarketSwitcherWidgetService;
  private final ModelMapper mapper;

  protected CouponAndMarketSwitcherWidget(
      CouponAndMarketSwitcherWidgetService couponAndMarketSwitcherWidgetService,
      ModelMapper mapper) {
    super(couponAndMarketSwitcherWidgetService);
    this.couponAndMarketSwitcherWidgetService = couponAndMarketSwitcherWidgetService;
    this.mapper = mapper;
  }

  @PostMapping("/couponAndMarketSwitcherWidget")
  public ResponseEntity<CouponAndMarketSwitcher> create(
      @RequestBody CouponAndMarketSwitcherDto couponAndMarketSwitcherDto) {
    CouponAndMarketSwitcher couponAndMarketSwitcher =
        mapper.map(couponAndMarketSwitcherDto, CouponAndMarketSwitcher.class);
    return super.create(couponAndMarketSwitcher);
  }

  @PutMapping("/couponAndMarketSwitcherWidget/{id}")
  public CouponAndMarketSwitcher update(
      @PathVariable String id, @RequestBody CouponAndMarketSwitcherDto couponAndMarketSwitcherDto) {
    CouponAndMarketSwitcher couponAndMarketSwitcher =
        mapper.map(couponAndMarketSwitcherDto, CouponAndMarketSwitcher.class);
    return super.update(id, couponAndMarketSwitcher);
  }

  @GetMapping("/couponAndMarketSwitcherWidget/{id}")
  public CouponAndMarketSwitcher findById(@PathVariable String id) {
    return super.read(id);
  }

  @DeleteMapping("/couponAndMarketSwitcherWidget/{id}")
  public void deleteById(@PathVariable String id) {
    super.delete(id);
  }

  @GetMapping("/couponAndMarketSwitcherWidget/brand/{brand}")
  public CouponAndMarketSwitcher findAllByBrand(@PathVariable String brand) {
    return couponAndMarketSwitcherWidgetService
        .readByBrand(brand)
        .orElseThrow(NotFoundException::new);
  }

  @PostMapping("/couponAndMarketSwitcherWidget/{id}/image")
  public ResponseEntity<CouponAndMarketSwitcher> addCouponAndMarketSwitcherImg(
      @PathVariable("id") String id,
      @ValidFileType({"png", "jpg", "jpeg", "svg"}) @RequestParam("file") MultipartFile file) {
    CouponAndMarketSwitcher couponAndMarketSwitcher =
        couponAndMarketSwitcherWidgetService.findOne(id).orElseThrow(NotFoundException::new);
    return couponAndMarketSwitcherWidgetService
        .attachImage(couponAndMarketSwitcher, file)
        .map(
            (CouponAndMarketSwitcher switcher) -> {
              CouponAndMarketSwitcher saved = couponAndMarketSwitcherWidgetService.save(switcher);
              return new ResponseEntity<>(saved, HttpStatus.OK);
            })
        .orElseGet(failedToUpdateImage());
  }

  @DeleteMapping("/couponAndMarketSwitcherWidget/{id}/image")
  public ResponseEntity<CouponAndMarketSwitcher> removeCouponAndMarketSwitcherImage(
      @PathVariable("id") String id) {
    CouponAndMarketSwitcher couponAndMarketSwitcher =
        couponAndMarketSwitcherWidgetService.findOne(id).orElseThrow(NotFoundException::new);

    return couponAndMarketSwitcherWidgetService
        .removeImage(couponAndMarketSwitcher)
        .map(
            (CouponAndMarketSwitcher switcher) -> {
              CouponAndMarketSwitcher saved = couponAndMarketSwitcherWidgetService.save(switcher);
              return new ResponseEntity<>(saved, HttpStatus.OK);
            })
        .orElseGet(failedToUpdateImage());
  }
}
