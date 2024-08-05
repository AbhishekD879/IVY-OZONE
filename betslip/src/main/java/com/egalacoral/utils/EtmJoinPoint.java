/**
 * Created by oleg.perushko@symphony-solutions.eu on 25.04.16
 */
package com.egalacoral.utils;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface EtmJoinPoint {
}
