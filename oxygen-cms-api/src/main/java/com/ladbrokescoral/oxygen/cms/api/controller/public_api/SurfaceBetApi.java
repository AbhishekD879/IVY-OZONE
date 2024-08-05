package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.service.SurfaceBetService;
import java.util.Set;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

/** @author PBalarangakumar 06-07-2023 */
@RestController
public class SurfaceBetApi implements Public {

  private final SurfaceBetService surfaceBetService;

  public SurfaceBetApi(final SurfaceBetService surfaceBetService) {
    this.surfaceBetService = surfaceBetService;
  }

  @GetMapping("active-surface-bets/{brand}")
  public ResponseEntity<Set<String>> findActiveSurfaceBetsByBrand(@PathVariable String brand) {
    return ResponseEntity.ok(surfaceBetService.findActiveSurfaceBetsByBrand(brand));
  }
}
