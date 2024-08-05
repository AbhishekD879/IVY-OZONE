package com.ladbrokescoral.oxygen.notification.services.repositories;

import com.ladbrokescoral.oxygen.notification.entities.sportsbook.Event;
import org.springframework.data.repository.CrudRepository;

public interface Events extends CrudRepository<Event, String> {}
