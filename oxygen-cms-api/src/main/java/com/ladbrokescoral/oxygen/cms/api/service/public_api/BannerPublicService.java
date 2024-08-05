package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.BannerDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.mapping.BannerMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.BannerRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SportCategoryRepository;
import java.time.Instant;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.bson.types.ObjectId;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Slf4j
@Service
public class BannerPublicService {

  private final BannerRepository repository;
  private final SportCategoryRepository sportCategoryRepository;

  public BannerPublicService(
      BannerRepository repository, SportCategoryRepository sportCategoryRepository) {
    this.repository = repository;
    this.sportCategoryRepository = sportCategoryRepository;
  }

  public List<BannerDto> find(String brand, String categoryName) {
    Collection<SportCategory> categories =
        sportCategoryRepository.findAllByMatchingTargetUri(categoryName, brand);
    if (CollectionUtils.isEmpty(categories)) {
      log.info("No category found by targetUri {}", categoryName);
      return Collections.emptyList();
    }

    List<ObjectId> listOfObjectId =
        categories.stream()
            .map(SportCategory::getId)
            .map(ObjectId::new)
            .collect(Collectors.toList());

    return repository
        .findAllByBrandAndDisabledAndCategoryIdInAndValidityPeriodStartBeforeAndValidityPeriodEndAfterOrderBySortOrder(
            brand, false, listOfObjectId, Instant.now(), Instant.now())
        .stream()
        .map(BannerMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }
}
