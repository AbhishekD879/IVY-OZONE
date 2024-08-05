package com.coral.oxygen.middleware.featured.repository;

import com.coral.oxygen.middleware.pojos.model.output.NextRaceFilterDto;
import java.util.Optional;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface NextRacesFilterRepository extends CrudRepository<NextRaceFilterDto, String> {
  Optional<NextRaceFilterDto> findByCategoryId(String categoryId);
}
