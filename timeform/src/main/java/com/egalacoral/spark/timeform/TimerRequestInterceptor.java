package com.egalacoral.spark.timeform;

import com.egalacoral.spark.timeform.timer.TimerService;
import etm.core.monitor.EtmPoint;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.handler.HandlerInterceptorAdapter;

public class TimerRequestInterceptor extends HandlerInterceptorAdapter {

  private TimerService timerService;

  public TimerRequestInterceptor(TimerService timerService) {
    this.timerService = timerService;
  }

  @Override
  public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler)
      throws Exception {
    EtmPoint etmPoint = timerService.createPoint(request.getRequestURI());
    request.setAttribute(EtmPoint.class.getName(), etmPoint);
    return super.preHandle(request, response, handler);
  }

  @Override
  public void postHandle(
      HttpServletRequest request,
      HttpServletResponse response,
      Object handler,
      ModelAndView modelAndView)
      throws Exception {
    super.postHandle(request, response, handler, modelAndView);
  }

  @Override
  public void afterCompletion(
      HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex)
      throws Exception {
    super.afterCompletion(request, response, handler, ex);
    EtmPoint etmPoint = (EtmPoint) request.getAttribute(EtmPoint.class.getName());
    if (etmPoint != null) {
      timerService.submit(etmPoint);
    }
  }
}
