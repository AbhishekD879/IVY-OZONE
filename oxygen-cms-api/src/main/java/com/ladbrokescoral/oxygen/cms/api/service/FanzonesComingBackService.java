package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.constants.FZConstants;
import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneComingBack;
import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneSyc;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.exception.FanzoneComingBackCreateException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesComingBackRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesSycRepository;
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
public class FanzonesComingBackService extends AbstractService<FanzoneComingBack> {

  private FanzonesComingBackRepository fanzonesComingBackRepository;
  private FanzonesSycRepository fanzonesSycRepository;

  @Autowired
  public FanzonesComingBackService(
      FanzonesComingBackRepository fanzonesComingBackRepository,
      FanzonesSycRepository fanzonesSycRepository) {
    super(fanzonesComingBackRepository);
    this.fanzonesComingBackRepository = fanzonesComingBackRepository;
    this.fanzonesSycRepository = fanzonesSycRepository;
  }

  private FanzoneComingBack createFanzoneComingBack(
      FanzoneComingBack fanzoneComingBack, String brand) {
    fanzoneComingBack.setBrand(brand);
    return fanzoneComingBack;
  }

  public FanzoneComingBack setSeasonStartDateFromFanzoneSyc(
      FanzoneComingBack fanzoneComingBack, String brand) {
    try {
      List<FanzoneSyc> fanzoneSyc = fanzonesSycRepository.findByBrand(brand);
      fanzoneComingBack.setFzSeasonStartDate(fanzoneSyc.get(0).getSeasonStartDate());
    } catch (IndexOutOfBoundsException e) {
      log.error("FanzoneSyc doesnot exist  ", e);
    }
    return fanzoneComingBack;
  }

  public Optional<FanzoneComingBack> findAllByBrand(String brand) {
    Optional<FanzoneComingBack> fanzoneComingBack =
        fanzonesComingBackRepository.findAllByBrand(brand);
    if (fanzoneComingBack.isPresent()) {
      return fanzoneComingBack;
    } else {
      return Optional.of(new FanzoneComingBack());
    }
  }

  public FanzoneComingBack findAllByBrandAndId(String brand, String id) {
    Optional<FanzoneComingBack> fanzoneComingBack =
        fanzonesComingBackRepository.findAllByBrandAndId(brand, id);
    return fanzoneComingBack.isPresent() ? fanzoneComingBack.get() : new FanzoneComingBack();
  }

  public Boolean checkFanzoneComingBack(String brand) {
    Optional<FanzoneComingBack> fanzoneComingBack =
        fanzonesComingBackRepository.findAllByBrand(brand);
    Boolean isFanzoneNewSeaosnCreated = false;
    if (fanzoneComingBack.isPresent()) {
      isFanzoneNewSeaosnCreated = true;
    }
    return isFanzoneNewSeaosnCreated;
  }

  public FanzoneComingBack getFanzoneComingBack(FanzoneComingBack dto, String brand) {
    Boolean isFanzoneComingBackCreated = checkFanzoneComingBack(brand);
    if (Boolean.TRUE.equals(isFanzoneComingBackCreated)) {
      throw new FanzoneComingBackCreateException(FZConstants.FANZONECOMINGBACK_ALREADYEXIST);
    } else {
      return createFanzoneComingBack(dto, brand);
    }
  }

  public void deleteAllByBrand(String brand) {
    Optional<FanzoneComingBack> fanzonesComingBack =
        fanzonesComingBackRepository.findAllByBrand(brand);
    if (fanzonesComingBack.isPresent()) {
      fanzonesComingBackRepository.delete(fanzonesComingBack.get());
    } else {
      throw new NotFoundException();
    }
  }

  public FanzoneComingBack populateCreatorAndUpdater(
      CrudService<User> userServiceObj, @NotNull FanzoneComingBack entity) {
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
