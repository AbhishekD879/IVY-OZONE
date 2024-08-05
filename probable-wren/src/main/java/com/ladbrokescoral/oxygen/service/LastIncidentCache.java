package com.ladbrokescoral.oxygen.service;

import com.ladbrokescoral.oxygen.dto.messages.IncidentMessage;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Qualifier("lastIncidentCache")
@Repository
public interface LastIncidentCache extends CrudRepository<IncidentMessage, String> {}
