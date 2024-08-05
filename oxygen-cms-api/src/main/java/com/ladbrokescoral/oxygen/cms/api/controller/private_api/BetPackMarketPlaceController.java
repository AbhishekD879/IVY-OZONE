package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.BetPackDto;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BetPackEntity;
import com.ladbrokescoral.oxygen.cms.api.exception.BetPackMarketPlaceException;
import com.ladbrokescoral.oxygen.cms.api.service.BetPackMarketPlaceService;
import java.time.Instant;
import java.util.List;
import javax.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class BetPackMarketPlaceController extends AbstractSortableController<BetPackEntity> {

  private final BetPackMarketPlaceService betEnablerService;

  public BetPackMarketPlaceController(BetPackMarketPlaceService betEnablerService) {
    super(betEnablerService);
    this.betEnablerService = betEnablerService;
  }

  @GetMapping("bet-packs")
  public List<BetPackEntity> getAllBetPack() {
    return super.readAll();
  }

  @GetMapping("bet-packs/brand/{brand}")
  public List<BetPackEntity> getBetPackByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PostMapping("bet-pack")
  public ResponseEntity<BetPackEntity> createBetPack(@Valid @RequestBody BetPackDto betPackDto) {
    if ((betPackDto.isFilterBetPack() && !betPackDto.getFilterList().isEmpty())
        || (!betPackDto.isFilterBetPack())) {
      BetPackEntity betPackEntity =
          betEnablerService.checkActiveBetPackLimit(betPackDto.getId(), betPackDto);
      return super.create(betPackEntity);
    } else {
      return new ResponseEntity<>(HttpStatus.PARTIAL_CONTENT);
    }
  }

  @PostMapping("bet-pack/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  @GetMapping("bet-pack/{id}")
  public ResponseEntity<BetPackEntity> getBetPack(@PathVariable String id) {
    return new ResponseEntity<>(super.read(id), HttpStatus.OK);
  }

  @GetMapping("bet-pack/active-ids/{brand}")
  public List<String> getActiveBetPackIds(@PathVariable String brand) {
    return betEnablerService.getActiveBetPackId(brand);
  }

  @PutMapping("bet-pack/{id}")
  public ResponseEntity<BetPackEntity> update(
      @PathVariable("id") String id, @Valid @RequestBody BetPackDto betPackDto) {
    betEnablerService.validateSortOrder(betPackDto);
    betEnablerService.checkActiveBetPackLimit(id, betPackDto);
    BetPackEntity updateEntity = betEnablerService.checkDateValidation(id, betPackDto);
    return new ResponseEntity<>(super.update(id, updateEntity), HttpStatus.OK);
  }

  @DeleteMapping("bet-pack/{id}")
  public ResponseEntity<BetPackEntity> deleteById(@PathVariable String id) {
    BetPackEntity betPackEntity = super.read(id);
    if (!(Instant.now().isAfter(betPackEntity.getBetPackStartDate())
        && (Instant.now().isBefore(betPackEntity.getMaxTokenExpirationDate())))) {
      return super.delete(id);
    }
    throw new BetPackMarketPlaceException(
        "Bet Pack has been active. It can only be deleted after all token expiry dates have passed.");
  }

  @DeleteMapping("bet-pack/internal/{id}")
  public ResponseEntity<BetPackEntity> deleteByIdInternal(@PathVariable String id) {
    return super.delete(id);
  }
}
