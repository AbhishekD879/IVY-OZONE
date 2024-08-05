package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.constants.FZConstants;
import com.ladbrokescoral.oxygen.cms.api.entity.PreferenceCentre;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.exception.PreferenceCentreCreateException;
import com.ladbrokescoral.oxygen.cms.api.repository.PreferenceCentresRepository;
import com.ladbrokescoral.oxygen.cms.util.Util;
import java.util.List;
import java.util.Optional;
import javax.validation.constraints.NotNull;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.validation.annotation.Validated;

@Slf4j
@Component
@Validated
public class PreferenceCentresService extends AbstractService<PreferenceCentre> {

  private PreferenceCentresRepository preferenceCentresRepository;

  @Autowired
  public PreferenceCentresService(PreferenceCentresRepository preferenceCentresRepository) {
    super(preferenceCentresRepository);
    this.preferenceCentresRepository = preferenceCentresRepository;
  }

  // to get all preference centres based on brand
  public Optional<PreferenceCentre> findAllPreferencesByBrand(String brand) {
    Optional<PreferenceCentre> preferenceCentre =
        preferenceCentresRepository.findAllPreferencesByBrand(brand);
    if (preferenceCentre.isPresent()) {
      return preferenceCentre;
    } else {
      return Optional.of(new PreferenceCentre());
    }
  }

  // to get specific preference centre based on brand and id
  public PreferenceCentre findByBrandAndColumn(String brand, String column, String val) {
    Optional<PreferenceCentre> preferenceCentre =
        preferenceCentresRepository.findByBrandAndColumn(brand, column, val);
    return preferenceCentre.isPresent() ? preferenceCentre.get() : new PreferenceCentre();
  }

  // to delete all preference centres
  public void deleteAllByBrand(String brand) {
    Optional<PreferenceCentre> preferences =
        preferenceCentresRepository.findAllPreferencesByBrand(brand);
    if (preferences.isPresent()) {
      preferenceCentresRepository.delete(preferences.get());
    } else {
      throw new NotFoundException();
    }
  }

  // to check if a preference centre already exists
  public Boolean checkPreferenceCentre(String brand) {
    List<PreferenceCentre> preferenceCentre = preferenceCentresRepository.findByBrand(brand);
    Boolean isPreferenceCentreCreated = true;
    if (preferenceCentre.isEmpty()) {
      isPreferenceCentreCreated = false;
    }
    return isPreferenceCentreCreated;
  }

  // to check if a preference centre already exists
  public PreferenceCentre getPreferenceCentre(Object dto, String brand) {
    Boolean isPreferenceCentreCreated = checkPreferenceCentre(brand);
    if (Boolean.TRUE.equals(isPreferenceCentreCreated)) {
      throw new PreferenceCentreCreateException(FZConstants.PREFERENCECENTRE_ALREADYEXIST);
    } else {
      return createPreferenceCentre(dto, brand);
    }
  }

  // to create a preference centre
  private PreferenceCentre createPreferenceCentre(Object dto, String brand) {
    PreferenceCentre preferenceCentre =
        Util.objectMapper().convertValue(dto, PreferenceCentre.class);
    preferenceCentre.setBrand(brand);
    return preferenceCentre;
  }

  public PreferenceCentre populateCreatorAndUpdater(
      CrudService<User> userServiceObj, @NotNull PreferenceCentre entity) {
    Optional.ofNullable(entity.getCreatedBy())
        .filter(Util::isValidObjectIdString)
        .flatMap(userServiceObj::findOne)
        .ifPresent(user -> entity.setCreatedByUserName(user.getEmail()));

    Optional.ofNullable(entity.getUpdatedBy())
        .filter(Util::isValidObjectIdString)
        .flatMap(userServiceObj::findOne)
        .ifPresent(user -> entity.setUpdatedByUserName(user.getEmail()));
    return entity;
  }
}
