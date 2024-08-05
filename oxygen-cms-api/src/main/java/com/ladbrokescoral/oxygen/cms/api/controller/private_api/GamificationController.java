package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.GamificationDetailsDto;
import com.ladbrokescoral.oxygen.cms.api.dto.GamificationDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Gamification;
import com.ladbrokescoral.oxygen.cms.api.service.GamificationService;
import java.util.List;
import java.util.Optional;
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
@SuppressWarnings("java:S4684")
public class GamificationController extends AbstractCrudController<Gamification> {

  private GamificationService gamificationService;

  GamificationController(GamificationService gamificationService) {
    super(gamificationService);
    this.gamificationService = gamificationService;
  }

  @PostMapping("/gamification")
  @Override
  public ResponseEntity<Gamification> create(@RequestBody @Valid Gamification entity) {
    return super.create(entity);
  }

  @PutMapping("/gamification/{id}")
  public Optional<GamificationDetailsDto> updateById(
      @PathVariable String id, @RequestBody @Valid Gamification entity) {
    Gamification gamification = super.update(id, entity);
    return gamificationService.getGamificationDetailsById(gamification);
  }

  @GetMapping("/gamification/{id}")
  public Optional<GamificationDetailsDto> getGamificationDetails(@PathVariable String id) {
    Gamification gamification = super.read(id);
    return gamificationService.getGamificationDetailsById(gamification);
  }

  @GetMapping("/gamification/brand/{brand}")
  public List<GamificationDto> findGamificationByBrand(@PathVariable String brand) {
    return gamificationService.findGamificationByBrand(brand);
  }

  @DeleteMapping("/gamification/{id}")
  @Override
  public ResponseEntity<Gamification> delete(@PathVariable String id) {
    return super.delete(id);
  }
}
