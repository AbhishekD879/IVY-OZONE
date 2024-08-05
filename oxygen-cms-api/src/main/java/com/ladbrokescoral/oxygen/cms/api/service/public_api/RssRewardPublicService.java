package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.RssRewardResponse;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.RssReward;
import com.ladbrokescoral.oxygen.cms.api.exception.RssRewardNotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.RssRepository;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class RssRewardPublicService {
  @Value("${public.brand}")
  private String brand;

  @Value("${crm.brand}")
  private String crmBrand;

  @Value("${crm.frontend}")
  private String frontend;

  @Value("${crm.commType}")
  private Integer communicationType;

  private final RssRepository rssRepository;

  public RssRewardPublicService(RssRepository rssRepository) {
    this.rssRepository = rssRepository;
  }

  public ResponseEntity<RssRewardResponse> getRssReward() {
    Optional<RssReward> rssReward = rssRepository.findOneByBrand(brand);
    log.info("getRssReward public api service {}", rssReward);
    if (!rssReward.isPresent()) {
      log.info("Record does not exist in CMS");
      throw new RssRewardNotFoundException("Record does not exist in CMS");
    } else if (!rssReward.get().isEnabled()) {
      log.info("Active record does not exist in CMS");
      throw new RssRewardNotFoundException("Active record does not exist in CMS");
    }
    return ResponseEntity.ok(toResponse(rssReward.get()));
  }

  private RssRewardResponse toResponse(RssReward entity) {
    RssRewardResponse response = new RssRewardResponse();
    response.setSitecoreTemplateId(entity.getSitecoreTemplateId());
    response.setCommunicationType(
        entity.getSitecoreTemplateId() != null ? communicationType : null);
    response.setCoins(entity.getCoins());
    response.setSource(entity.getSource());
    response.setSubSource(entity.getSubSource());
    response.setProduct(entity.getProduct());
    response.setBrand(crmBrand);
    response.setFrontend(frontend);
    return response;
  }
}
