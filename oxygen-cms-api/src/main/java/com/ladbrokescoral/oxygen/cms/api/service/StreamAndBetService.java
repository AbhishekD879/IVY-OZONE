package com.ladbrokescoral.oxygen.cms.api.service;

import static com.ladbrokescoral.oxygen.cms.api.entity.StreamAndBet.SABChildElement;

import com.ladbrokescoral.oxygen.cms.api.dto.StreamAndBetDto;
import com.ladbrokescoral.oxygen.cms.api.entity.StreamAndBet;
import com.ladbrokescoral.oxygen.cms.api.mapping.StreamAndBetMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.StreamAndBetRepository;
import java.util.Optional;
import org.springframework.stereotype.Component;

@Component
public class StreamAndBetService extends AbstractService<StreamAndBet> {

  private final StreamAndBetRepository streamAndBetRepository;

  public StreamAndBetService(StreamAndBetRepository streamAndBetRepository) {
    super(streamAndBetRepository);
    this.streamAndBetRepository = streamAndBetRepository;
  }

  public Optional<StreamAndBet> findOneByBrand(String brand) {
    return streamAndBetRepository.findOneByBrand(brand);
  }

  public StreamAndBetDto addCategory(StreamAndBet streamAndBet, SABChildElement category) {
    Optional<SABChildElement> childElement =
        streamAndBet.getChildren().stream()
            .filter(value -> value.getSiteServeId().equals(category.getSiteServeId()))
            .findFirst();
    childElement.ifPresent(value -> streamAndBet.getChildren().remove(value));

    streamAndBet.getChildren().add(category);
    return StreamAndBetMapper.INSTANCE.toDto(streamAndBetRepository.save(streamAndBet));
  }

  public void removeCategory(StreamAndBet streamAndBet, SABChildElement category) {
    streamAndBet.getChildren().remove(category);
    streamAndBetRepository.save(streamAndBet);
  }
}
