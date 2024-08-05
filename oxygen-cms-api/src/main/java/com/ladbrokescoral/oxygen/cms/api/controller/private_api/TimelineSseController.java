package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.service.TimelineSseService;
import lombok.AllArgsConstructor;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

@RestController
@AllArgsConstructor
public class TimelineSseController implements Abstract {
  private TimelineSseService timelineSseService;

  @GetMapping(
      value = {"/timeline/sse"},
      produces = MediaType.TEXT_EVENT_STREAM_VALUE)
  public SseEmitter streamSseMvc() {
    return timelineSseService.createAndRegisterEmitter();
  }
}
