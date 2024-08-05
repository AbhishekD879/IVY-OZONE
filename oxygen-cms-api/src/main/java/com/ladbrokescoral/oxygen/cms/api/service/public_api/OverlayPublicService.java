package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.Overlay;
import com.ladbrokescoral.oxygen.cms.api.service.OverlayService;
import java.util.List;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/** OverLay Service */
@Slf4j
@Service
public class OverlayPublicService {

  private final OverlayService service;

  @Autowired
  public OverlayPublicService(OverlayService service) {
    this.service = service;
  }

  public List<Overlay> findByBrand(String brand) {
    return service.findByBrand(brand);
  }

  public Optional<Overlay> findOneByBrand(String brand) {
    return service.findOneByBrand(brand);
  }
}
