package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.archival.repository.SportCategoryArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.entity.SportCategoryArchive;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.repository.SportCategoryRepository;
import com.ladbrokescoral.oxygen.cms.api.scheduler.ScheduledTaskExecutor;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.ObjectUtils;
import org.bson.types.ObjectId;
import org.modelmapper.ModelMapper;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.springframework.util.CollectionUtils;

@Slf4j
@Component
@AllArgsConstructor
public class SportCategoryArchivalUploadTask {

  private final ScheduledTaskExecutor scheduledTaskExecutor;
  private final SportCategoryArchivalRepository sportCategoryArchivalRepository;
  private final SportCategoryRepository sportCategoryRepository;
  private final ModelMapper modelMapper;

  @Scheduled(cron = "${sportCategory.uploadArchival.cron}")
  public void uploadArchivalRecords() {
    scheduledTaskExecutor.execute(this::uploadSportCategoriesRecords);
  }

  private void uploadSportCategoriesRecords() {

    List<SportCategory> categories = sportCategoryRepository.findAll();
    List<SportCategoryArchive> archivalCategories = new ArrayList<>();
    List<SportCategory> updatecategories = new ArrayList<>();
    Instant updateDate = Instant.now().truncatedTo(ChronoUnit.DAYS).minus(1, ChronoUnit.DAYS);
    categories.forEach(
        (SportCategory category) -> {
          if (ObjectUtils.isEmpty(category.getArchivalId())) {
            category.setArchivalId(ObjectId.get().toHexString());
            updatecategories.add(category);
            archivalCategories.add(prepareArchiveEntity(category));
          } else if (category.getUpdatedAt().isAfter(updateDate)) {
            archivalCategories.add(prepareArchiveEntity(category));
          }
        });

    try {
      if (!CollectionUtils.isEmpty(updatecategories))
        sportCategoryRepository.saveAll(updatecategories);

      if (!CollectionUtils.isEmpty(archivalCategories))
        sportCategoryArchivalRepository.saveAll(archivalCategories);
    } catch (Exception e) {
      log.error("Error while Executing uploadSportCategoriesRecords", e);
    } finally {
      log.info("uploadSportCategoriesRecords completed");
    }
  }

  private SportCategoryArchive prepareArchiveEntity(SportCategory category) {
    SportCategoryArchive archive = modelMapper.map(category, SportCategoryArchive.class);
    archive.setId(null);
    return archive;
  }
}
