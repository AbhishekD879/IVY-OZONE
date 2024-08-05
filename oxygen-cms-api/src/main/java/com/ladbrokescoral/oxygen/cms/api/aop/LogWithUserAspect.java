package com.ladbrokescoral.oxygen.cms.api.aop;

import com.amazonaws.services.s3.model.PutObjectRequest;
import java.io.InputStream;
import java.util.Optional;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.aspectj.lang.annotation.Pointcut;
import org.aspectj.lang.reflect.CodeSignature;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;

@Aspect
@Slf4j(topic = "UserLog")
@Component
public class LogWithUserAspect {

  public static final String LOG_FORMAT = "[user: %s] %s";
  public static final String UPLOADING_IMAGE_LOG_MASK = "Uploading image %s to %s by path %s";
  public static final String UPLOADING_LOG_MASK = "Uploading %s by path %s for brand %s";
  public static final String MONGO_UPDATES_LOG_MASK = "Updating %s entity in Mongo";
  public static final String CONTROLLER_LOG_MASK = "Executing %s in %s controller with args [%s]";
  public static final String ARG_MASK = "{%s : %s}";

  @Pointcut("within(com.ladbrokescoral.oxygen.cms.api.controller.private_api..*)")
  public void privateApiPointcut() {
    // pointcut doesn't require body.
  }

  @Pointcut(
      "@annotation(org.springframework.web.bind.annotation.PostMapping) ||"
          + " @annotation(org.springframework.web.bind.annotation.DeleteMapping) || "
          + "@annotation(org.springframework.web.bind.annotation.PutMapping)")
  public void restOperationsPointcut() {
    // pointcut doesn't require body.
  }

  @Pointcut(
      "execution(public * com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService.upload(..))")
  public void sigletonForcePointcut() {
    // pointcut doesn't require body.
  }

  @Pointcut("privateApiPointcut() && restOperationsPointcut()")
  public void privateApiLogPointcut() {
    // pointcut doesn't require body.
  }

  @Before("privateApiLogPointcut()")
  public void logPrivateApi(JoinPoint joinPoint) {
    doLog(
        String.format(
            CONTROLLER_LOG_MASK,
            joinPoint.getSignature().getName(),
            joinPoint.getTarget().getClass().getSimpleName(),
            getArgs(joinPoint)));
  }

  @Before("sigletonForcePointcut() && args(path, fileName, *, brand)")
  public void singletonForce(String path, String fileName, String brand) {
    doLog(String.format(UPLOADING_LOG_MASK, fileName, path, brand));
  }

  @Before("execution(public * org.springframework.data.repository.CrudRepository.save(..))")
  public void mongoSaveOperation(JoinPoint joinPoint) {
    doLog(String.format(MONGO_UPDATES_LOG_MASK, joinPoint.getArgs()[0].getClass().getSimpleName()));
  }

  @Before(
      "execution(public * com.ladbrokescoral.oxygen.cms.api.service.BrandCacheService.uploadFile(..)) && args(relativePath, fileName, fileStream)")
  public void akamaiImageUpload(String relativePath, String fileName, InputStream fileStream) {
    doLog(String.format(UPLOADING_IMAGE_LOG_MASK, fileName, "Akamai", relativePath));
  }

  @Before(
      "execution(public * com.amazonaws.services.s3.AmazonS3.putObject(..)) && args(putObjectRequest)")
  public void amazonImageUpload(PutObjectRequest putObjectRequest) {
    doLog(String.format(UPLOADING_IMAGE_LOG_MASK, "", "Amazon", putObjectRequest.getKey()));
  }

  private void doLog(String message) {

    String userDetails =
        Optional.ofNullable(SecurityContextHolder.getContext().getAuthentication())
            .filter(Authentication::isAuthenticated)
            .map(Authentication::getPrincipal)
            .map(Object::toString)
            .orElse("no authentication available");

    log.info(String.format(LOG_FORMAT, userDetails, message));
  }

  // creates a comma separated list of {"argName" : "argValue"}, ...
  private String getArgs(JoinPoint joinPoint) {
    String[] parameterNames = ((CodeSignature) joinPoint.getSignature()).getParameterNames();
    return IntStream.range(0, joinPoint.getArgs().length)
        .mapToObj(i -> String.format(ARG_MASK, parameterNames[i], joinPoint.getArgs()[i]))
        .collect(Collectors.joining(", "));
  }
}
