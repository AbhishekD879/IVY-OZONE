package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.MyStable;
import java.util.List;
import java.util.Optional;
import org.springframework.data.mongodb.repository.Query;

public interface MyStableRepository extends CustomMongoRepository<MyStable> {
  Optional<MyStable> findOneByBrand(String brand);

  List<MyStable> findByBrand(String brand);

  @Query("{'brand' : ?0}")
  MyStable getByBrand(String brand);
}
