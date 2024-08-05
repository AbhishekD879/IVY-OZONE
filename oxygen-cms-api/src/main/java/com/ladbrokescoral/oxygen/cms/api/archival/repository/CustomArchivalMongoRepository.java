package com.ladbrokescoral.oxygen.cms.api.archival.repository;

import java.time.Instant;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.repository.NoRepositoryBean;

@NoRepositoryBean
public interface CustomArchivalMongoRepository<E> extends MongoRepository<E, String> {

  void deleteByArchivalDateBefore(Instant now);
}
