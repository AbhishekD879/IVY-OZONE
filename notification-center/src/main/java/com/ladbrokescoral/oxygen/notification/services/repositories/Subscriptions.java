package com.ladbrokescoral.oxygen.notification.services.repositories;

import com.ladbrokescoral.oxygen.notification.entities.dto.SubscriptionDTO;
import java.util.List;
import org.springframework.data.repository.PagingAndSortingRepository;

public interface Subscriptions extends PagingAndSortingRepository<SubscriptionDTO, String> {

  List<SubscriptionDTO> findByEventId(long eventId);

  List<SubscriptionDTO> findAllByType(String type);
}
