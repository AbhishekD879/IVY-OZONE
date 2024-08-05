package com.entain.oxygen.promosandbox.repository;

import com.entain.oxygen.promosandbox.model.PromoConfig;
import java.util.List;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface PromoConfigRepository extends MongoRepository<PromoConfig, String> {

  List<PromoConfig> findAllByBrandAndIsDataCleaned(String brand, boolean isDataCleaned);

  List<PromoConfig> findAllByPromotionId(String promotionId);
}
