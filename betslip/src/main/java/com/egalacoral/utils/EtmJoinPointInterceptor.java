/**
 * Created by oleg.perushko@symphony-solutions.eu on 25.04.16
 */
package com.egalacoral.utils;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Aspect
@Component
public class EtmJoinPointInterceptor {

	@Autowired
	private EtmJoinPointService joinPointService;

	@Pointcut(value = "execution(public * *(..))")
	public void anyPublicMethod() {}

	@Around("anyPublicMethod() && @annotation(logAction)")
	public Object logAction(ProceedingJoinPoint pjp, EtmJoinPoint logAction) throws Throwable {
		return null;
	}
}
