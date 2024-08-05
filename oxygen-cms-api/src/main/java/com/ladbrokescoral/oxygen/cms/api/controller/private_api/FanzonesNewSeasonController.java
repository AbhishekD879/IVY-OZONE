package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.constants.FZConstants;
import com.ladbrokescoral.oxygen.cms.api.dto.FanzoneNewSeasonDto;
import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneNewSeason;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.exception.FanzoneNewSeasonCreateException;
import com.ladbrokescoral.oxygen.cms.api.service.CrudService;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesNewSeasonService;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@Slf4j
@RestController
public class FanzonesNewSeasonController extends AbstractCrudController<FanzoneNewSeason> {

  private FanzonesNewSeasonService fanzoneNewSeasonService;
  private CrudService<User> userService;
  private ModelMapper modelMapper;

  @Autowired
  public FanzonesNewSeasonController(
      FanzonesNewSeasonService fanzoneNewSeasonService,
      CrudService<User> userService,
      ModelMapper modelMapper) {
    super(fanzoneNewSeasonService);
    this.fanzoneNewSeasonService = fanzoneNewSeasonService;
    this.userService = userService;
    this.modelMapper = modelMapper;
  }

  @PostMapping("{brand}/fanzone-new-season")
  public ResponseEntity<FanzoneNewSeason> create(
      @RequestBody FanzoneNewSeasonDto entity, @PathVariable String brand) {
    try {
      FanzoneNewSeason fanzoneNewSeason = modelMapper.map(entity, FanzoneNewSeason.class);
      fanzoneNewSeason = fanzoneNewSeasonService.getFanzoneNewSeason(fanzoneNewSeason, brand);
      return super.create(
          fanzoneNewSeasonService.populateCreatorAndUpdater(
              userService, fanzoneNewSeason.prepareModelBeforeSave()));
    } catch (FanzoneNewSeasonCreateException e) {
      throw new FanzoneNewSeasonCreateException(FZConstants.FANZONENEWSEASON_ALREADYEXIST);
    }
  }

  @GetMapping("{brand}/fanzone-new-season")
  public Optional<FanzoneNewSeason> findAllByBrand(@PathVariable String brand) {
    return fanzoneNewSeasonService.findAllByBrand(brand);
  }

  @PutMapping("{brand}/fanzone-new-season/id/{id}")
  public FanzoneNewSeason updateFanzoneNewSeason(
      @PathVariable String brand,
      @PathVariable String id,
      @RequestBody FanzoneNewSeasonDto entity) {
    FanzoneNewSeason fanzoneNewSeason = fanzoneNewSeasonService.findAllByBrandAndId(brand, id);
    FanzoneNewSeason updatedfanzoneNewSeason = modelMapper.map(entity, FanzoneNewSeason.class);
    return super.update(
        fanzoneNewSeason.getId(),
        fanzoneNewSeasonService.populateCreatorAndUpdater(
            userService, updatedfanzoneNewSeason.prepareModelBeforeSave()));
  }

  @DeleteMapping("{brand}/fanzone-new-season")
  public void deleteAllByBrand(@PathVariable String brand) {
    fanzoneNewSeasonService.deleteAllByBrand(brand);
  }
}
