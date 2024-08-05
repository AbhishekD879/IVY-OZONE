package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.RGYMetaInfoEntity;
import com.ladbrokescoral.oxygen.cms.api.service.RGYMetaInfoService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class RGYMetaInfoController extends AbstractSortableController<RGYMetaInfoEntity> {

  private RGYMetaInfoService rgyMetaInfoService;

  public RGYMetaInfoController(RGYMetaInfoService rgyMetaInfoService) {
    super(rgyMetaInfoService);
    this.rgyMetaInfoService = rgyMetaInfoService;
  }

  @GetMapping("rgy-mtaInfo/brand/{brand}")
  public ResponseEntity<RGYMetaInfoEntity> getRgyMetaInfo(@PathVariable String brand) {
    return rgyMetaInfoService.getRgyMetaInfo(brand);
  }

  @PutMapping("rgy-mtaInfo/{brand}/{rgyFlag}")
  public ResponseEntity<RGYMetaInfoEntity> updateRgyFlag(
      @PathVariable String brand, @PathVariable boolean rgyFlag) {
    return rgyMetaInfoService.updateRgyFlag(brand, rgyFlag);
  }
}
