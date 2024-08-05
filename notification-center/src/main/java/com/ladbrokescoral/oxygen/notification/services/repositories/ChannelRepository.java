package com.ladbrokescoral.oxygen.notification.services.repositories;

import com.ladbrokescoral.oxygen.notification.entities.dto.ChannelDTO;
import java.util.List;
import org.springframework.data.repository.CrudRepository;

public interface ChannelRepository extends CrudRepository<ChannelDTO, String> {
  List<ChannelDTO> findByName(String name);
}
