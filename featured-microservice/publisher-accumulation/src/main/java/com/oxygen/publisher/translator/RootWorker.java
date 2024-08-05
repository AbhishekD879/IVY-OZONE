package com.oxygen.publisher.translator;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/** Created by Aliaksei Yarotski on 2/2/18. */
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.SOURCE)
public @interface RootWorker {}
