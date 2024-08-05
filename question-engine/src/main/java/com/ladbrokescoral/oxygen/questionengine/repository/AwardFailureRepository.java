package com.ladbrokescoral.oxygen.questionengine.repository;

import com.ladbrokescoral.oxygen.questionengine.model.AwardStatus;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface AwardFailureRepository extends CrudRepository<AwardStatus, AwardStatus.Id> {
}
