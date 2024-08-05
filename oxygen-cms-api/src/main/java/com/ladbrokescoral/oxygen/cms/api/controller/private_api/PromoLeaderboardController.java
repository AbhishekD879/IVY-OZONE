package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.PromoLeaderboardConfigDto;
import com.ladbrokescoral.oxygen.cms.api.entity.PromoLeaderboardConfig;
import com.ladbrokescoral.oxygen.cms.api.service.PromoLeaderboardService;
import java.util.List;
import javax.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@SuppressWarnings("java:S4684")
public class PromoLeaderboardController extends AbstractCrudController<PromoLeaderboardConfig> {

  private final PromoLeaderboardService promoLeaderboardService;

  PromoLeaderboardController(PromoLeaderboardService promoLeaderboardService) {
    super(promoLeaderboardService);
    this.promoLeaderboardService = promoLeaderboardService;
  }

  @PostMapping("/promo-leaderboard")
  @Override
  public ResponseEntity<PromoLeaderboardConfig> create(
      @RequestBody @Valid PromoLeaderboardConfig entity) {
    return super.create(entity);
  }

  @PutMapping("/promo-leaderboard/{id}")
  public PromoLeaderboardConfig update(
      @PathVariable String id,
      @RequestBody @Valid PromoLeaderboardConfig entity,
      @RequestParam("isFileChanged") boolean isFileChanged) {
    promoLeaderboardService.getFileChangedMap().put(id, isFileChanged);
    return super.update(id, entity);
  }

  @GetMapping("/promo-leaderboard/{id}")
  public PromoLeaderboardConfig readById(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("/promo-leaderboard/brand/{brand}")
  public List<PromoLeaderboardConfigDto> findAllPromoLeaderboard(@PathVariable String brand) {
    return promoLeaderboardService.findLeaderboardByBrand(brand);
  }

  // This API will be used in Nav Item
  @GetMapping("/promo-leaderboard/active/brand/{brand}")
  public List<PromoLeaderboardConfigDto> findAllActivePromoLeaderboard(@PathVariable String brand) {
    return promoLeaderboardService.findAllActiveLeaderboardByBrand(brand);
  }

  @DeleteMapping("/promo-leaderboard/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }
}
