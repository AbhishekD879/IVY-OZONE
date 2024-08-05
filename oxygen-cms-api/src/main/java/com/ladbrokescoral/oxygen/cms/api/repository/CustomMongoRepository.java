package com.ladbrokescoral.oxygen.cms.api.repository;

import java.util.List;
import java.util.Optional;
import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import org.springframework.data.repository.NoRepositoryBean;

@NoRepositoryBean
public interface CustomMongoRepository<E> extends MongoRepository<E, String> {

  Optional<E> findById(String id);

  @Query("{'brand' : ?0}")
  List<E> findByBrand(String brand, Sort sort);

  @Query("{'brand' : ?0}")
  List<E> findByBrand(String brand);

  /** Can be used to return projection */
  <T> T findById(String id, Class<T> type);

  @Query("{ _id : {'$in' : ?0}}")
  List<E> findByIdMatches(List<String> ids);
}
