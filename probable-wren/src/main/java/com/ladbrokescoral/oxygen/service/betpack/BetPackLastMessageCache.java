package com.ladbrokescoral.oxygen.service.betpack;

import com.ladbrokescoral.oxygen.dto.messages.BetPackMessage;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Qualifier("betPackLastMessageCache")
@Repository
public interface BetPackLastMessageCache extends CrudRepository<BetPackMessage, String> {}
