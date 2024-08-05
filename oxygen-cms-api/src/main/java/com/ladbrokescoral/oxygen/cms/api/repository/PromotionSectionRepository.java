package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.PromotionSection;
import java.util.List;
import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.repository.Query;

public interface PromotionSectionRepository extends CustomMongoRepository<PromotionSection> {
  @Query("{" + "'brand': ?0, " + "'disabled': false" + "}")
  List<PromotionSection> findSections(String brand, Sort order);
}
