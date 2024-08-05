package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.QuizPopupSetting;
import java.util.Optional;

public interface QuizPopupSettingRepository extends CustomMongoRepository<QuizPopupSetting> {
  Optional<QuizPopupSetting> findOneByBrand(String brand);

  boolean existsByBrand(String brand);
}
