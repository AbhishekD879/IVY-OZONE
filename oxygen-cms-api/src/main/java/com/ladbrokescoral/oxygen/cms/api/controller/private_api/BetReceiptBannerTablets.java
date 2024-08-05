package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BetReceiptBannerTablet;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.BetReceiptBannerTabletService;
import java.util.List;
import javax.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class BetReceiptBannerTablets extends AbstractImageController<BetReceiptBannerTablet> {

  private final BetReceiptBannerTabletService betReceiptTabletService;

  @Autowired
  public BetReceiptBannerTablets(BetReceiptBannerTabletService crudService) {
    super(crudService);
    betReceiptTabletService = crudService;
  }

  @PostMapping("bet-receipt-banner-tablet")
  @Override
  public ResponseEntity create(@RequestBody @Valid BetReceiptBannerTablet entity) {
    return super.create(entity);
  }

  @GetMapping("bet-receipt-banner-tablet")
  @Override
  public List<BetReceiptBannerTablet> readAll() {
    return super.readAll();
  }

  @GetMapping("bet-receipt-banner-tablet/{id}")
  @Override
  public BetReceiptBannerTablet read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("bet-receipt-banner-tablet/brand/{brand}")
  @Override
  public List<BetReceiptBannerTablet> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PutMapping("bet-receipt-banner-tablet/{id}")
  @Override
  public BetReceiptBannerTablet update(
      @PathVariable String id, @RequestBody @Valid BetReceiptBannerTablet entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("bet-receipt-banner-tablet/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @PostMapping("bet-receipt-banner-tablet/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  @PostMapping("bet-receipt-banner-tablet/{id}/image")
  public ResponseEntity uploadImage(
      @PathVariable("id") String id, @RequestParam("file") MultipartFile file) {

    return betReceiptTabletService
        .findOne(id)
        .map(betReceipt -> betReceiptTabletService.uploadImage(betReceipt, file).get())
        .map(betReceiptTabletService::save)
        .map(ResponseEntity::ok)
        .orElseGet(notFound());
  }

  @DeleteMapping("bet-receipt-banner-tablet/{id}/image")
  public ResponseEntity removeImage(@PathVariable("id") String id) {
    BetReceiptBannerTablet betReceiptBannerTablet =
        betReceiptTabletService.findOne(id).orElseThrow(NotFoundException::new);

    return betReceiptTabletService
        .removeImages(betReceiptBannerTablet)
        .map(betReceiptTabletService::save)
        .map(ResponseEntity::ok)
        .orElseGet(failedToRemoveImage());
  }
}
