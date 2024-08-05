package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.Overlay;
import com.ladbrokescoral.oxygen.cms.api.service.OverlayService;
import java.util.List;
import java.util.Optional;
import javax.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/** OverLay Controller */
@RestController
public class OverlayController extends AbstractSortableController<Overlay> {

  private final OverlayService overlayService;

  @Autowired
  OverlayController(OverlayService overlayService) {
    super(overlayService);
    this.overlayService = overlayService;
  }

  /** Create Overlay */
  @PostMapping("overlay")
  @Override
  public ResponseEntity create(@RequestBody @Valid Overlay entity) {
    return super.create(entity);
  }

  /** List All Overlay */
  @GetMapping("overlay")
  @Override
  public List<Overlay> readAll() {
    return super.readAll();
  }

  /**
   * List All Overlay based on Id
   *
   * @param id - Overlay Id
   */
  @GetMapping("overlay/{id}")
  @Override
  public Overlay read(@PathVariable String id) {
    return super.read(id);
  }

  /**
   * Update Overlay based on Id
   *
   * @param id - Overlay Id
   */
  @PutMapping("overlay/{id}")
  @Override
  public Overlay update(@PathVariable String id, @RequestBody Overlay entity) {
    return super.update(id, entity);
  }

  /**
   * List All Overlay based on Brand
   *
   * @param brand - Brand
   */
  @GetMapping("overlay/brand/{brand}")
  public ResponseEntity<Overlay> readOneByBrand(@PathVariable String brand) {
    Optional<Overlay> optionalOverlay = overlayService.findOneByBrand(brand);

    if (optionalOverlay.isPresent()) {
      Overlay overlay = optionalOverlay.get();
      return new ResponseEntity<>(overlay, HttpStatus.OK);
    }
    return new ResponseEntity<>(HttpStatus.NOT_FOUND);
  }
}
