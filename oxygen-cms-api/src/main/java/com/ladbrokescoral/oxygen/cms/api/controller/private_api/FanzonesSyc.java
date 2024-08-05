package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.constants.FZConstants;
import com.ladbrokescoral.oxygen.cms.api.dto.FanzoneSycDto;
import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneSyc;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.exception.FanzoneSycCreateException;
import com.ladbrokescoral.oxygen.cms.api.service.CrudService;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesSycService;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@Slf4j
@RestController
public class FanzonesSyc extends AbstractCrudController<FanzoneSyc> {

  private final FanzonesSycService fanzonesSycService;
  private CrudService<User> userService;
  private ModelMapper modelMapper;

  @Autowired
  public FanzonesSyc(
      FanzonesSycService fanzonesSycService,
      CrudService<User> userService,
      ModelMapper modelMapper) {
    super(fanzonesSycService);
    this.fanzonesSycService = fanzonesSycService;
    this.userService = userService;
    this.modelMapper = modelMapper;
  }

  /**
   * This API call is used to create FanzoneSyc.
   *
   * @param entity represent FanzoneSycDto
   * @param brand represent brand name
   * @param pageName represent fanzone-syc
   * @return
   */
  @PostMapping("{brand}/{pageName}")
  public ResponseEntity<FanzoneSyc> create(
      @RequestBody FanzoneSycDto entity,
      @PathVariable String brand,
      @PathVariable String pageName) {
    try {
      log.info("creating fanzonesyc");
      FanzoneSyc fanzoneSyc = modelMapper.map(entity, FanzoneSyc.class);
      fanzoneSyc = fanzonesSycService.getFanzoneSyc(fanzoneSyc, brand, pageName);
      return super.create(
          fanzonesSycService.populateCreatorAndUpdater(
              userService, (FanzoneSyc) fanzoneSyc.prepareModelBeforeSave()));
    } catch (FanzoneSycCreateException e) {
      log.error("FanzoneSyc already exists  ", e);
      throw new FanzoneSycCreateException(FZConstants.FANZONESYC_ALREADYEXIST);
    }
  }

  /**
   * This API call is used to get FanzoneSyc.
   *
   * @param brand represent brand name
   * @param pageName represent fanzone-syc
   * @return it will return FanzoneSyc.
   */
  @GetMapping("{brand}/{pageName}")
  public Optional<FanzoneSyc> findAllByBrandAndPageName(
      @PathVariable String brand, @PathVariable String pageName) {
    log.info("getting FanzoneSyc from database");
    return fanzonesSycService.findAllByBrandAndPageName(brand, pageName);
  }

  /**
   * This API call is used for updating FanzoneSyc
   *
   * @param brand represent brand name
   * @param pageName represent fanzone-syc
   * @param column represents the column name
   * @param value represents the value of column
   * @param entity represent FanzoneSycDto
   * @return it will return updated FanzoneSyc
   */
  @PutMapping("{brand}/{pageName}/{column}/{value}")
  public FanzoneSyc updatePageNameAndColumn(
      @PathVariable String brand,
      @PathVariable String pageName,
      @PathVariable String column,
      @PathVariable String value,
      @RequestBody FanzoneSycDto entity) {
    log.info("updating fanzonesyc");
    FanzoneSyc fanzoneSyc =
        fanzonesSycService.findByBrandPageNameAndColumn(brand, pageName, column, value);
    FanzoneSyc updatedFanzoneSyc = modelMapper.map(entity, FanzoneSyc.class);
    fanzonesSycService.setSeasonStartDateForFanzoneComingBack(updatedFanzoneSyc, brand);
    fanzonesSycService.setSeasonStartAndEndDateForFanzoneOptinEmail(updatedFanzoneSyc, brand);
    return super.update(
        fanzoneSyc.getId(),
        fanzonesSycService.populateCreatorAndUpdater(
            userService, (FanzoneSyc) updatedFanzoneSyc.prepareModelBeforeSave()));
  }
  /**
   * This API call is used to delete FanzoneSyc
   *
   * @param brand represent brand name
   * @param pageName represent fanzone-syc
   */
  @DeleteMapping("{brand}/{pageName}")
  public void deleteAllByBrandAndPageName(
      @PathVariable String brand, @PathVariable String pageName) {
    log.info("deleting fanzonesyc");
    fanzonesSycService.deleteAllByBrandPageName(brand, pageName);
  }
}
