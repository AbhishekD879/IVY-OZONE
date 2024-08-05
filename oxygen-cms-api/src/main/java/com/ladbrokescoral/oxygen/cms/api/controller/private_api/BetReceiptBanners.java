package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BetReceiptBanner;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.BetReceiptBannerService;
import java.util.List;
import javax.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class BetReceiptBanners extends AbstractImageController<BetReceiptBanner> {
  private BetReceiptBannerService betReceiptService;

  @Autowired
  public BetReceiptBanners(BetReceiptBannerService crudService) {
    super(crudService);
    betReceiptService = crudService;
  }

  @PostMapping("bet-receipt-banner")
  public ResponseEntity create(@RequestBody @Valid BetReceiptBanner entity) {
    return super.create(entity);
  }

  @GetMapping("bet-receipt-banner")
  @Override
  public List<BetReceiptBanner> readAll() {
    return super.readAll();
  }

  @GetMapping("bet-receipt-banner/{id}")
  @Override
  public BetReceiptBanner read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("bet-receipt-banner/brand/{brand}")
  @Override
  public List<BetReceiptBanner> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PutMapping("bet-receipt-banner/{id}")
  public BetReceiptBanner update(
      @PathVariable String id, @RequestBody @Valid BetReceiptBanner entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("bet-receipt-banner/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @Override
  @PostMapping("bet-receipt-banner/ordering")
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  @PostMapping("bet-receipt-banner/{id}/image")
  public ResponseEntity uploadImage(
      @PathVariable("id") String id, @RequestParam("file") MultipartFile file) {

    return betReceiptService
        .findOne(id)
        .map(betReceipt -> betReceiptService.uploadImage(betReceipt, file).get())
        .map(betReceiptService::save)
        .map(ResponseEntity::ok)
        .orElseGet(notFound());
  }

  @DeleteMapping("bet-receipt-banner/{id}/image")
  public ResponseEntity removeImage(@PathVariable("id") String id) {
    BetReceiptBanner betReceiptBanner =
        betReceiptService.findOne(id).orElseThrow(NotFoundException::new);

    return betReceiptService
        .removeImages(betReceiptBanner)
        .map(betReceiptService::save)
        .map(ResponseEntity::ok)
        .orElseGet(failedToRemoveImage());
  }
}
