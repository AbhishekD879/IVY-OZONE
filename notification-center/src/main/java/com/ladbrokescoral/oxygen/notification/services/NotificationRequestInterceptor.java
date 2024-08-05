package com.ladbrokescoral.oxygen.notification.services;

import com.ladbrokescoral.oxygen.notification.utils.RequestLoggingUtil;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.handler.HandlerInterceptorAdapter;
import org.springframework.web.util.ContentCachingRequestWrapper;

@Component
public class NotificationRequestInterceptor extends HandlerInterceptorAdapter {

  private static final Logger logger =
      LoggerFactory.getLogger(NotificationRequestInterceptor.class);

  @Override
  public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler)
      throws Exception {
    String postData;
    HttpServletRequest requestCacheWrapperObject = null;
    try {
      requestCacheWrapperObject = new ContentCachingRequestWrapper(request);
      requestCacheWrapperObject.getParameterMap();
    } catch (Exception exception) {
      exception.printStackTrace();
    } finally {
      postData = RequestLoggingUtil.readPayload(requestCacheWrapperObject);
      logger.info("REQUEST DATA: " + postData);
    }
    return true;
  }

  @Override
  public void afterCompletion(
      HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex)
      throws Exception {
    logger.info("RESPONSE: " + response.getStatus());
  }
}
