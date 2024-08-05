package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.constants.FZConstants;
import com.ladbrokescoral.oxygen.cms.api.dto.FanzoneNewGamingPopUpDto;
import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneNewGamingPopUp;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.exception.FanzoneNewGamingPopUpException;
import com.ladbrokescoral.oxygen.cms.api.service.CrudService;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesNewGamingPopUpService;
import java.util.Optional;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class FanzonesNewGamingPopUp extends AbstractCrudController<FanzoneNewGamingPopUp> {

  private final FanzonesNewGamingPopUpService fanzonesNewGamingPopUpService;

  private ModelMapper modelMapper;

  private CrudService<User> userService;

  @Autowired
  public FanzonesNewGamingPopUp(
      CrudService<User> userService,
      FanzonesNewGamingPopUpService fanzonesNewGamingPopUpService,
      ModelMapper modelMapper) {
    super(fanzonesNewGamingPopUpService);
    this.userService = userService;
    this.fanzonesNewGamingPopUpService = fanzonesNewGamingPopUpService;
    this.modelMapper = modelMapper;
  }

  @PostMapping("{brand}/fanzone-new-gaming-pop-up")
  public ResponseEntity<FanzoneNewGamingPopUp> create(
      @RequestBody FanzoneNewGamingPopUpDto entity, @PathVariable String brand) {
    try {
      FanzoneNewGamingPopUp fanzoneNewGamingPopUp =
          modelMapper.map(entity, FanzoneNewGamingPopUp.class);
      fanzoneNewGamingPopUp =
          fanzonesNewGamingPopUpService.getFanzoneNewGamingPopUp(fanzoneNewGamingPopUp, brand);
      return super.create(
          fanzonesNewGamingPopUpService.populateCreatorAndUpdater(
              userService, fanzoneNewGamingPopUp.prepareModelBeforeSave()));
    } catch (FanzoneNewGamingPopUpException e) {
      throw new FanzoneNewGamingPopUpException(FZConstants.FANZONENEWGAMINGPOPUP_ALREADYEXISTS);
    }
  }

  @GetMapping("{brand}/fanzone-new-gaming-pop-up")
  public Optional<FanzoneNewGamingPopUp> getFanzoneNewGamingPopup(@PathVariable String brand) {
    return fanzonesNewGamingPopUpService.findAllByBrand(brand);
  }

  @PutMapping("{brand}/fanzone-new-gaming-pop-up/id/{id}")
  public FanzoneNewGamingPopUp updateFanzoneNewGamingPopup(
      @PathVariable String brand,
      @PathVariable String id,
      @RequestBody FanzoneNewGamingPopUpDto entity) {
    FanzoneNewGamingPopUp fanzoneNewGamingPopUp =
        fanzonesNewGamingPopUpService.findAllByBrandAndId(brand, id);
    FanzoneNewGamingPopUp updatedFanzoneNewGamingPopUp =
        modelMapper.map(entity, FanzoneNewGamingPopUp.class);
    return super.update(
        fanzoneNewGamingPopUp.getId(),
        fanzonesNewGamingPopUpService.populateCreatorAndUpdater(
            userService, updatedFanzoneNewGamingPopUp.prepareModelBeforeSave()));
  }
}
