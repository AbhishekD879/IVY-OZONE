package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.Fanzone;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.service.CrudService;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesService;
import com.ladbrokescoral.oxygen.cms.util.Util;
import java.util.List;
import java.util.Optional;
import javax.validation.Valid;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@Slf4j
@RestController
public class Fanzones extends AbstractCrudController<Fanzone> {

  private final FanzonesService fanzonesService;
  private CrudService<User> userService;

  @Autowired
  public Fanzones(FanzonesService fanzonesService, CrudService<User> userService) {
    super(fanzonesService);
    this.fanzonesService = fanzonesService;
    this.userService = userService;
  }

  /**
   * to create fanzone
   *
   * @param dto for payload
   * @param brand represents the brand for which fanzone is being created
   * @return the created fanzone after checking there is no existing fanzone with the same name or
   *     same teamId
   */
  @PostMapping("{brand}/fanzone")
  public ResponseEntity<Fanzone> create(@RequestBody Object dto, @PathVariable String brand) {
    log.info("creating fanzone");
    ResponseEntity<Fanzone> responseEntity = null;
    Fanzone fanzoneEntity = (Util.objectMapper().convertValue(dto, Fanzone.class));
    fanzoneEntity = fanzonesService.processFanzone(fanzoneEntity, brand);
    responseEntity =
        super.create(
            fanzonesService.populateCreatorAndUpdater(
                userService, (Fanzone) fanzoneEntity.prepareModelBeforeSave()));
    log.info("fanzone created");
    return responseEntity;
  }

  /**
   * to get a specific fanzone
   *
   * @param brand represents brand name
   * @param column represents the column name
   * @param val represents the value of column
   * @return it will return the requested single Fanzone
   */
  @GetMapping("{brand}/fanzone/{column}/{val}")
  public Fanzone findByPagenameAndColumn(
      @PathVariable String brand, @PathVariable String column, @PathVariable String val) {
    log.info("getting fanzone from db");
    return fanzonesService.findByBrandAndColumn(brand, column, val);
  }

  /**
   * to retrieve all fanzones
   *
   * @param brand represents brand name
   * @return it will return all the Fanzones
   */
  @GetMapping("{brand}/fanzone")
  public Optional<List<Fanzone>> findAllByPageName(@PathVariable String brand) {
    log.info("getting all fanzones");
    return fanzonesService.findAllFanzonesByBrand(brand);
  }

  /**
   * to update an existing fanzone
   *
   * @param brand represents brand name
   * @param column represents the column name
   * @param value represents the value of column
   * @param dto for holding requested payload
   * @return it will return the updated Fanzone
   */
  @PutMapping("{brand}/fanzone/{column}/{value}")
  public Fanzone updatePageNameAndColumn(
      @PathVariable String brand,
      @PathVariable String column,
      @PathVariable String value,
      @RequestBody @Valid Object dto) {
    log.info("updating fanzone");
    Fanzone fanzoneindb = fanzonesService.findByBrandAndColumn(brand, column, value);
    Fanzone fanzoneEntity = Util.objectMapper().convertValue(dto, Fanzone.class);
    fanzoneEntity = fanzonesService.processFanzoneForUpdate(fanzoneEntity, brand, fanzoneindb);
    fanzoneEntity.setBrand(fanzoneindb.getBrand());
    return super.update(
        fanzoneindb.getId(),
        fanzonesService.populateCreatorAndUpdater(
            userService, (Fanzone) fanzoneEntity.prepareModelBeforeSave()));
  }

  /**
   * To delete all fanzones
   *
   * @param brand represent the brand name
   */
  @DeleteMapping("{brand}/fanzone")
  public void deleteAllByBrandAndPageName(@PathVariable String brand) {
    log.info("deleting all fanzones");
    fanzonesService.deleteAllByBrand(brand);
  }

  /**
   * To delete multiple fanzones
   *
   * @param brand represent the brand name
   * @param column represents the column name
   * @param values represents the value of column
   */
  @DeleteMapping("{brand}/fanzone/{column}/{values}")
  public void deleteByBrandAndColumn(
      @PathVariable String brand, @PathVariable String column, @PathVariable List<String> values) {
    log.info("deleting fanzone by ids");
    for (String value : values) fanzonesService.deleteByBrandAndColumn(brand, column, value);
  }
}
