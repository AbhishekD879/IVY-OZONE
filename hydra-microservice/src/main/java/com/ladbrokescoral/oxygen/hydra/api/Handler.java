package com.ladbrokescoral.oxygen.hydra.api;

import com.ladbrokescoral.oxygen.hydra.dto.Response;
import java.time.Instant;
import javax.servlet.http.HttpServletRequest;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class Handler {

  @CrossOrigin
  @RequestMapping("/v1/session")
  public Response get(HttpServletRequest request) {

    return new Response(request.getRemoteAddr(), Instant.now().toEpochMilli());
  }
}
