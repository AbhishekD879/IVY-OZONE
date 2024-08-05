package com.ladbrokescoral.oxygen.questionengine.configuration.annotation;

import org.springframework.context.annotation.Profile;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * Excludes annotated bean from being scanned during Integration test context setup.
 */
@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.TYPE, ElementType.METHOD})
@Profile("!INTEGRATION-TEST")
public @interface ExcludeFromIntegrationTests {

}
