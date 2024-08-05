package com.ladbrokescoral.oxygen.service;

import com.ladbrokescoral.oxygen.dto.messages.SimpleMessage;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Qualifier("lastMessageCache")
@Repository
public interface LastMessageCache extends CrudRepository<SimpleMessage, String> {}
