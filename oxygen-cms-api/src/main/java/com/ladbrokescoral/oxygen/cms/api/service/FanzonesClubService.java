package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneClub;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesClubRepository;
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
public class FanzonesClubService extends AbstractService<FanzoneClub> {
  private FanzonesClubRepository fanzonesClubRepository;

  @Autowired
  public FanzonesClubService(FanzonesClubRepository fanzonesClubRepository) {
    super(fanzonesClubRepository);
    this.fanzonesClubRepository = fanzonesClubRepository;
  }

  // to get all the fanzoneclubs from the repository based on the brand name
  public Optional<List<FanzoneClub>> findAllFanzonesByBrand(String brand) {
    return fanzonesClubRepository.findAllFanzonesByBrand(brand);
  }

  // to get a specific fanzoneclub based on the id
  public FanzoneClub findByBrandAndColumn(String brand, String column, String val) {
    Optional<FanzoneClub> fanzoneClub =
        fanzonesClubRepository.findByBrandAndColumn(brand, column, val);
    return fanzoneClub.isPresent() ? fanzoneClub.get() : new FanzoneClub();
  }

  // to delete specific fanzoneclub based on the id
  public void deleteByBrandAndColumn(String brand, String column, String value) {
    FanzoneClub fanzoneClub =
        fanzonesClubRepository
            .findByBrandAndColumn(brand, column, value)
            .orElseThrow(NotFoundException::new);
    fanzonesClubRepository.findAllFanzonesByBrand(brand);
    fanzonesClubRepository.delete(fanzoneClub);
  }

  // To delete all the fanzoneclubs
  public void deleteAllByBrand(String brand) {
    Optional<List<FanzoneClub>> fanzonesClub = fanzonesClubRepository.findAllFanzonesByBrand(brand);
    if (fanzonesClub.isPresent()) {
      fanzonesClub.get().stream()
          .forEach(fanzoneClub -> fanzonesClubRepository.delete(fanzoneClub));
    } else {
      throw new NotFoundException();
    }
  }

  public FanzoneClub populateCreatorAndUpdater(
      CrudService<User> userServiceObj, @NotNull FanzoneClub entity) {
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
