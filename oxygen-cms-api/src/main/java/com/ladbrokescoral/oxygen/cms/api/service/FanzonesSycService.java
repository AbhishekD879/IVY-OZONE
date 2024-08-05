package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.constants.FZConstants;
import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneComingBack;
import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneOptinEmail;
import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneSyc;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.exception.FanzoneSycCreateException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesSycRepository;
import com.ladbrokescoral.oxygen.cms.util.Util;
import java.util.Optional;
import javax.validation.constraints.NotNull;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.validation.annotation.Validated;

@Slf4j
@Component
@Validated
public class FanzonesSycService extends AbstractService<FanzoneSyc> {

  private FanzonesSycRepository fanzonesSycRepository;

  private FanzonesComingBackService fanzonesComingBackService;

  private FanzonesOptinEmailService fanzonesOptinEmailService;

  @Autowired
  public FanzonesSycService(
      FanzonesSycRepository fanzonesSycRepository,
      FanzonesComingBackService fanzonesComingBackService,
      FanzonesOptinEmailService fanzonesOptinEmailService) {
    super(fanzonesSycRepository);
    this.fanzonesSycRepository = fanzonesSycRepository;
    this.fanzonesComingBackService = fanzonesComingBackService;
    this.fanzonesOptinEmailService = fanzonesOptinEmailService;
  }

  // to get specific fanzonesyc based on brand and id
  public FanzoneSyc findByBrandPageNameAndColumn(
      String brand, String pageName, String column, String val) {
    Optional<FanzoneSyc> fanzoneSyc =
        fanzonesSycRepository.findByBrandPageNameAndColumn(brand, pageName, column, val);
    return fanzoneSyc.isPresent() ? fanzoneSyc.get() : new FanzoneSyc();
  }

  // to get fanzonesyc based on brand
  public Optional<FanzoneSyc> findAllByBrandAndPageName(String brand, String pageName) {
    Optional<FanzoneSyc> fanzonesyc =
        fanzonesSycRepository.findAllByBrandAndPageName(brand, pageName);
    if (fanzonesyc.isPresent()) {
      return fanzonesyc;
    } else {
      return Optional.of(new FanzoneSyc());
    }
  }

  // to delete all fanzonesyc
  public void deleteAllByBrandPageName(String brand, String pageName) {
    Optional<FanzoneSyc> fanzonesycs =
        fanzonesSycRepository.findAllByBrandAndPageName(brand, pageName);
    if (fanzonesycs.isPresent()) {
      fanzonesSycRepository.delete(fanzonesycs.get());
    } else {
      throw new NotFoundException();
    }
  }

  // This method is used to check if FanzoneSyc is present or not
  public Boolean checkFanzoneSyc(String brand, String pageName) {
    Optional<FanzoneSyc> fanzoneSyc =
        fanzonesSycRepository.findAllByBrandAndPageName(brand, pageName);
    Boolean isFanzoneSycCreated = false;
    if (fanzoneSyc.isPresent()) {
      isFanzoneSycCreated = true;
    }
    return isFanzoneSycCreated;
  }

  // to check if fanzonesyc already exixts
  public FanzoneSyc getFanzoneSyc(FanzoneSyc dto, String brand, String pageName) {
    Boolean isFanzoneSycCreated = checkFanzoneSyc(brand, pageName);
    if (Boolean.TRUE.equals(isFanzoneSycCreated)) {
      throw new FanzoneSycCreateException(FZConstants.FANZONESYC_ALREADYEXIST);
    } else {
      return createFanzoneSyc(dto, brand);
    }
  }

  // to create Fanzonesyc
  private FanzoneSyc createFanzoneSyc(FanzoneSyc fanzoneSyc, String brand) {
    fanzoneSyc.setBrand(brand);
    return fanzoneSyc;
  }

  public void setSeasonStartDateForFanzoneComingBack(FanzoneSyc fanzoneSyc, String brand) {
    try {
      Optional<FanzoneComingBack> fanzoneComingBack =
          fanzonesComingBackService.findAllByBrand(brand);
      if (fanzoneComingBack.isPresent()) {
        fanzoneComingBack.get().setFzSeasonStartDate(fanzoneSyc.getSeasonStartDate());
        fanzonesComingBackService.save(fanzoneComingBack.get());
      } else {
        throw new NotFoundException();
      }
    } catch (NotFoundException e) {
      log.error("Fanzone Coming Back doesnot exist  ", e);
    }
  }

  public FanzoneSyc populateCreatorAndUpdater(
      CrudService<User> userServiceObj, @NotNull FanzoneSyc entity) {
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

  public void setSeasonStartAndEndDateForFanzoneOptinEmail(FanzoneSyc fanzoneSyc, String brand) {
    Optional<FanzoneOptinEmail> fanzoneOptinEmail =
        fanzonesOptinEmailService.findFanzoneOptinEmailByBrand(brand);
    if (fanzoneOptinEmail.isPresent()) {
      fanzoneOptinEmail.get().setSeasonStartDate(fanzoneSyc.getSeasonStartDate());
      fanzoneOptinEmail.get().setSeasonEndDate(fanzoneSyc.getSeasonEndDate());
      fanzonesOptinEmailService.save(fanzoneOptinEmail.get());
    }
  }
}
