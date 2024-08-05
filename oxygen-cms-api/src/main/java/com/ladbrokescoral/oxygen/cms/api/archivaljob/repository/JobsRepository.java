package com.ladbrokescoral.oxygen.cms.api.archivaljob.repository;

import com.ladbrokescoral.oxygen.cms.api.archivaljob.repository.entity.Jobs;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface JobsRepository extends MongoRepository<Jobs, String> {

  Jobs findFirstByJobNameAndJobStatusOrderByUpdatedDateDesc(String jobName, String status);
}
