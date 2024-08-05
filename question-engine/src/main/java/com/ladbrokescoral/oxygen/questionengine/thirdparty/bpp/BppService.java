package com.ladbrokescoral.oxygen.questionengine.thirdparty.bpp;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestParam;

import com.ladbrokescoral.oxygen.questionengine.configuration.BppFeignConfig;
import com.ladbrokescoral.oxygen.questionengine.model.bpp.BppTokenRequest;
import com.ladbrokescoral.oxygen.questionengine.model.bpp.FreebetTriggerResponse;
import com.ladbrokescoral.oxygen.questionengine.model.bpp.UserData;

@FeignClient(name = "bpp", url = "${bpp.baseUrl}", configuration = BppFeignConfig.class)
public interface BppService {

  @PostMapping("/Proxy/auth/userdata")
  UserData findUserData(@RequestBody BppTokenRequest tokenRequest);

  @GetMapping("/Proxy/optinTrigger")
  FreebetTriggerResponse triggerFreebet(@RequestHeader("token") String token, @RequestParam("id") String promotionId);
}
