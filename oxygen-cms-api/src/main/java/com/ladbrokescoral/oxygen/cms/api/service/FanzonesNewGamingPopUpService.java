package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.constants.FZConstants;
import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneNewGamingPopUp;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.exception.FanzoneNewGamingPopUpException;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesNewGamingPopUpRepository;
import com.ladbrokescoral.oxygen.cms.util.Util;
import java.util.Optional;
import javax.validation.constraints.NotNull;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.validation.annotation.Validated;

@Component
@Validated
public class FanzonesNewGamingPopUpService extends AbstractService<FanzoneNewGamingPopUp> {
  private FanzonesNewGamingPopUpRepository fanzonesNewGamingPopUpRepository;

  @Autowired
  public FanzonesNewGamingPopUpService(
      FanzonesNewGamingPopUpRepository fanzonesNewGamingPopUpRepository) {
    super(fanzonesNewGamingPopUpRepository);
    this.fanzonesNewGamingPopUpRepository = fanzonesNewGamingPopUpRepository;
  }

  private FanzoneNewGamingPopUp createFanzoneNewGamingPopUp(
      FanzoneNewGamingPopUp fanzoneNewGamingPopUp, String brand) {
    fanzoneNewGamingPopUp.setBrand(brand);
    return fanzoneNewGamingPopUp;
  }

  public Optional<FanzoneNewGamingPopUp> findAllByBrand(String brand) {
    Optional<FanzoneNewGamingPopUp> fanzoneNewGamingPopUp =
        fanzonesNewGamingPopUpRepository.findAllByBrand(brand);
    if (fanzoneNewGamingPopUp.isPresent()) {
      return fanzoneNewGamingPopUp;
    } else {
      return Optional.of(new FanzoneNewGamingPopUp());
    }
  }

  public FanzoneNewGamingPopUp findAllByBrandAndId(String brand, String id) {
    Optional<FanzoneNewGamingPopUp> fanzoneNewGamingPopUp =
        fanzonesNewGamingPopUpRepository.findAllByBrandAndId(brand, id);
    return fanzoneNewGamingPopUp.isPresent()
        ? fanzoneNewGamingPopUp.get()
        : new FanzoneNewGamingPopUp();
  }

  public Boolean checkFanzoneNewGamingPopUp(String brand) {
    Optional<FanzoneNewGamingPopUp> fanzoneNewGamingPopUp =
        fanzonesNewGamingPopUpRepository.findAllByBrand(brand);
    Boolean isFanzoneNewGamingPopUpCreated = false;
    if (fanzoneNewGamingPopUp.isPresent()) {
      isFanzoneNewGamingPopUpCreated = true;
    }
    return isFanzoneNewGamingPopUpCreated;
  }

  public FanzoneNewGamingPopUp getFanzoneNewGamingPopUp(FanzoneNewGamingPopUp dto, String brand) {
    Boolean isFanzoneNewGamingPopUpCreated = checkFanzoneNewGamingPopUp(brand);
    if (Boolean.TRUE.equals(isFanzoneNewGamingPopUpCreated)) {
      throw new FanzoneNewGamingPopUpException(FZConstants.FANZONENEWGAMINGPOPUP_ALREADYEXISTS);
    } else {
      return createFanzoneNewGamingPopUp(dto, brand);
    }
  }

  public FanzoneNewGamingPopUp populateCreatorAndUpdater(
      CrudService<User> userServiceObj, @NotNull FanzoneNewGamingPopUp entity) {
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
