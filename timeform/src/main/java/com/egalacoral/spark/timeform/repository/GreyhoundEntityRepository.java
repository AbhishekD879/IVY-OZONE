package com.egalacoral.spark.timeform.repository;

import com.egalacoral.spark.timeform.entity.GreyhoundEntity;
import java.util.List;
import java.util.Optional;
import org.socialsignin.spring.data.dynamodb.repository.EnableScan;
import org.springframework.data.repository.CrudRepository;

@EnableScan
public interface GreyhoundEntityRepository extends CrudRepository<GreyhoundEntity, Integer> {
  Optional<GreyhoundEntity> findByGreyhoundId(Integer id);

  List<GreyhoundEntity> findByGreyhoundIdIn(Iterable<Integer> id);
}
