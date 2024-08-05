package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.constants.FZConstants;
import com.ladbrokescoral.oxygen.cms.api.dto.FanzoneNewSignpostingDto;
import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneNewSignposting;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.exception.FanzoneNewSignpostingCreateException;
import com.ladbrokescoral.oxygen.cms.api.service.CrudService;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesNewSignpostingService;
import java.util.Optional;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class FanzonesNewSignposting extends AbstractCrudController<FanzoneNewSignposting> {

  private final FanzonesNewSignpostingService fanzonesNewSignpostingService;

  private ModelMapper modelMapper;

  private CrudService<User> userService;

  @Autowired
  public FanzonesNewSignposting(
      CrudService<User> userService,
      FanzonesNewSignpostingService fanzonesNewSignpostingService,
      ModelMapper modelMapper) {
    super(fanzonesNewSignpostingService);
    this.userService = userService;
    this.modelMapper = modelMapper;
    this.fanzonesNewSignpostingService = fanzonesNewSignpostingService;
  }

  @PostMapping("{brand}/fanzone-new-signposting")
  public ResponseEntity<FanzoneNewSignposting> create(
      @RequestBody FanzoneNewSignpostingDto entity, @PathVariable String brand) {
    try {
      FanzoneNewSignposting fanzoneNewSignposting =
          modelMapper.map(entity, FanzoneNewSignposting.class);
      fanzoneNewSignposting =
          fanzonesNewSignpostingService.getFanzoneNewSignposting(fanzoneNewSignposting, brand);
      return super.create(
          fanzonesNewSignpostingService.populateCreatorAndUpdater(
              userService, fanzoneNewSignposting.prepareModelBeforeSave()));
    } catch (FanzoneNewSignpostingCreateException e) {
      throw new FanzoneNewSignpostingCreateException(
          FZConstants.FANZONENEWSIGNPOSTING_ALREADYEXISTS);
    }
  }

  @GetMapping("{brand}/fanzone-new-signposting")
  public Optional<FanzoneNewSignposting> findAllByBrand(@PathVariable String brand) {
    return fanzonesNewSignpostingService.findAllByBrand(brand);
  }

  @PutMapping("{brand}/fanzone-new-signposting/id/{id}")
  public FanzoneNewSignposting updateFanzoneNewSignposting(
      @PathVariable String brand,
      @PathVariable String id,
      @RequestBody FanzoneNewSignpostingDto entity) {
    FanzoneNewSignposting fanzoneNewSignposting =
        fanzonesNewSignpostingService.findAllByBrandAndId(brand, id);
    FanzoneNewSignposting updatedFanzoneNewSignposting =
        modelMapper.map(entity, FanzoneNewSignposting.class);
    return super.update(
        fanzoneNewSignposting.getId(),
        fanzonesNewSignpostingService.populateCreatorAndUpdater(
            userService, updatedFanzoneNewSignposting.prepareModelBeforeSave()));
  }
}
