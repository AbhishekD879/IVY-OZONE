package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.RssReward;
import com.ladbrokescoral.oxygen.cms.api.repository.CustomMongoRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.RssRepository;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class RssRewardService extends AbstractService<RssReward> {
  private final RssRepository rssRepository;

  public RssRewardService(
      CustomMongoRepository<RssReward> repository, RssRepository rssRepository) {
    super(repository);
    this.rssRepository = rssRepository;
  }

  public RssReward getRssReward(String brand) {
    log.info("getRssReward call");
    return rssRepository.findOneByBrand(brand).orElse(new RssReward());
  }

  public ResponseEntity<String> deleteRssReward(String brand) {
    rssRepository.deleteByBrand(brand);
    return ResponseEntity.of(Optional.of("Rss reward deleted"));
  }
}
