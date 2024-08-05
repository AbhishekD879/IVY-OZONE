package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.MyBet;
import org.springframework.stereotype.Repository;

@Repository
public interface MyBetsRepository extends CustomMongoRepository<MyBet> {}
