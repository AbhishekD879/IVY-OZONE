package com.ladbrokescoral.oxygen.betpackmp.redis;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

/*
 class is repository for active bet pack ids
*/
@Repository
public interface BetPackRepository extends CrudRepository<ActiveBetPacks, String> {}
