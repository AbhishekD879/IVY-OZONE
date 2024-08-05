package com.ladbrokescoral.oxygen.questionengine.aspect;

import com.ladbrokescoral.oxygen.questionengine.aspect.annotation.Username;
import com.ladbrokescoral.oxygen.questionengine.service.AuthenticationService;
import io.vavr.collection.Stream;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.aspectj.lang.annotation.Pointcut;
import org.aspectj.lang.reflect.MethodSignature;
import org.slf4j.MDC;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Component;
import org.springframework.util.ReflectionUtils;

import java.lang.reflect.Field;
import java.util.Arrays;
import java.util.Optional;
import java.util.function.Function;

@Aspect
@Slf4j
@Component
@ConditionalOnProperty(value = "application.security.disabled", havingValue = "false")
@RequiredArgsConstructor
public class AuthenticateAspect {
  private final AuthenticationService authenticationService;

  @Before("authenticatedMethod() && hasUsernameAnnotatedStringParameter()")
  public void authenticateByUsernameAnnotatedParameter(JoinPoint jp) {
    int index = getUsernameAnnotatedParameterIndex(jp);

    String username = (String) jp.getArgs()[index];

    verifyUser(username);
    MDC.put("user", String.format("[user='%s']", username));
  }

  @Before("authenticatedMethod() && !hasUsernameAnnotatedStringParameter()")
  public void authenticateByUsernameAnnotatedField(JoinPoint jp) {
    String username = getUsernameField(jp);

    verifyUser(username);
    MDC.put("user", String.format("[user='%s']", username));
  }

  @Pointcut("@annotation(com.ladbrokescoral.oxygen.questionengine.aspect.annotation.Authenticate)")
  public void authenticatedMethod() {
  }

  @Pointcut("execution(* *(.., @com.ladbrokescoral.oxygen.questionengine.aspect.annotation.Username (String), ..))")
  public void hasUsernameAnnotatedStringParameter() {
  }


  private void verifyUser(String username) {
    log.info("Authenticating user '{}'", username);

    authenticationService.verifyUser(username);

    log.info("User '{}' successfully authenticated", username);
  }


  private int getUsernameAnnotatedParameterIndex(JoinPoint jp) {

    return Stream.of(((MethodSignature) jp.getSignature()).getMethod().getParameters())
        .zipWithIndex()
        .filter(tuple -> tuple._1.getAnnotation(Username.class) != null)
        .map(tuple -> tuple._2)
        .toJavaOptional().orElseThrow(IllegalStateException::new);
  }

  private String getUsernameField(JoinPoint jp) {
    return Arrays.stream(jp.getArgs())
        .map(this::findUsernameAnnotatedField)
        .filter(Optional::isPresent)
        .findFirst()
        .flatMap(Function.identity())
        .orElseThrow(() -> new IllegalStateException("Couldn't find any @Username annotated field on @Authenticated method"));
  }

  private Optional<String> findUsernameAnnotatedField(Object arg) {
    return Arrays.stream(arg.getClass().getDeclaredFields())
        .filter(field -> field.isAnnotationPresent(Username.class))
        .findFirst()
        .map(field -> getField(arg, field))
        .map(Object::toString);
  }

  private Object getField(Object arg, Field field) {
    ReflectionUtils.makeAccessible(field);

    return ReflectionUtils.getField(field, arg);
  }
}

