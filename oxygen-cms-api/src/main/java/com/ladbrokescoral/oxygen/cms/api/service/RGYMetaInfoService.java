package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.RGYMetaInfoEntity;
import com.ladbrokescoral.oxygen.cms.api.repository.RGYMetaInfoRepository;
import java.util.Optional;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

@Service
public class RGYMetaInfoService extends SortableService<RGYMetaInfoEntity> {
  private RGYMetaInfoRepository rgyMetaInfoRepository;

  public RGYMetaInfoService(RGYMetaInfoRepository rgyMetaInfoRepository) {
    super(rgyMetaInfoRepository);
    this.rgyMetaInfoRepository = rgyMetaInfoRepository;
  }

  public ResponseEntity<RGYMetaInfoEntity> getRgyMetaInfo(String brand) {
    Optional<RGYMetaInfoEntity> rgyMetaInfoEntity = rgyMetaInfoRepository.findOneByBrand(brand);
    if (rgyMetaInfoEntity.isPresent()) {
      RGYMetaInfoEntity metaInfo = rgyMetaInfoEntity.get();
      return new ResponseEntity<>(metaInfo, HttpStatus.OK);
    } else {
      RGYMetaInfoEntity metaInfo = new RGYMetaInfoEntity();
      metaInfo.setBrand(brand);
      metaInfo.setRgyEnabled(false);
      rgyMetaInfoRepository.save(metaInfo);
      return new ResponseEntity<>(metaInfo, HttpStatus.OK);
    }
  }

  public ResponseEntity<RGYMetaInfoEntity> updateRgyFlag(String brandCode, boolean rgyFlag) {
    Optional<RGYMetaInfoEntity> rgyMetaInfoEntity = rgyMetaInfoRepository.findOneByBrand(brandCode);
    if (rgyMetaInfoEntity.isPresent()) {
      RGYMetaInfoEntity metaInfo = rgyMetaInfoEntity.get();
      metaInfo.setRgyEnabled(rgyFlag);
      rgyMetaInfoRepository.save(metaInfo);
      return new ResponseEntity<>(metaInfo, HttpStatus.OK);
    } else {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }
  }
}
