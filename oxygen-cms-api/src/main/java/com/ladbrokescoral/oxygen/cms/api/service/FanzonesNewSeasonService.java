package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.constants.FZConstants;
import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneNewSeason;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.exception.FanzoneNewSeasonCreateException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesNewSeasonRepository;
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
public class FanzonesNewSeasonService extends AbstractService<FanzoneNewSeason> {

  private FanzonesNewSeasonRepository fanzonesNewSeasonRepository;

  @Autowired
  public FanzonesNewSeasonService(FanzonesNewSeasonRepository fanzonesNewSeasonRepository) {
    super(fanzonesNewSeasonRepository);
    this.fanzonesNewSeasonRepository = fanzonesNewSeasonRepository;
  }

  private FanzoneNewSeason createFanzoneNewSeason(FanzoneNewSeason fanzoneNewSeason, String brand) {
    fanzoneNewSeason.setBrand(brand);
    return fanzoneNewSeason;
  }

  public Optional<FanzoneNewSeason> findAllByBrand(String brand) {
    Optional<FanzoneNewSeason> fanzoneNewSeason = fanzonesNewSeasonRepository.findAllByBrand(brand);
    if (fanzoneNewSeason.isPresent()) {
      return fanzoneNewSeason;
    } else {
      return Optional.of(new FanzoneNewSeason());
    }
  }

  public FanzoneNewSeason findAllByBrandAndId(String brand, String id) {
    Optional<FanzoneNewSeason> fanzoneNewSeason =
        fanzonesNewSeasonRepository.findAllByBrandAndId(brand, id);
    return fanzoneNewSeason.isPresent() ? fanzoneNewSeason.get() : new FanzoneNewSeason();
  }

  public Boolean checkFanzoneNewSeason(String brand) {
    Optional<FanzoneNewSeason> fanzoneNewSeason = fanzonesNewSeasonRepository.findAllByBrand(brand);
    Boolean isFanzoneNewSeaosnCreated = false;
    if (fanzoneNewSeason.isPresent()) {
      isFanzoneNewSeaosnCreated = true;
    }
    return isFanzoneNewSeaosnCreated;
  }

  public FanzoneNewSeason getFanzoneNewSeason(FanzoneNewSeason dto, String brand) {
    Boolean isFanzoneNewSeasonCreated = checkFanzoneNewSeason(brand);
    if (Boolean.TRUE.equals(isFanzoneNewSeasonCreated)) {
      throw new FanzoneNewSeasonCreateException(FZConstants.FANZONENEWSEASON_ALREADYEXIST);
    } else {
      return createFanzoneNewSeason(dto, brand);
    }
  }

  public void deleteAllByBrand(String brand) {
    Optional<FanzoneNewSeason> fanzoneNewSeasons =
        fanzonesNewSeasonRepository.findAllByBrand(brand);
    if (fanzoneNewSeasons.isPresent()) {
      fanzonesNewSeasonRepository.delete(fanzoneNewSeasons.get());
    } else {
      throw new NotFoundException();
    }
  }

  public FanzoneNewSeason populateCreatorAndUpdater(
      CrudService<User> userServiceObj, @NotNull FanzoneNewSeason entity) {
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
