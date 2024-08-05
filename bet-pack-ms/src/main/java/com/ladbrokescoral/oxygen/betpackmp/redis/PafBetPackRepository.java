package com.ladbrokescoral.oxygen.betpackmp.redis;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface PafBetPackRepository extends CrudRepository<PafBetPack, String> {}
