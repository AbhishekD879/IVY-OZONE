package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.SurfaceBetDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SurfaceBetPublicService;
import java.util.List;
import javax.validation.constraints.NotNull;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class EdpSurfaceBetApi implements Public {
  private final SurfaceBetPublicService surfaceBetPublicService;

  @GetMapping("{brand}/edp-surface-bets/{eventId}")
  public ResponseEntity<List<SurfaceBetDto>> findByBrandAndEventId(
      @PathVariable("brand") @NotNull String brand,
      @PathVariable("eventId") @NotNull String eventId) {
    return new ResponseEntity<>(
        surfaceBetPublicService.findActiveEdpSurfaceBets(brand, eventId), HttpStatus.OK);
  }
}
