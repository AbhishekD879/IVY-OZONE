package com.egalacoral.spark.timeform.api;

import java.util.HashMap;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.egalacoral.spark.timeform.api.connectivity.*;
import com.egalacoral.spark.timeform.api.services.AuthenticationService;
import com.egalacoral.spark.timeform.api.services.DataService;
import com.egalacoral.spark.timeform.model.internal.TokenData;

/**
 * This class allows you to login into TimeForm API
 *
 * Instance of this class can be created through TimeFormAPIBuilder class
 * */
public class TimeFormAPI {

  private static final transient Logger LOGGER = LoggerFactory.getLogger(TimeFormAPI.class);

  private static final String SLASH = "/";

  private final TimeFormContext context;

  private final AuthenticationService authenticationService;

  private RequestPerformer simpleRequestPerformer;

  private RequestPerformer requestPerformer;

  private String userName;

  private String password;

  private TimeFormService timeFormService;

  TimeFormAPI(String loginUrl, String dataUrl, TimeProvider timeProvider, FailOverStrategy failOverStrategy) {
    context = new TimeFormContext(addSlash(loginUrl), addSlash(dataUrl));
    simpleRequestPerformer = new SimpleRequestPerformer();
    Map<Long, Integer> timeLimits = new HashMap<>();
    timeLimits.put(1000L * 60 * 60, 3000);
    timeLimits.put(1000L, 1);
    requestPerformer = new TimeLimitRequestPerformer(simpleRequestPerformer, timeProvider, timeLimits);
    requestPerformer = new FailOverRequestPerformer(requestPerformer, failOverStrategy, this::internalLogin);
    context.setRequestPerformer(requestPerformer);
    authenticationService = new AuthenticationService(context);
  }

  private static String addSlash(String url) {
    if (!url.endsWith(SLASH)) {
      url = url + SLASH;
    }
    return url;
  }

  private void internalLogin() {
    TokenData sessionToken =
        simpleRequestPerformer.invokeSync(authenticationService.getSessionToken(userName, password));
    LOGGER.info("Success login. {}", sessionToken);
    context.setTokenData(sessionToken);
  }

  /**
   * Login into timeform system
   *
   * @return instance of TimeFormService class which should be used for data retrivement
   */
  public synchronized TimeFormService login(String userName, String password) {
    this.userName = userName;
    this.password = password;
    context.setUserName(userName);
    internalLogin();
    if (timeFormService == null) {
      timeFormService = new TimeFormService(new DataService(context));
    }
    return timeFormService;
  }

}
