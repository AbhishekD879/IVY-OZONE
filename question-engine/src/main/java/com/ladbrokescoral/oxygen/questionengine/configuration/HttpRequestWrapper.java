package com.ladbrokescoral.oxygen.questionengine.configuration;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

import javax.servlet.http.HttpServletRequest;

@Component
@Getter
@RequiredArgsConstructor
public class HttpRequestWrapper {
  private final HttpServletRequest request;
}
