package com.entain.oxygen.promosandbox.controller;

import com.entain.oxygen.promosandbox.dto.PromoMessageDto;
import com.entain.oxygen.promosandbox.handler.PromoConfigMessageHandler;
import javax.validation.Valid;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
@Slf4j
public class QAController implements AbstractApi {

  private final PromoConfigMessageHandler promoConfigMessageHandler;

  @Autowired
  public QAController(PromoConfigMessageHandler promoConfigMessageHandler) {
    this.promoConfigMessageHandler = promoConfigMessageHandler;
  }

  @PostMapping(value = "publish-message")
  public void handleMessage(@RequestBody @Valid PromoMessageDto requestDto) {
    log.info("requestData :{} ", requestDto);
    promoConfigMessageHandler.handleKafkaMessage(requestDto);
  }
}
