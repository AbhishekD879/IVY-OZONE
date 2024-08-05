package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.constants.FZConstants;
import com.ladbrokescoral.oxygen.cms.api.dto.FanzoneComingBackDto;
import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneComingBack;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.exception.FanzoneComingBackCreateException;
import com.ladbrokescoral.oxygen.cms.api.service.CrudService;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesComingBackService;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@Slf4j
@RestController
public class FanzonesComingBackController extends AbstractCrudController<FanzoneComingBack> {

  private FanzonesComingBackService fanzonesComingBackService;
  private CrudService<User> userService;
  private ModelMapper modelMapper;

  @Autowired
  public FanzonesComingBackController(
      FanzonesComingBackService fanzonesComingBackService,
      CrudService<User> userService,
      ModelMapper modelMapper) {
    super(fanzonesComingBackService);
    this.fanzonesComingBackService = fanzonesComingBackService;
    this.userService = userService;
    this.modelMapper = modelMapper;
  }

  @PostMapping("{brand}/fanzone-coming-back")
  public ResponseEntity<FanzoneComingBack> create(
      @RequestBody FanzoneComingBackDto entity, @PathVariable String brand) {
    try {
      FanzoneComingBack fanzoneComingBack = modelMapper.map(entity, FanzoneComingBack.class);
      fanzoneComingBack = fanzonesComingBackService.getFanzoneComingBack(fanzoneComingBack, brand);
      fanzoneComingBack =
          fanzonesComingBackService.setSeasonStartDateFromFanzoneSyc(fanzoneComingBack, brand);
      return super.create(
          fanzonesComingBackService.populateCreatorAndUpdater(
              userService, fanzoneComingBack.prepareModelBeforeSave()));
    } catch (FanzoneComingBackCreateException e) {
      throw new FanzoneComingBackCreateException(FZConstants.FANZONECOMINGBACK_ALREADYEXIST);
    }
  }

  @GetMapping("{brand}/fanzone-coming-back")
  public Optional<FanzoneComingBack> findAllByBrand(@PathVariable String brand) {
    return fanzonesComingBackService.findAllByBrand(brand);
  }

  @PutMapping("{brand}/fanzone-coming-back/id/{id}")
  public FanzoneComingBack updateFanzoneNewSeason(
      @PathVariable String brand,
      @PathVariable String id,
      @RequestBody FanzoneComingBackDto entity) {
    FanzoneComingBack fanzoneComingBack = fanzonesComingBackService.findAllByBrandAndId(brand, id);
    FanzoneComingBack updatedfanzoneComingBack = modelMapper.map(entity, FanzoneComingBack.class);
    updatedfanzoneComingBack =
        fanzonesComingBackService.setSeasonStartDateFromFanzoneSyc(updatedfanzoneComingBack, brand);
    return super.update(
        fanzoneComingBack.getId(),
        fanzonesComingBackService.populateCreatorAndUpdater(
            userService, updatedfanzoneComingBack.prepareModelBeforeSave()));
  }

  @DeleteMapping("{brand}/fanzone-coming-back")
  public void deleteAllByBrand(@PathVariable String brand) {
    fanzonesComingBackService.deleteAllByBrand(brand);
  }
}
