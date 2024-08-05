package com.egalacoral.spark.timeform.controller.api;

import java.util.Optional;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

public class ResponseEntityBuilder {

  public static <T> ResponseEntity<T> build(Optional<T> optional) {
    ResponseEntity<T> entity;
    if (optional.isPresent()) {
      entity = new ResponseEntity<T>(optional.get(), HttpStatus.OK);
    } else {
      entity = new ResponseEntity<T>(HttpStatus.NOT_FOUND);
    }
    return entity;
  }

  public static <T> ResponseEntity<T> build(T object) {
    ResponseEntity<T> entity;
    if (object != null) {
      entity = new ResponseEntity<T>(object, HttpStatus.OK);
    } else {
      entity = new ResponseEntity<T>(HttpStatus.NOT_FOUND);
    }
    return entity;
  }
}
