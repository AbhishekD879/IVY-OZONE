package com.ladbrokescoral.oxygen.cms.api.archivaljob.repository;

import com.ladbrokescoral.oxygen.cms.api.archivaljob.repository.entity.DataRetentionJobs;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface DataRetentionJobsRepository extends MongoRepository<DataRetentionJobs, String> {}
