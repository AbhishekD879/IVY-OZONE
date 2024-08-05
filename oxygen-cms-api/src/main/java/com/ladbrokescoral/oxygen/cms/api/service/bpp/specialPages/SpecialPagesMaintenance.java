package com.ladbrokescoral.oxygen.cms.api.service.bpp.specialPages;

import com.ladbrokescoral.oxygen.cms.configuration.SpecialPageProperties;
import com.newrelic.api.agent.NewRelic;
import java.util.Map;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

@Slf4j
@Service
public class SpecialPagesMaintenance {
  private final Map<String, SpecialPageProperties.ApiConfiguration> bppAccessUrls;
  private static final String SECRET = "SECRET";
  private final HttpHeaders headers;

  private final RestTemplate restTemplate;

  public SpecialPagesMaintenance(
      SpecialPageProperties specialPageProperties, RestTemplate restTemplate) {
    this.headers = new HttpHeaders();
    this.headers.setContentType(MediaType.APPLICATION_JSON);
    this.restTemplate = restTemplate;
    this.bppAccessUrls = specialPageProperties.getSpecialpageConfig();

    if (CollectionUtils.isEmpty(bppAccessUrls)) {
      log.error("BPP Urls were not configured for SpecialPages Maintenance");
    }
  }

  public void saveOrUpdateSpecialPage(SpecialPageDTO specialPageDTO) {
    String requestUri = "";
    HttpEntity<SpecialPageDTO> entity = null;
    try {
      SpecialPageProperties.ApiConfiguration brandConfig =
          bppAccessUrls.get(specialPageDTO.getBrand());
      String bppUrl = brandConfig.getUrl();
      this.headers.set(SECRET, brandConfig.getSecret());
      requestUri = UriComponentsBuilder.fromHttpUrl(bppUrl).toUriString();
      entity = new HttpEntity(specialPageDTO, headers);
      restTemplate.exchange(requestUri, HttpMethod.POST, entity, Void.class);
    } catch (Exception e) {
      log.error("Issue with posting the specialpage config to BPP", e);
      NewRelic.noticeError(e);
    }
  }
}
