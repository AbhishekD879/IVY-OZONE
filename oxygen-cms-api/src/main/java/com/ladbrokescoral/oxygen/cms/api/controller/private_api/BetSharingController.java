package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.BetSharingDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BetSharingEntity;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.BetSharingService;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import javax.validation.Valid;
import org.modelmapper.ModelMapper;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
public class BetSharingController extends AbstractCrudController<BetSharingEntity> {
  private final ModelMapper modelMapper;
  private final BetSharingService betSharingService;

  public BetSharingController(ModelMapper modelMapper, BetSharingService betSharingService) {
    super(betSharingService);
    this.modelMapper = modelMapper;
    this.betSharingService = betSharingService;
  }

  @PostMapping("/bet-sharing")
  public ResponseEntity<BetSharingEntity> createBetSharing(
      @Valid @Validated @RequestBody BetSharingDto betSharingDto) {
    BetSharingEntity betSharingEntity = modelMapper.map(betSharingDto, BetSharingEntity.class);
    return super.create(betSharingEntity);
  }

  @PutMapping("/bet-sharing/{id}")
  public BetSharingEntity updateBetSharing(
      @PathVariable("id") String id, @Valid @Validated @RequestBody BetSharingDto betSharingDto) {
    BetSharingEntity betSharingEntity = modelMapper.map(betSharingDto, BetSharingEntity.class);
    return super.update(id, betSharingEntity);
  }

  @DeleteMapping("/bet-sharing/{id}")
  public ResponseEntity<BetSharingEntity> deleteById(@PathVariable("id") String id) {
    return super.delete(id);
  }

  @GetMapping("/bet-sharing/brand/{brand}")
  public BetSharingEntity getByBrand(@Valid @Validated @Brand @PathVariable("brand") String brand) {
    return betSharingService.getBetSharingByBrand(brand).orElseThrow(NotFoundException::new);
  }
}
