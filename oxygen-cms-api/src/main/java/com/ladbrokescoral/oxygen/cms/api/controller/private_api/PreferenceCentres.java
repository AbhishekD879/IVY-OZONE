package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.constants.FZConstants;
import com.ladbrokescoral.oxygen.cms.api.entity.PreferenceCentre;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.exception.PreferenceCentreCreateException;
import com.ladbrokescoral.oxygen.cms.api.service.CrudService;
import com.ladbrokescoral.oxygen.cms.api.service.PreferenceCentresService;
import com.ladbrokescoral.oxygen.cms.util.Util;
import java.util.Optional;
import javax.validation.Valid;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@Slf4j
@RestController
public class PreferenceCentres extends AbstractCrudController<PreferenceCentre> {

  private final PreferenceCentresService preferenceCentresService;
  private CrudService<User> userService;

  @Autowired
  public PreferenceCentres(
      PreferenceCentresService preferenceCentresService, CrudService<User> userService) {
    super(preferenceCentresService);
    this.preferenceCentresService = preferenceCentresService;
    this.userService = userService;
  }

  /**
   * to create a preference centre
   *
   * @param dto for holding requested payload
   * @param brand represents brand name
   * @return it will return the created preference centre
   */
  @PostMapping("{brand}/fanzone-preference-center")
  public ResponseEntity<PreferenceCentre> create(
      @RequestBody Object dto, @PathVariable String brand) {
    log.info("creating fanzone preference centre");
    ResponseEntity<PreferenceCentre> responseEntity = null;
    try {
      PreferenceCentre preferenceCentre = preferenceCentresService.getPreferenceCentre(dto, brand);
      responseEntity =
          super.create(
              preferenceCentresService.populateCreatorAndUpdater(
                  userService, (PreferenceCentre) preferenceCentre.prepareModelBeforeSave()));
    } catch (PreferenceCentreCreateException e) {
      log.error("preference centre already exists  ", e);
      throw new PreferenceCentreCreateException(FZConstants.PREFERENCECENTRE_ALREADYEXIST);
    }
    log.info("created fanzone preference centre");
    return responseEntity;
  }

  /**
   * to get preference centre
   *
   * @param brand represents brand name
   * @return the preference centre in the collection
   */
  @GetMapping("{brand}/fanzone-preference-center")
  public Optional<PreferenceCentre> findAllPreferencesByBrand(@PathVariable String brand) {
    log.info("getting fanzone preference centre");
    return preferenceCentresService.findAllPreferencesByBrand(brand);
  }

  /**
   * to update the existing preference centre
   *
   * @param brand represents brand name
   * @param column represents the column name
   * @param value represents the value of column
   * @param dto for holding requested payload
   * @return it will return the updated preference centre
   */
  @PutMapping("{brand}/fanzone-preference-center/{column}/{value}")
  public PreferenceCentre updatePageNameAndColumn(
      @PathVariable String brand,
      @PathVariable String column,
      @PathVariable String value,
      @RequestBody @Valid Object dto) {
    log.info("updating fanzone preference centre");
    PreferenceCentre preferenceCentre =
        preferenceCentresService.findByBrandAndColumn(brand, column, value);
    PreferenceCentre updatedPreferenceCentre =
        Util.objectMapper().convertValue(dto, PreferenceCentre.class);
    updatedPreferenceCentre.setBrand(brand);
    return super.update(
        preferenceCentre.getId(),
        preferenceCentresService.populateCreatorAndUpdater(
            userService, (PreferenceCentre) updatedPreferenceCentre.prepareModelBeforeSave()));
  }

  /**
   * to delete preference centre
   *
   * @param brand represents brand name
   */
  @DeleteMapping("{brand}/fanzone-preference-center")
  public void deleteAllByBrand(@PathVariable String brand) {
    log.info("deleting fanzone preference centre");
    preferenceCentresService.deleteAllByBrand(brand);
  }
}
