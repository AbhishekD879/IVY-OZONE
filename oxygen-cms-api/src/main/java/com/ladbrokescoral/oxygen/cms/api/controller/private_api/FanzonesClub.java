package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.FanzoneClubDto;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.service.CrudService;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesClubService;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@Slf4j
@RestController
public class FanzonesClub extends AbstractCrudController<FanzoneClub> {
  private final FanzonesClubService fanzonesClubService;
  private CrudService<User> userService;
  private ModelMapper modelMapper;

  @Autowired
  public FanzonesClub(
      FanzonesClubService fanzonesClubService,
      CrudService<User> userService,
      ModelMapper modelMapper) {
    super(fanzonesClubService);
    this.fanzonesClubService = fanzonesClubService;
    this.userService = userService;
    this.modelMapper = modelMapper;
  }

  /**
   * This API call is used to create FanzoneClub
   *
   * @param entity represent FanzoneClubDto
   * @param brand represent brand name
   * @return it will return created entity
   */
  @PostMapping("{brand}/fanzone-club")
  public ResponseEntity<FanzoneClub> create(
      @RequestBody FanzoneClubDto entity, @PathVariable String brand) {
    log.info("FanzoneClub is created");
    FanzoneClub fanzoneClub = modelMapper.map(entity, FanzoneClub.class);
    return super.create(
        fanzonesClubService.populateCreatorAndUpdater(
            userService, (FanzoneClub) fanzoneClub.prepareModelBeforeSave()));
  }

  /**
   * This API call is used to get single FanzoneClub
   *
   * @param brand represent brand name
   * @param column represent the column name
   * @param val represent the value of column
   * @return it will return the requested single FanzoneClub.
   */
  @GetMapping("{brand}/fanzone-club/{column}/{val}")
  public FanzoneClub findByPagenameAndColumn(
      @PathVariable String brand, @PathVariable String column, @PathVariable String val) {
    log.info("getting fanzoneclub from database");
    return super.read(val);
  }

  /**
   * This API call is used to get all the FanzoneClubs.
   *
   * @param brand represent brand name
   * @return it will return all the requested FanzoneClubs.
   */
  @GetMapping("{brand}/fanzone-club")
  public List<FanzoneClub> findAllByPageName(@PathVariable String brand) {
    log.info("getting all FanzoneClubs from database");
    return super.readAll();
  }

  /**
   * This API call is used for updating FanzoneClub
   *
   * @param brand represent brand name
   * @param column represent the column name
   * @param value represent the value of column
   * @param entity represent FanzoneClubDto
   * @return it will return updated FanzoneClub
   */
  @PutMapping("{brand}/fanzone-club/{column}/{value}")
  public FanzoneClub updatePageNameAndColumn(
      @PathVariable String brand,
      @PathVariable String column,
      @PathVariable String value,
      @RequestBody FanzoneClubDto entity) {
    FanzoneClub updatedFanzoneClub = modelMapper.map(entity, FanzoneClub.class);
    FanzoneClub fanzoneClub = fanzonesClubService.findByBrandAndColumn(brand, column, value);
    log.info("fanzoneclub is Updated");
    return super.update(
        fanzoneClub.getId(),
        fanzonesClubService.populateCreatorAndUpdater(
            userService, (FanzoneClub) updatedFanzoneClub.prepareModelBeforeSave()));
  }

  /**
   * This API call is used to delete all FanzoneClubs.
   *
   * @param brand represent brand name
   */
  @DeleteMapping("{brand}/fanzone-club")
  public void deleteAllByBrandAndPageName(@PathVariable String brand) {
    log.info("deleting fanzoneclub");
    fanzonesClubService.deleteAllByBrand(brand);
  }

  /**
   * This API call is used to delete single/multiple FanzoneClubs.
   *
   * @param brand represent brand name
   * @param column represent the column name
   * @param values represent the value of column
   */
  @DeleteMapping("{brand}/fanzone-club/{column}/{values}")
  public void deleteByBrandAndColumn(
      @PathVariable String brand, @PathVariable String column, @PathVariable List<String> values) {
    log.info("deleting all fanzoneclubs");
    for (String value : values) fanzonesClubService.deleteByBrandAndColumn(brand, column, value);
  }
}
