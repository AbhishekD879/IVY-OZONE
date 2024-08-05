package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Offer;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.OfferService;
import java.util.List;
import java.util.Optional;
import javax.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class Offers extends AbstractSortableController<Offer> {
  private OfferService offerService;

  @Autowired
  Offers(OfferService offerService) {
    super(offerService);
    this.offerService = offerService;
  }

  @PostMapping("offer")
  @Override
  public ResponseEntity create(@RequestBody @Valid Offer entity) {
    return super.create(entity);
  }

  @GetMapping("offer")
  @Override
  public List<Offer> readAll() {
    return super.readAll();
  }

  @GetMapping("offer/{id}")
  @Override
  public Offer read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("offer/brand/{brand}")
  @Override
  public List<Offer> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PutMapping("offer/{id}")
  @Override
  public Offer update(@PathVariable String id, @RequestBody @Valid Offer entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("offer/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    removeImage(id);
    return super.delete(id);
  }

  @PostMapping("offer/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  @PostMapping("offer/{id}/image")
  public ResponseEntity uploadImage(
      @PathVariable("id") String id, @RequestParam("file") MultipartFile file) {
    Optional<Offer> maybeEntity = offerService.findOne(id);
    if (!maybeEntity.isPresent()) {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }
    Optional<Offer> offerOptional = offerService.attachImage(maybeEntity.get(), file);
    return offerOptional
        .map(
            offer -> {
              Offer saved = offerService.save(offer);
              return new ResponseEntity(saved, HttpStatus.OK);
            })
        .orElseGet(() -> new ResponseEntity("Failed to upload image", HttpStatus.BAD_REQUEST));
  }

  @DeleteMapping("offer/{id}/image")
  public ResponseEntity removeImage(@PathVariable("id") String id) {
    Offer offer = offerService.findOne(id).orElseThrow(NotFoundException::new);

    return offerService
        .removeImage(offer)
        .map(offerService::save)
        .map(ResponseEntity::ok)
        .orElseGet(failedToRemoveImage());
  }
}
