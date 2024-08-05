package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.constants.FZConstants;
import com.ladbrokescoral.oxygen.cms.api.entity.Fanzone;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.exception.InvalidPageNameException;
import com.ladbrokescoral.oxygen.cms.api.exception.InvalidTeamIdException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.FanzonesRepository;
import com.ladbrokescoral.oxygen.cms.util.Util;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import javax.validation.constraints.NotNull;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.validation.annotation.Validated;

@Slf4j
@Component
@Validated
public class FanzonesService extends AbstractService<Fanzone> {

  private FanzonesRepository fanzonesRepository;

  @Autowired
  public FanzonesService(FanzonesRepository fanzonesRepository) {
    super(fanzonesRepository);
    this.fanzonesRepository = fanzonesRepository;
  }

  // to get all the fanzones from the repository based on the brand
  public Optional<List<Fanzone>> findAllFanzonesByBrand(String brand) {
    return fanzonesRepository.findAllFanzonesByBrand(brand);
  }

  // to get a specific fanzone based on the id
  public Fanzone findByBrandAndColumn(String brand, String column, String val) {
    Optional<Fanzone> fanzone = fanzonesRepository.findByBrandAndColumn(brand, column, val);
    return fanzone.isPresent() ? fanzone.get() : new Fanzone();
  }

  // to delete specific fanzone based on the id
  public void deleteByBrandAndColumn(String brand, String column, String value) {
    Fanzone fanzone =
        fanzonesRepository
            .findByBrandAndColumn(brand, column, value)
            .orElseThrow(NotFoundException::new);
    fanzonesRepository.delete(fanzone);
  }

  // to delete all fanzones
  public void deleteAllByBrand(String brand) {
    Optional<List<Fanzone>> fanzones = fanzonesRepository.findAllFanzonesByBrand(brand);
    if (fanzones.isPresent()) {
      fanzones.get().stream().forEach(fanzone -> fanzonesRepository.delete(fanzone));
    } else {
      throw new NotFoundException();
    }
  }

  // to process the fanzone
  public Fanzone processFanzone(Fanzone fanzoneEntity, String brand) {
    Optional<List<Fanzone>> fanzoneList = findAllFanzonesByBrand(brand);
    if (fanzoneList.isPresent()) {
      checkFanzone(fanzoneList, fanzoneEntity);
      fanzoneEntity.setBrand(brand);
      return fanzoneEntity;
    } else {
      throw new NotFoundException();
    }
  }

  // to process fanzone for update
  public Fanzone processFanzoneForUpdate(Fanzone fanzoneEntity, String brand, Fanzone fanzoneindb) {
    Optional<List<Fanzone>> fanzoneList = findAllFanzonesByBrand(brand);
    if (fanzoneList.isPresent()) {
      fanzoneList.get().removeIf(fanzone -> fanzone.getId().equals(fanzoneindb.getId()));
      checkFanzoneForUpdate(fanzoneList, fanzoneEntity);
      fanzoneEntity.setBrand(brand);
      return fanzoneEntity;
    } else {
      throw new NotFoundException();
    }
  }

  // checking if the fanzone being created has same name or id as remaining fanzones in the
  // collection
  public Fanzone checkFanzone(Optional<List<Fanzone>> fanzoneList, Fanzone fanzoneEntity) {
    if (fanzoneList.isPresent()) {
      List<String> fanzoneNames =
          fanzoneList.get().stream()
              .map(fanzone -> fanzone.getName().toUpperCase())
              .collect(Collectors.toList());
      List<String> teamId =
          fanzoneList.get().stream()
              .map(fanzone -> fanzone.getTeamId().toUpperCase())
              .collect(Collectors.toList());
      if (teamId.contains(fanzoneEntity.getTeamId().toUpperCase())) {
        throw new InvalidTeamIdException(FZConstants.INVALID_TEAMID);
      }
      if ((fanzoneNames.contains(fanzoneEntity.getName().toUpperCase()))) {
        throw new InvalidPageNameException(FZConstants.INVALID_TEAMNAME);
      }
      return fanzoneEntity;
    } else {
      throw new NotFoundException();
    }
  }

  // checking if the fanzone being updated has same teamid or name  same as the remaining fanzones
  // and throwing exception
  public Fanzone checkFanzoneForUpdate(Optional<List<Fanzone>> fanzoneList, Fanzone fanzoneEntity) {
    if (fanzoneList.isPresent()) {
      List<String> fanzoneNames =
          fanzoneList.get().stream()
              .map(fanzone -> fanzone.getName().toUpperCase())
              .collect(Collectors.toList());
      List<String> teamIds =
          fanzoneList.get().stream()
              .map(fanzone -> fanzone.getTeamId().toUpperCase())
              .collect(Collectors.toList());
      if (teamIds.contains(fanzoneEntity.getTeamId().toUpperCase())) {
        throw new InvalidTeamIdException(FZConstants.INVALID_TEAMID);
      }
      if ((fanzoneNames.contains(fanzoneEntity.getName().toUpperCase()))) {
        throw new InvalidPageNameException(FZConstants.INVALID_TEAMNAME);
      }
      return fanzoneEntity;
    } else {
      throw new NotFoundException();
    }
  }

  public Fanzone populateCreatorAndUpdater(
      CrudService<User> userServiceObj, @NotNull Fanzone entity) {
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
