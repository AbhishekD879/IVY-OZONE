package com.ladbrokescoral.oxygen.betpackmp.redis.bet_pack;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

/*
 This class is repository for bet pack messages
*/
@Qualifier("betPackLastMessageCache")
@Repository
public interface BetPackLastMessageCache extends CrudRepository<BetPackMessage, String> {}
