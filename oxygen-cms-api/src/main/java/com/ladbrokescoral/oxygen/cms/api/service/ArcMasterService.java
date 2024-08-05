package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.ArcMasterData;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.ArcMasterRepository;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import org.apache.commons.collections4.CollectionUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

@Service
public class ArcMasterService {

  private ArcMasterRepository arcMasterRepository;

  @Autowired
  public ArcMasterService(ArcMasterRepository arcMasterRepository) {
    this.arcMasterRepository = arcMasterRepository;
  }

  public ArcMasterData getMasterDataByLineItem(String masterLineName) {
    return arcMasterRepository.findByMasterLineName(masterLineName);
  }

  public ResponseEntity<ArcMasterData> createMasterData(ArcMasterData arcMasterData) {
    ArcMasterData savedEntity = arcMasterRepository.save(arcMasterData);
    return new ResponseEntity<>(savedEntity, HttpStatus.CREATED);
  }

  public ArcMasterData update(
      Optional<ArcMasterData> existingEntity, final ArcMasterData updateEntity) {
    return existingEntity
        .map((ArcMasterData entity) -> arcMasterRepository.save(updateEntity))
        .orElseThrow(NotFoundException::new);
  }

  public List<ArcMasterData> getAllMetadata() {
    List<ArcMasterData> masterData = arcMasterRepository.findAll();
    if (CollectionUtils.isNotEmpty(masterData)) {
      return masterData;
    }
    return Collections.emptyList();
  }
}
