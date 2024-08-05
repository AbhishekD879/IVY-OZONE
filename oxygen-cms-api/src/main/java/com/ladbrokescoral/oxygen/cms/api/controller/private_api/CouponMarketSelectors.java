package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.CouponMarketSelector;
import com.ladbrokescoral.oxygen.cms.api.service.CouponMarketSelectorService;
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
public class CouponMarketSelectors extends AbstractSortableController<CouponMarketSelector> {
  CouponMarketSelectors(CouponMarketSelectorService sortableService) {
    super(sortableService);
  }

  @Override
  @GetMapping("/coupon-market-selector")
  public List<CouponMarketSelector> readAll() {
    return super.readAll();
  }

  @Override
  @GetMapping("coupon-market-selector/brand/{brand}")
  public List<CouponMarketSelector> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @Override
  @PostMapping("coupon-market-selector/ordering")
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  @Override
  @PostMapping("/coupon-market-selector")
  public ResponseEntity create(@Valid @RequestBody CouponMarketSelector entity) {
    return super.create(entity);
  }

  @Override
  @GetMapping("/coupon-market-selector/{id}")
  public CouponMarketSelector read(@PathVariable("id") String id) {
    return super.read(id);
  }

  @Override
  @PutMapping("/coupon-market-selector/{id}")
  public CouponMarketSelector update(
      @PathVariable("id") String id, @Valid @RequestBody CouponMarketSelector updateEntity) {
    return super.update(id, updateEntity);
  }

  @Override
  @DeleteMapping("/coupon-market-selector/{id}")
  public ResponseEntity delete(@PathVariable("id") String id) {
    return super.delete(id);
  }
}
