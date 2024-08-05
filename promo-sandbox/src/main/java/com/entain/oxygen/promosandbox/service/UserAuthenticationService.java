package com.entain.oxygen.promosandbox.service;

import com.entain.oxygen.promosandbox.dto.bpp.BppTokenRequest;
import com.entain.oxygen.promosandbox.dto.bpp.UserData;
import com.entain.oxygen.promosandbox.exception.BppTokenRequiredException;
import com.entain.oxygen.promosandbox.exception.InvalidBppTokenException;
import com.entain.oxygen.promosandbox.utils.JsonUtil;
import java.util.Objects;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;

@Service
@Slf4j
public class UserAuthenticationService {

  @Value("${promosandbox.enableSecurity}")
  private boolean enableSecurity;

  public final WebClient webClient;

  public UserAuthenticationService(WebClient webClient) {
    this.webClient = webClient;
  }

  public void validateToken(String token, String customerId) {
    if (enableSecurity && StringUtils.hasText(customerId)) {
      validateTokenAndCustomerId(token, customerId);
      try {
        BppTokenRequest bppTokenRequest = new BppTokenRequest().setToken(token);
        String jsonReqData = JsonUtil.toJson(bppTokenRequest);
        UserData userData =
            webClient
                .method(HttpMethod.POST)
                .uri("/auth/userdata")
                .body(BodyInserters.fromValue(jsonReqData))
                .accept(MediaType.APPLICATION_JSON)
                .retrieve()
                .bodyToMono(UserData.class)
                .block();
        if (Objects.isNull(userData) || !userData.isUserValid()) {
          throw new InvalidBppTokenException("Invalid token bpp");
        }
      } catch (Exception ex) {
        log.error("Error while validating bpp token. {} ", ex.getMessage());
        throw new InvalidBppTokenException("Invalid token bpp");
      }
    }
  }

  public void validateTokenAndCustomerId(String token, String customerId) {
    if (StringUtils.hasText(customerId) && !StringUtils.hasText(token)) {
      throw new BppTokenRequiredException("token is missing in header");
    }
  }
}
